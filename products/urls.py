from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .views import ProductsView, CartViews

router = routers.DefaultRouter()

router.register(r'products', ProductsView)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^cart/$', CartViews.as_view(), name='user_cart'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
