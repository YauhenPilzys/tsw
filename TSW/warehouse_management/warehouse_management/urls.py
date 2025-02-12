"""
URL configuration for warehouse_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from core.views import *
from django.views.decorators.csrf import csrf_exempt

# Регистрация маршрутов
router = DefaultRouter()
router.register(r'tsw', TSWViewSet, basename='tsw')
router.register(r'warehouses', WarehouseViewSet, basename='warehouses')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'ramps', RampViewSet, basename='ramps')
router.register(r'places', PlaceViewSet, basename='places')
router.register(r'type-places', TypePlaceViewSet, basename='type-places')
router.register(r'service-orders', ServiceOrderViewSet, basename='service-orders')
router.register(r'transfers', TransferViewSet, basename='transfers')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'parkings', ParkingViewSet, basename='parkings')
router.register(r'place-parks', PlaceParkViewSet, basename='place-parks')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'log-books', LogBookViewSet, basename='log-books')
router.register(r'notices', NoticeViewSet, basename='notices')
router.register(r'docs', DocViewSet, basename='doc')
router.register(r'document-files', DocumentFileViewSet, basename='document-file')
router.register(r'log-places', LogPlaceViewSet, basename='log-place')
router.register(r'recipients', RecipientViewSet, basename='recipient')
router.register(r'transports', TransportViewSet, basename='transport')
router.register(r'transport-notice', TransportNoticeViewSet, basename='transport-notice')
router.register(r'user-actions', UserActionLogViewSet, basename='user-action-log')
router.register(r'eclients', EClientViewSet, basename='eclient')






# Настройка схемы Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="TSW API",
        default_version='v1',
        description="Документация API для проекта TSW",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('pass/<int:logbook_id>/', generate_pass_pdf, name='generate_pass_pdf'),
    path('api/v1/directories/<str:directory_name>/', DirectoryView.as_view(), name='directory'),
    path('notices/<int:notice_id>/download_xml/', download_notice_xml, name='download_notice_xml'),
    path('send-xml/<int:pk>/', SendXMLFile.as_view(), name='send_xml'),
    path('check-status/<int:pk>/', CheckEClientStatus.as_view(), name='check-eclient-status'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('proxy/registration/<str:guid>/', get_registration_info, name='get_registration_info'),
    path('proxy/files/<str:guid>/', get_file_list, name='get_file_list'),
    # path('proxy/files/<int:id_reg>/', get_file_list, name='get_file_list'),
    path('proxy/file/<int:file_id>/', get_file, name='get_file'),


]

# Добавление URL-маршрутов для обслуживания статических файлов - чтобы картинки отображались, по ним создавались url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
