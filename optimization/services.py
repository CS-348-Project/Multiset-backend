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


def calculate_transfers(gid: int):
    """
        Calculates optimal transfers for a group
    Args:
        gid: the id of the group to calculate transfers for
    Returns:
        a list of dicts with keys: `from_id`, `to_id`, `amount` representing optimal transfers
    """

    # first, we need to check if the optimization flag is set
    flag = execute_query(
        Path("optimization/sql/get_optimization_flag.sql"),
        {
            "group_id": gid,
        },
        fetchone=True,
    )

    if not flag["optimize_payments"]:
        return JsonResponse({"status": "error, optimization flag not set"}, status=400)

    # then we get the balances of the group members
    balances = execute_query(
        Path("optimization/sql/get_group_balances.sql"),
        {
            "group_id": gid,
        },
        fetchall=True,
    )

    # and we solve the linear program
    solution = _solve_ilp(balances)

    if solution:
        return JsonResponse(solution, safe=False, status=200)

    return JsonResponse({"status": "error, no feasible solution found"}, status=500)


# input is list of dicts with keys: "user_id", "balance"
def _solve_ilp(input: list[dict["member_id":str, "balance":float]]):
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
                    from_id = input[i]["member_id"]
                    to_id = input[j]["member_id"]

                    output.append(
                        {
                            "from_id": from_id,
                            "to_id": to_id,
                            "amount": transfers[i][j].value(),
                        }
                    )

        return output

    # if there is no optimal solution we return None
    # this means there is an issue with an invariant in the database
    # (e.g. purchase splits not adding up to the purchase amount)
    # because there is always a feasible solution if everything adds up to 0
    return None
