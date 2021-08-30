from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register(
    'cards',
    views.CardsViewSet,
    basename='CardsAPI',
)

urlpatterns_v1 = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] 


urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
    path('v1/', include(v1_router.urls)),
]
