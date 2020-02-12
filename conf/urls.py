from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from apps.accounts.views import AccountViewSet
from apps.financeiro.views import ComprovantesViewSet, FinanceiroViewSet
from apps.inscricao.views import StartView
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

admin.site.site_header = "Sistema de Inscrição Igreja em Contagem"
admin.site.site_title = "Sistema de Inscrição Igreja em Contagem"
admin.site.index_title = "Sistema de Inscrição Igreja em Contagem"

urlpatterns = [
    path('', StartView.as_view(), name="start"),
    path('api/token/auth', obtain_jwt_token),
    # path('api/financeiro/', include('apps.financeiro.urls')),
    path('api/inscricao/', include('apps.data.urls')),
    path('api/comprovante/', ComprovantesViewSet.as_view()),
    path('admin/', admin.site.urls),
    path('<conferencia>/', include('apps.inscricao.urls')),
    path(r'favicon.ico',RedirectView.as_view(url='/static/ico/favicon.ico')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register(r'api/account', AccountViewSet, basename='api_account')
router.register(r'api/financeiro', FinanceiroViewSet, basename='api_financeiro')
# router.register(r'api/comprovante', , basename='api_comprovantes')

urlpatterns = urlpatterns + router.urls

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
