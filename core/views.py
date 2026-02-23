from decimal import Decimal
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from core.auth.keycloak_auth import KeycloakAuthentication
from core.models import User, Product, Address, Order, OrderItem
from core.serializers import (
    SignupSerializer,
    ProfileSerializer,
    ProductSerializer,
    AddressSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
)
from core.utils.keycloak import create_keycloak_user, get_keycloak_token

GST_RATE = Decimal("0.18")


# =========================
# AUTH
# =========================
@method_decorator(csrf_exempt, name="dispatch")
class SignupAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        full_name = serializer.validated_data.get("full_name", "")

        # 1️⃣ Create user in Keycloak FIRST
        create_keycloak_user(
            email=email,
            password=password,
            full_name=full_name,
        )

        # 2️⃣ Create user in DB ONLY if Keycloak succeeds
        user = serializer.save()

        return Response(
            {"message": "Account created successfully"},
            status=status.HTTP_201_CREATED,
        )




@method_decorator(csrf_exempt, name="dispatch")
class SigninAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password are required")

        # 1️⃣ Authenticate with Keycloak (ONLY ONCE)
        try:
            token_data = get_keycloak_token(email, password)
        except Exception as e:
            print("KEYCLOAK ERROR:", e)
            raise AuthenticationFailed("Invalid email or password")

        # 2️⃣ Sync user locally
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": "",
                "company": "",
                "gst_number": "",
                "is_verified": True,
            },
        )

        # 3️⃣ Return response
        return Response(
            {
                "access": token_data["access_token"],
                "refresh": token_data["refresh_token"],
                "expires_in": token_data.get("expires_in"),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "company": user.company,
                    "gst_number": user.gst_number,
                    "user_id": user.user_id,
                    "is_verified": user.is_verified,
                },
            },
            status=status.HTTP_200_OK,
        )





class ProfileDetailAPI(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# =========================
# PRODUCTS
# =========================
class ProductListCreateAPI(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


# =========================
# ADDRESSES
# =========================
class AddressListCreateAPI(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


# =========================
# ORDERS
# =========================
class OrderListCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        return OrderCreateSerializer if self.request.method == "POST" else OrderListSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.create(
            user=request.user,
            address=Address.objects.filter(
                id=serializer.validated_data.get("address_id"),
                user=request.user
            ).first()
        )

        total_amount = Decimal("0.00")
        snapshot = {}

        for item in serializer.validated_data["items"]:
            product = Product.objects.get(id=item["product_id"])
            qty = item["quantity"]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=product.price,
            )

            total = product.price * qty
            total_amount += total

            snapshot[product.name] = {
                "qty": qty,
                "price": float(product.price),
                "total": float(total),
            }

        order.total_amount = total_amount
        order.tax_amount = total_amount * GST_RATE
        order.items_snapshot = snapshot
        order.save()

        return Response(
            {
                "order_id": order.order_id,
                "net_amount": order.net_amount,
                "gst": float(order.tax_amount),
            },
            status=status.HTTP_201_CREATED,
        )


# =========================
# DASHBOARD
# =========================

class DashboardAPI(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        print("IS AUTH:", request.user.is_authenticated)

        orders = Order.objects.filter(user=request.user)

        return Response({
            "total_orders": orders.count(),
            "active_orders": orders.filter(status="active").count(),
            "completed_orders": orders.filter(status="completed").count(),
            "cancelled_orders": orders.filter(status="cancelled").count(),
            "total_amount": orders.aggregate(Sum("net_amount"))["net_amount__sum"] or 0,
            "recent_orders": OrderListSerializer(
                orders.order_by("-created_at")[:5], many=True
            ).data,
        })
class DashboardAPI(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        print("IS AUTH:", request.user.is_authenticated)

        orders = Order.objects.filter(user=request.user)

        return Response({
            "total_orders": orders.count(),
            "active_orders": orders.filter(status="active").count(),
            "completed_orders": orders.filter(status="completed").count(),
            "cancelled_orders": orders.filter(status="cancelled").count(),
            "total_amount": orders.aggregate(Sum("net_amount"))["net_amount__sum"] or 0,
            "recent_orders": OrderListSerializer(
                orders.order_by("-created_at")[:5], many=True
            ).data,
        })
class DashboardAPI(APIView):
    authentication_classes = [KeycloakAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        print("IS AUTH:", request.user.is_authenticated)

        orders = Order.objects.filter(user=request.user)

        return Response({
            "total_orders": orders.count(),
            "active_orders": orders.filter(status="active").count(),
            "completed_orders": orders.filter(status="completed").count(),
            "cancelled_orders": orders.filter(status="cancelled").count(),
            "total_amount": orders.aggregate(Sum("net_amount"))["net_amount__sum"] or 0,
            "recent_orders": OrderListSerializer(
                orders.order_by("-created_at")[:5], many=True
            ).data,
        })
