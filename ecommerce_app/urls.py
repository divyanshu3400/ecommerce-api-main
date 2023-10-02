from django.urls import path
from django.conf.urls.static import static
from ecommerce_app import views
from ecommerce import settings

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('product_detail/<int:product_id>/<str:product_category_name>/', views.product_detail, name="product_detail"),
    path('dummy_product/', views.dummy_product, name="dummy_product"),
    path('cart/', views.shopping_cart, name="shopping-cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('register/', views.register, name="register"),
    path('validate_email/', views.validate_email, name="validate_email"),
    path('validate_username/', views.validate_username, name="validate_username"),
    path('search/', views.search_products, name="search_products"),
    path('send-otp/', views.send_otp_email, name='send-otp'),
    path('verify-otp/', views.login_view, name='verify-otp'),
    path('your-orders/', views.your_orders, name='your-orders'),
    path('user-profile/', views.user_profile, name='user-profile'),
    path('email-confirmation/<str:token>/', views.email_confirmation, name='email_confirmation'),
    path('logout/', views.logout_view, name='logout'),
    path('user-email-confirmation/', views.email_confirmation_view, name='user-email-confirmation'),
    path('your-account/', views.user_account, name='user-account'),
    path('change-password/', views.change_password, name='change-password'),
    path('my-wishlist/', views.my_wishlist, name='my-wishlist'),
    path('manage-address/', views.manage_address, name='manage_address'),
    path('user-login/', views.user_login, name='user-login'),
    path('delete-address/', views.delete_address, name="delete-user-address"),
    path('update-address', views.update_address, name="update-user-address"),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('get-states/', views.get_state, name='get_state'),
    path('address/edit/<int:address_id>/', views.manage_address, name='edit-address'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
