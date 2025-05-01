from django.urls import path
from .views import VectorDBView, HealthCheckView

urlpatterns = [
    path('vector/', VectorDBView.as_view(), name='vector'),
    path('health/', HealthCheckView.as_view(), name='health'),
] 