"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("modules.products.urls")),
    path("api/cart/", include("modules.cart.urls")),
    path("api/accounts/", include("modules.accounts.urls")),
    path("api/orders/", include("modules.orders.urls")),
    path("api/shipment/", include("modules.shipment.urls")),
    path("api/checkout/", include("modules.checkout.urls")),
    path("api/reviews/", include("modules.reviews.urls")),
    path("api/search/", include("modules.search.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
