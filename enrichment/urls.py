from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ComercioViewSet, KeywordViewSet, EnrichmentAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'comercios', ComercioViewSet)
router.register(r'keywords', KeywordViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Bank Transactions",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="fenavillarroel"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(router.urls)),
    path('api/v1/enrichment/', EnrichmentAPIView.as_view(), name='enrichment'),
]
