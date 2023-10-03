from rest_framework import generics, status
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.decorators import api_view
import base64
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from ecommerce_api.serializers import *
from django.shortcuts import render, get_object_or_404
import random
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from ecommerce_app.models import *
from ecommerce_app.model_serialize_mapping.mapping import PRODUCT_TYPE_MAPPING
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


def email_confirmation_view(request):
    logo = Logo.objects.all()
    return render(request, 'ecommerce_app/email_confirmation.html', {'logo': logo})


def email_confirmation(request, token):
    confirmation_email = get_object_or_404(EmailConfirmation, token=token)
    user = confirmation_email.user
    user.is_active = True
    user.save()
    confirmation_email.delete()
    messages.success(request, 'Thanks for verifying your account. Now you can login.')
    return render(request, 'ecommerce_app/email_confirmation.html')


def generate_otp():
    digits = "0123456789"
    return ''.join(random.choice(digits) for _ in range(6))


def create_otp(user):
    otp_token = OTPToken.objects.create(user=user, token=generate_otp())
    return otp_token


class SendOTPView(APIView):
    def post(self, request):
        if request.method == 'POST':
            email = request.data.get('email')
            user = ""
            if email:
                try:
                    user = User.objects.get(username=email, email=email)
                except:
                    if User.objects.filter(email=email):
                        return JsonResponse({'message': "User already exists!!!"})
                    else:
                        user = User.objects.create(username=email, email=email)
                otp = create_otp(user)
                subject = 'Educart OTP verification'
                to_email = [email]
                logo = Logo.objects.all()
                html_content = render_to_string(
                    'ecommerce_app/otp_email_template.html', {'otp': otp, 'for': 'login', 'logo': logo})
                email = EmailMessage(subject, html_content,
                                     settings.EMAIL_HOST_USER, to_email)
                email.content_subtype = 'html'
                email.send()
                return JsonResponse({'message': "OTP sent successfully!!"})
            else:
                return JsonResponse({'message': 'Email is required'}, status=400)
        else:
            return JsonResponse({'response': 'error while sending the OTP'})


class EmailOTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_token = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        try:
            if verify_otp(user, otp_token):
                user.is_active = True
                user.save()
                
                token, created = Token.objects.get_or_create(user=user)
                data ={'message': 'Logged in successfully', 
                       'token': token.key,
                       "user_id":user.id
                       }
                return Response(data, status=status.HTTP_200_OK)
            else:
                OTPToken.objects.all().delete()
                return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except OTPToken.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def verify_otp(user, otp):
    otp_token = OTPToken.objects.filter(
        user=user, token=otp).order_by('-created_at').last()
    if otp_token:
        time_difference = timezone.now() - otp_token.created_at
        # OTP expires after 5 minutes (300 seconds)
        if time_difference.seconds < 300:
            otp_token.delete()
            return True
    return False


class NavbarCatList(generics.ListAPIView):
    queryset = NavbarCat.objects.all()
    serializer_class = NavBarCatSerializer


class AllProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ParentCategoryList(APIView):
    serializer_class = ParentCategorySerializer

    def post(self, request):
        nav_id = request.data.get('nav_id')
        queryset = ParentCategory.objects.filter(nav=nav_id)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChildCategoryList(APIView):
    serializer_class = ChildCategorySerializer

    def post(self, request):
        pcat = request.data.get('pcat_id')
        queryset = ChildCategory.objects.filter(pcat=pcat)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryProductList(APIView):
    serializer_Class = ProductSerializer

    def post(self, request):
        category = request.data.get('child_cat_id')
        queryset = FashionProduct.objects.filter(category=category)
        serializer = self.serializer_Class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandList(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_data(request):
    try:
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get("user_id")
            profile = Profile.objects.get(user=user_id)

            if profile.profile_image:
                existing_image_path = profile.profile_image.path
                default_storage.delete(existing_image_path)

            if 'phone_number' in serializer.validated_data:
                profile.phone_number = serializer.validated_data['phone_number']
            if 'age' in serializer.validated_data:
                profile.age = serializer.validated_data['age']
            if 'profile_image' in serializer.validated_data:
                profile_image_data = serializer.validated_data['profile_image']
                gender = serializer.validated_data['gender']
                email = serializer.validated_data['email']
                name = serializer.validated_data['name']
                try:
                    user = User.objects.get(email=email)
                    if user.id != user_id:
                        return Response({"message": "Email is already associated with another user."},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user.first_name = name
                        user.save()

                except User.DoesNotExist:
                    user = User.objects.get(pk=user_id)
                    user.username = email
                    user.email = email
                    user.first_name = name
                    user.save()

                try:
                    image_data = base64.b64decode(profile_image_data)
                    image = Image.open(BytesIO(image_data))
                    profile.profile_image.save("Img_" + name + ".png", ContentFile(image_data))
                    profile.save()
                except Exception as e:
                    print(f"Error decoding/processing image data: {e}")

                profile.gender = gender
                profile.save()

            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


# class ProductDetailApi(APIView):
#     def post(self, request):
#         product_id = request.data.get('product_id')
#         category_name = request.data.get('category_name')

#         if category_name not in PRODUCT_TYPE_MAPPING:
#             return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)

#         product_info = PRODUCT_TYPE_MAPPING[category_name]
#         model = product_info['model']
#         serializer_class = product_info['serializer']

#         try:
#             product = model.objects.get(pk=product_id)
#         except model.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = serializer_class(product, context={'request': request})
#         return Response(serializer.data)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProductDetailApi(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        category_name = request.data.get('category_name')

        if category_name not in PRODUCT_TYPE_MAPPING:
            return Response({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)

        product_info = PRODUCT_TYPE_MAPPING[category_name]
        model = product_info['model']
        serializer_class = product_info['serializer']

        try:
            product = model.objects.get(pk=product_id)
        except model.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        feedback = Feedback.objects.filter(product=product_id)
        
        product_serializer = serializer_class(product, context={'request': request})
        feedback_serializer = FeedbackSerializer(feedback, many=True)
        
        data = product_serializer.data
        data['feedback'] = feedback_serializer.data

        return Response(data)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UserProfileAPI(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        user_serializer = UserSerializer(user)
        profile_serializer = ProfileSerializer(profile, context={'request': request})

        response_data = {
            "user_data": {
                "user_id": user_serializer.data["id"],
                "is_superuser": user_serializer.data["is_superuser"],
                "username": user_serializer.data["username"],
                "name": user_serializer.data["first_name"],
                "email": user_serializer.data["email"],
                "is_staff": user_serializer.data["is_staff"],
                "is_active": user_serializer.data["is_active"],
                "date_joined": user_serializer.data["date_joined"],
                "phone_number": profile_serializer.data["phone_number"],
                "age": profile_serializer.data["age"],
                "gender": profile_serializer.data["gender"],
                "profile_image": request.build_absolute_uri(profile_serializer.data["profile_image"]),
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddToCart(APIView):
    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        print(request.data.get('user_id'))
        if serializer.is_valid():
            user = User.objects.get(pk=request.data.get('user_id'))
            cart, created = Cart.objects.get_or_create(user=user)
            print(cart)
            cart_item = CartItem(
                cart=cart,
                product=serializer.validated_data['product'],
                quantity=serializer.validated_data['quantity']
            )
            cart_item.save()
            return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RemoveProductFromCartAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        cart_item_id = request.data.get('cart_item_id')
        try:
            user = User.objects.get(pk=user_id)
            cart = Cart.objects.get(user=user)
            print(user)
            cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
            print(cart_item)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"message": "Product removed from the Cart successfully."}, status=status.HTTP_204_NO_CONTENT)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CartDetailView(APIView):
    def get(self, request):
        user_id = request.data.get('user_id')
        try:
            cart = Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return Response({"message":"No Items in cart"},status=status.HTTP_404_NOT_FOUND)
        cart_items = cart.cartitem_set.all()
        serializer = CartViewSerializer(cart_items, many=True)
        total_price = cart.grand_total_price()
        response_data = {
            'cart_detail': serializer.data,
            'total_price': total_price
        }
        return Response(response_data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddToWishlistAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddToWishlistSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            product_id = serializer.validated_data['product_id']
            try:
                user = User.objects.get(id=user_id)
                product = Product.objects.get(product_id=product_id)
            except User.DoesNotExist:
                return Response({"message": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            except Product.DoesNotExist:
                return Response({"message": "Product does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            existing_wishlist_item = WishlistItem.objects.filter(user=user, product=product)
            if existing_wishlist_item.exists():
                return Response({"message": "Product is already in the wishlist."}, status=status.HTTP_200_OK)
            wishlist_item = WishlistItem(user=user, product=product)
            wishlist_item.save()
            return Response({"message": "Product added to the wishlist successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RemoveProductFromWishlistAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        try:
            user = User.objects.get(pk=user_id)
            wishlist_item = WishlistItem.objects.get(user=user, product=product_id)
        except WishlistItem.DoesNotExist:
            return Response({"error": "Wishlist item not found."}, status=status.HTTP_404_NOT_FOUND)
        wishlist_item.delete()
        return Response({"message": "Product removed from the wishlist successfully."},status=status.HTTP_204_NO_CONTENT)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class WishlistItemListByUserView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        user_id = self.request.data.get('user_id')
        user = User.objects.get(pk=user_id)
        wishlist_items = WishlistItem.objects.filter(user=user)
        products = [item.product for item in wishlist_items]
        return products

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AddAddressToProfileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(pk=request.data.get('user_id'))
            user_profile = Profile.objects.get(user=user)
            address = serializer.save(profile=user_profile)
            return Response(AddressSerializer(address).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UpdateAddressAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        address_id = request.data.get('address_id')
        try:
            user = User.objects.get(pk=user_id)
            user_profile = Profile.objects.get(user=user)
            address = Address.objects.get(profile=user_profile, id=address_id)
        except Address.DoesNotExist:
            return Response({"message": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateAddressSerializer(instance=address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DeleteAddressAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        address_id = request.data.get('address_id')
        try:
            user = User.objects.get(pk=user_id)
            user_profile = Profile.objects.get(user=user)
            address = Address.objects.get(profile=user_profile, id=address_id)
        except Address.DoesNotExist:
            return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response({"message": "Address deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class IncreaseCartItemQuantity(APIView):
    def post(self, request):
        cart_item_id = request.data.get("cart_item_id")
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        product = cart_item.product
        if not product:
            return Response({'error': 'Associated product not found'}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.quantity + 1 <= product.units_in_stock:
            cart_item.quantity += 1
            cart_item.save()
            return Response({'quantity': cart_item.quantity})
        else:
            return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DecreaseCartItemQuantity(APIView):
    def post(self, request):
        cart_item_id = request.data.get("cart_item_id")
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            return Response({'error': 'Quantity cannot be less than 1'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'quantity': cart_item.quantity})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class PlaceOrderView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        cart_data_list = request.data.get("cart_detail")
        total_price = request.data.get('total_price')
        address_id = request.data.get('address_id')
        try:
            user = User.objects.get(pk=user_id)
            profile = Profile.objects.get(user=user)
            shipping_address = Address.objects.get(profile=profile, id=address_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        order_data = {
            "user": user,
            "total_price": total_price,
            "status": "pending",
            "shipping_address": shipping_address,
        }
        order = Order.objects.create(**order_data)

        for product_item in cart_data_list:
            product_id = product_item.get("product_id")
            quantity = product_item.get("quantity")
            sub_total = product_item.get("subtotal")

            try:
                product = Product.objects.get(product_id=product_id)
            except Product.DoesNotExist:
                return Response({"message": f"Product with ID {product_id} not found"},
                                status=status.HTTP_404_NOT_FOUND)

            order_item_data = {
                "order": order,
                "product": product,
                "quantity": quantity,
                "sub_total": sub_total,
                "created_at": timezone.now(),
            }
            OrderItem.objects.create(**order_item_data)
        order.save()
        cart = Cart.objects.get(user=user)
        cart.clear_cart()
        return Response({"message": "Order placed successfully"})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class UpdateOrderStatusView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        order_id = request.data.get('order_id')
        new_status = request.data.get("status")
        try:
            user = User.objects.get(pk=user_id)
            order = Order.objects.get(user=user, id=order_id)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if new_status not in [choice[0] for choice in ORDER_STATUS_CHOICES]:
            return Response({"message": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    
        if new_status == 'cancelled' and order.status == 'cancelled':
            return Response({"message": "Order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.update_status(new_status)
        
        if new_status == 'cancelled':
            order.cancel_order()
        else:
            order.place_order()
        
        return Response({"message": "Order status updated successfully"})

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class GetUserOrdersView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        user = User.objects.get(pk=user_id)
        orders = Order.objects.filter(user=user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CreateFeedbackView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment')
        feedback = Feedback.objects.filter(product=product_id, user=user_id).first()
        if feedback:
            feedback.rating = rating
            feedback.comment = comment
            feedback.save()
            feedback_serializer = FeedbackSerializer(feedback)
            return Response(feedback_serializer.data, status=status.HTTP_200_OK)
        else:
            feedback_data = {
                'product': product_id,
                'user': user_id,
                'rating': rating,
                'comment': comment,
                'created_at': timezone.now(),
            }
            feedback_serializer = FeedbackSerializer(data=feedback_data)

            if feedback_serializer.is_valid():
                feedback_serializer.save()
                return Response(feedback_serializer.data, status=status.HTTP_201_CREATED)
            return Response(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):

    user_id = request.data.get("user_id")
    user = User.objects.get(id=user_id)
    token, created = Token.objects.get_or_create(user=user)
    token.delete()

    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
