from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecommerce_app.urls')),
    path('api/', include('ecommerce_api.urls'))
]

admin.site.site_title = "E-Commerce Admin"
admin.site.index_title = "E-Commerce Admin Panel"
