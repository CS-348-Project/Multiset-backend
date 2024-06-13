from django.contrib import admin
from django.urls import path, include
from django.db import connection
from django.http import JsonResponse
from ninja import NinjaAPI
from settlements.api import router as settlements_router
from purchases.api import router as purchases_router
from groups.api import router as groups_router
from analytics.api import router as analytics_router
from optimization.api import router as optimization_router
from users.api import router as users_router
from grocery_lists.api import router as grocery_lists_router
from auth.api import router as auth_router
from ninja.security import HttpBearer
from auth.services import get_associated_user_id


class GlobalAuth(HttpBearer):
    # To get the user id from within an endpoint you can use request.auth
    def authenticate(self, request, token):
        user_id = get_associated_user_id(token)
        if not user_id:
            return None
        return user_id


api = NinjaAPI(auth=GlobalAuth())
api.add_router("/settlements/", settlements_router)
api.add_router("/purchases/", purchases_router)
api.add_router("/groups/", groups_router)
api.add_router("/analytics/", analytics_router)
api.add_router("/optimization/", optimization_router)
api.add_router("/users/", users_router)
api.add_router("/grocery-lists/", grocery_lists_router)
api.add_router("/auth/", auth_router)

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.get("/")
def home(request):
    return {"message": "Hello, world!"}


@api.get("/users")
def get_users(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()
    return JsonResponse(rows, safe=False)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("accounts/", include("allauth.urls")),
]
