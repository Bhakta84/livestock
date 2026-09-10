from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken


def api_root(request):
    return JsonResponse({
        "message": "BLDCL API",
        "endpoints": {
            "login": "/api/auth/login/",
            "register": "/api/auth/register/",
            "token": "/api/auth/token/",
            "refresh": "/api/auth/token/refresh/",
            "tenders": "/api/tenders/",
            "bids": "/api/bids/",
        },
    })


class AuthUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "name", "role"]

    def get_name(self, obj):
        return (obj.get_full_name() or obj.username or obj.email).strip() or obj.email

    def get_role(self, obj):
        if obj.is_staff or obj.is_superuser:
            return "Admin"
        if obj.groups.filter(name="Bidder").exists():
            return "Bidder"
        if obj.groups.filter(name="Procurement Officer").exists():
            return "Procurement Officer"
        if obj.groups.filter(name="Evaluator").exists():
            return "Evaluator"
        if obj.groups.filter(name="Approving Authority").exists():
            return "Approving Authority"
        return "Bidder"

class AuthTokenMixin:
    def token_response(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "user": AuthUserSerializer(user).data,
        }

class LoginView(AuthTokenMixin, APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = (request.data.get("email") or "").strip()
        password = request.data.get("password") or ""
        if not email or not password:
            return Response({"detail": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first() or User.objects.filter(username__iexact=email).first()
        if user is None or not user.check_password(password):
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(self.token_response(user))

class RegisterView(AuthTokenMixin, APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        name = (request.data.get("name") or "").strip()
        email = (request.data.get("email") or "").strip()
        password = request.data.get("password") or ""
        if not name or not email or not password:
            return Response({"detail": "Name, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            return Response({"detail": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        bidder_group, _ = Group.objects.get_or_create(name="Bidder")
        user.groups.add(bidder_group)
        return Response(self.token_response(user), status=status.HTTP_201_CREATED)

urlpatterns=[
 path("admin/",admin.site.urls),
 path("api/", api_root, name="api_root"),
 path("api/auth/login/",LoginView.as_view(),name="login"),
 path("api/auth/register/",RegisterView.as_view(),name="register"),
 path("api/auth/token/",TokenObtainPairView.as_view(),name="token"),
 path("api/auth/token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
 path("api/tenders/",include("tenders.urls")),
 path("api/bids/",include("bids.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
