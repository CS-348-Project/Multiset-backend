from ninja import Router
from .services import handle_google_login
from .serializers import AuthSerializer

router = Router()

@router.get("/")  
def google_login(request):
    auth_serializer = AuthSerializer(data=request.GET)
    auth_serializer.is_valid(raise_exception=True)
    
    validated_data = auth_serializer.validated_data
    return handle_google_login(request, validated_data)
