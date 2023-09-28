from django.urls import path
from django.conf.urls.static import static
from ecommerce_api.views import *

urlpatterns = [


   #   APIs

    path('verify-email-otp/', EmailOTPVerificationView.as_view(), name='verify-email-otp'),
    path('navbar_list/', NavbarCatList.as_view(), name='navbar-list'),
    path('send-email-otp/', SendOTPView.as_view(), name='send-otp'),
    path('parent-categories-list/', ParentCategoryList.as_view(), name='parent-categories-list'),
    path('child-categories-list/', ChildCategoryList.as_view(), name='child-categories-list'),
    path('cat-product-list/', CategoryProductList.as_view(), name='product-list'),
    path('brand-list/', BrandList.as_view(), name='brand-list'),


    path('update-profile/', update_profile_data, name='update_profile'),
    path('all-product-list/', AllProductList.as_view(), name='all-product-list'),
    path('product_details/', ProductDetailApi.as_view(), name='product_details'),
    path('user-profile/', UserProfileAPI.as_view(), name='api_user_profile'),

    # APIs to perform(CRUD) operations on User Cart
    path('add-to-cart/', AddToCart.as_view(), name='api_cart_add'),
    path('cart-item-list/', CartDetailView.as_view(), name='cart-item-list'),
    path('cart-item-delete/', RemoveProductFromCartAPIView.as_view(), name='cart-item-delete'),
    path('cart-items/increase/', IncreaseCartItemQuantity.as_view(), name='increase-cart-item-quantity'),
    path('cart-items/decrease/', DecreaseCartItemQuantity.as_view(), name='decrease-cart-item-quantity'),


    # APIs to perform(CRUD) operations on Wishlist
    path('add-to-wishlist/', AddToWishlistAPIView.as_view(), name='add-to-wishlist'),
    path('remove-from-wishlist/', RemoveProductFromWishlistAPIView.as_view(), name='remove-from-wishlist'),
    path('wishlist-items/', WishlistItemListByUserView.as_view(), name='wishlist-item-list'),
    
    
    # APIs to perform(CRUD) operations on Address
    path('add-address/', AddAddressToProfileAPIView.as_view(), name='add-address'),
    path('update-address/', UpdateAddressAPIView.as_view(), name='update-address'),
    path('delete-address/', DeleteAddressAPIView.as_view(), name='delete-address'),


    # place order 
    path('place-order/', PlaceOrderView.as_view(), name="place-order"),
    path('orders/update_status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('user-orders-detail/', GetUserOrdersView.as_view(), name='user-orders-detail'),


    # user feedback
    path('product-feedback/', CreateFeedbackView.as_view(), name='create-feedback'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
