from rest_framework import serializers
from ecommerce_app.models import *


# class FeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else None 

    def get_product_name(self, obj):
        return obj.product.product_name if obj.product else None 

    class Meta:
        model = Feedback
        fields = ['id', 'rating', 'comment', 'created_at', 'user_name', 'product_name']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ProductSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizes
        fields = ['id','product_size']




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            image_url = request.build_absolute_uri(instance.image.url)
        else:
            image_url = None

        return {'image': image_url, }




class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set') 
    class Meta:
        model = Product
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id','brand_name','brand_image','status']


class ElectronicProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    images = ProductImageSerializer(many=True, source='productimage_set')
    colors = ColorSerializer(many=True)

    class Meta:
        model = ElectronicProduct
        fields = '__all__'


class ProductIdSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class OTPTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPToken
        fields = '__all__'


class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmation
        fields = '__all__'


class NavBarCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarCat
        fields = '__all__'


class ParentCategorySerializer(serializers.ModelSerializer):
    pcat_logos_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = ParentCategory
        fields = '__all__'

    def get_pcat_logos_absolute_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.pcat_logos)
        else:
            return obj.pcat_logos


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildCategory
        fields = '__all__'


class FashionProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    images = ProductImageSerializer(many=True, source='productimage_set')
    colors = ColorSerializer(many=True)
    sizes = ProductSizesSerializer(many=True)

    class Meta:
        model = FashionProduct
        fields = '__all__'


class ParentCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = "__all__"


class ProfileUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    name = serializers.CharField(max_length=200, required=True)
    email = serializers.CharField(max_length=200, required=True)
    age = serializers.IntegerField(required=True)
    profile_image = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)


class BookProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set')
    feedback = FeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = BookProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set')
    class Meta:
        model = Product
        fields = '__all__'


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


class CartViewSerializer(serializers.ModelSerializer):
    cart_item_id = serializers.IntegerField(source='id')
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('cart_item_id', 'product_id', 'category_name', 'quantity', 'subtotal')

    def get_category_name(self, obj):
        if obj.product:
            return obj.product.category_name
        return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserProfileIdSerializer(serializers.Serializer):
    user_profile_id = serializers.IntegerField()


class AddToWishlistSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()


class WishlistSerializer(serializers.Serializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'state', 'city', 'postal_code', 'country', 'latitude',
                  'longitude']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity', 'subtotal']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    shipping_address = AddressSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
