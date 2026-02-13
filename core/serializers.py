from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from core.models import Address, Order, OrderItem, Product

User = get_user_model()


# =========================
# SIGNUP SERIALIZER
# =========================
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            # "company",
            # "gst_number",
            "password",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(
            email=validated_data["email"],
            username=validated_data["email"], 
            full_name=validated_data.get("full_name", ""),
            # company=validated_data.get("company", ""),
            # gst_number=validated_data.get("gst_number", ""),
        )

        user.set_password(password) 
        user.save()
        return user


# =========================
# SIGNIN SERIALIZER
# =========================
class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(
            username=email,  
            password=password
        )

        if not user:
            raise AuthenticationFailed("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        data["user"] = user
        return data



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "company",
            "gst_number",
            "user_id",
            "is_verified",
        )
        read_only_fields = ("email", "user_id", "is_verified")
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "category",
            "is_active",
        )

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = OrderItem
        fields = (
            "product_name",
            "quantity",
            "price",
        )
  
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "address_code",
            "address",
        )
        read_only_fields = ("address_code",)
class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=False)
    items = OrderItemInputSerializer(many=True)

    def validate(self, data):
        if not data["items"]:
            raise serializers.ValidationError("Order must contain items")
        return data
    
class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    gst_amount = serializers.DecimalField(
        source="tax_amount",
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "order_id",
            "status",
            "items",
            "total_amount",
            "gst_amount",
            "net_amount",
            "created_at",
        )

class DashboardStatsSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    active_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()
    total_amount = serializers.DecimalField(
        max_digits=14, decimal_places=2
    )
    recent_orders = serializers.ListField()