from django.http import JsonResponse
from pathlib import Path
from pulp import (
    LpAffineExpression,
    LpMinimize,
    LpStatusOptimal,
    LpProblem,
    LpVariable,
)

from multiset.db_utils import execute_query

"""
Our goal is to minimize the amount of total transferred money.
See https://www.notion.so/Optimization-LP-88256a673acb483b9d37bb2a6e7d0959
for a more detailed breakown. This service is basically a step-by-step
recreation of the math there.
"""


def flag(gid: int):
    """
        Checks if optimization is enabled for a group
    Args:
        gid: the id of the group to check
    Returns:
        a dict with key `optimize_payments` and value `True` if optimization is enabled
    """

    result = execute_query(
        Path("optimization/sql/get_optimization_flag.sql"),
        {
            "group_id": gid,
        },
        fetchone=True,
    )

    return result


def toggle(gid: int):
    """
        Toggles optimization for a group
    Args:
        gid: the id of the group to toggle
    Returns:
        a dict with key `optimize_payments` and value `True` if optimization is now enabled
    """

    result = execute_query(
        Path("optimization/sql/toggle_optimization_flag.sql"),
        {
            "group_id": gid,
        },
        fetchone=True,
    )

    return result


def debts(gid: int):
    """
        Gets all debts for a group
    Args:
        gid: the id of the group to get debts for
    Returns:
        a list of dicts representing debts
    """

    result = execute_query(
        Path("optimization/sql/get_overall_balances.sql"),
        {
            "group_id": gid,
        },
        fetchall=True,
    )

    return result


def calculate(gid: int, uid: int, show_all: bool = False):
    """
        Calculates transfers for a group:
        - if optimization is disabled, just returns the balances between each pair of users that need to be resolved
        - if optimization is enabled, solves an ILP to minimize the number of transfers
    Args:
        gid: the id of the group to calculate transfers for
        show_all: whether to show all balances or only those for the current user
    Returns:
        a list of dicts representing optimal transfers
    """

    # first, let's check if optimization is enabled for this group
    # TODO handling of non-existing group
    optimization_flag = flag(gid)

    # if optimization is not enabled, we just get the balances and return them
    if not optimization_flag["optimize_payments"]:
        balances = execute_query(
            Path("optimization/sql/get_aggregated_balances_noopt.sql"),
            {
                "group_id": gid,
            },
            fetchall=True,
        )

        update_debts(balances, gid)

        return _get_response(
            balances, uid, optimization_flag["optimize_payments"], show_all
        )

    # if optimization is enabled, we get the balances and solve the ILP
    balances = execute_query(
        Path("optimization/sql/get_aggregated_balances_opt.sql"),
        {
            "group_id": gid,
        },
        fetchall=True,
    )

    # if all balances are 0, we can return an empty list of transfers
    if all(item["balance"] == 0 for item in balances):
        update_debts(solution, gid)

        return _get_response([], uid, optimization_flag["optimize_payments"], show_all)

    # and we solve the linear program
    solution = _solve_ilp(balances)

    if solution:
        update_debts(
            solution, gid
        )  # we wait to do this in case the solution is not feasible

        return _get_response(
            solution, uid, optimization_flag["optimize_payments"], show_all
        )

    return JsonResponse({"status": "error, no feasible solution found"}, status=500)


def update_debts(balances: list[dict], gid: int):
    """
        Updates the debts recorded for a group in the database
    Args:
        balances: list of dicts representing the balances to update
        gid: the id of the group to update
    """

    # first, delete all debts for this group
    execute_query(
        Path("optimization/sql/delete_group_debts.sql"),
        {"group_id": gid},
    )

    # then, insert the new debts
    for balance in balances:
        # TODO make this a single query?
        execute_query(
            Path("optimization/sql/insert_debt.sql"),
            {
                "amount": balance["amount"],
                "borrower_user_id": balance["from_user_id"],
                "collector_user_id": balance["to_user_id"],
                "borrower_group_id": gid,
                "collector_group_id": gid,
            },
        )


