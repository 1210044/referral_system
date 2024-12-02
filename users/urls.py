from rest_framework.routers import DefaultRouter
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from users.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title='Referral System API',
        default_version='v1',
        description='API for working with referrals',
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='api_docs'),
]
