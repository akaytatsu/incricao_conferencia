from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

admin.site.site_header = "Sistema de Inscrição Igreja em Contagem"
admin.site.site_title = "Sistema de Inscrição Igreja em Contagem"
admin.site.index_title = "Sistema de Inscrição Igreja em Contagem"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<conferencia>/', include('apps.inscricao.urls')),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
# router.register(r'api', DataViewSet, basename='api')

urlpatterns = urlpatterns + router.urls