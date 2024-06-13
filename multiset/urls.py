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

api = NinjaAPI()
api.add_router("/settlements/", settlements_router)
api.add_router("/purchases/", purchases_router)
api.add_router("/groups/", groups_router)
api.add_router("/analytics/", analytics_router)
api.add_router("/optimization/", optimization_router)
api.add_router("/users/", users_router)


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