# input is list of dicts with keys: "user_id", "balance"
def _solve_ilp(input: list[dict]):
    """
        Solves an integer linear program (ILP) that minimizes the number of transfers
        to resolve the balances in the input list.
    Args:
        input: list of dicts with keys `member_id` and `balance` representing current balances
        (positive balance => owed money, negative balance => owing money)
    Returns:
        list of dicts with keys `from_id`, `to_id`, `amount` representing optimal transfers
    """

    # first, let's declare our variables
    # transfers[i][j] = x_i_j
    # binary_variables[i][j] = y_i_j

    # as we go, we'll also deal with the objective function
    # which is the sum of all binary variables

    transfers: list[list[LpVariable]] = []
    binary_variables: list[list[LpVariable]] = []
    objective_function = LpAffineExpression()

    for i in range(len(input)):
        transfers.append([])
        binary_variables.append([])

        for j in range(len(input)):
            transfers[-1].append(LpVariable(f"x_{i}_{j}", lowBound=0))
            binary_variables[-1].append(LpVariable(f"y_{i}_{j}", cat="Binary"))

            objective_function += binary_variables[i][j]

    # now we create our model and add the objective function
    model = LpProblem("minimize_total_transfer", LpMinimize)
    model += objective_function

    # let's add the constraints
    for i in range(len(input)):
        expr = LpAffineExpression(input[i]["balance"])

        for j in range(len(input)):
            expr += transfers[i][j]
            expr -= transfers[j][i]

        # this constraint ensures that the balance is 0 after all transfers
        constraint = expr == 0

        model += (constraint, f"balance_{i}")

    for i in range(len(input)):
        for j in range(len(input)):
            # this constraint ensures that the transfer is 0 if the binary variable is 0
            # (i.e. we can't "cheat" the objective function by transferring but still having
            # 0 in the binary variable)
            constraint = transfers[i][j] <= binary_variables[i][j] * abs(
                input[i]["balance"]
            )
            model += (constraint, f"binary_{i}_{j}")

    status = model.solve()

    if status == LpStatusOptimal:
        # We have a solution! Now we need to return it in a way that makes sense
        output = []

        # we iterate over all variables and check if they are > 0
        # if they are, we add that transfer to the list
        for i in range(len(transfers)):
            for j in range(len(transfers[i])):
                if transfers[i][j].value() > 0:
                    output.append(
                        {
                            # group id (same for all transfers in the same group)
                            "group_id": input[i]["group_id"],
                            # giver
                            "from_user_id": input[i]["user_id"],
                            "from_first_name": input[i]["first_name"],
                            "from_last_name": input[i]["last_name"],
                            # receiver
                            "to_user_id": input[j]["user_id"],
                            "to_first_name": input[j]["first_name"],
                            "to_last_name": input[j]["last_name"],
                            # amount
                            "amount": transfers[i][j].value(),
                        }
                    )

        return output

    # if there is no optimal solution we return None
    # this means there is an issue with an invariant in the database
    # (e.g. purchase splits not adding up to the purchase amount)
    # because there is always a feasible solution if everything adds up to 0
    return None


def _get_response(transfers: list[dict], uid: int, optimized: bool, show_all: bool):
    """
        Formats the response for the frontend. This is to ensure consistency
        since this logic is used in multiple places.
    Args:
        transfers: list of dicts representing transfers
        optimized: whether the transfers are optimized
    Returns:
        a JsonResponse object
    """

    if show_all:
        transfers_to_return = transfers
    else:
        transfers_to_return = [
            transfer
            for transfer in transfers
            if transfer["from_user_id"] == uid or transfer["to_user_id"] == uid
        ]

    return JsonResponse(
        {"optimized": optimized, "transfers": transfers_to_return},
        safe=False,
        status=200,
    )
