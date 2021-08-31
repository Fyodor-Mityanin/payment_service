from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns_v1 = [
    path('invoices/', views.InvoiceListCreateAPI.as_view()),
    path('invoices/<int:pk>/', views.InvoiceDetailPayAPI.as_view()),
    path('cards/', views.CardListCreateAPI.as_view()),
    path('cards/<int:pk>/', views.CardDetailDestroyAPI.as_view()),
    path('auth/users/me/', views.UserDetailAPI.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]


urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
    # path('v1/', include(v1_router.urls)),
]
