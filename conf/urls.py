from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token

from apps.accounts.views import AccountViewSet
from apps.financeiro.views import FinanceiroViewSet, ComprovantesViewSet
from apps.relatorios.views import gen_report_cracha

admin.site.site_header = "Sistema Unificado Igreja em Contagem"
admin.site.site_title = "Sistema Unificado Igreja em Contagem"
admin.site.index_title = "Sistema Unificado Igreja em Contagem"

urlpatterns = [
    path('api/token/auth', obtain_jwt_token),
    path('api/inscricao/', include('apps.data.urls')),
    path('api/comprovante/', ComprovantesViewSet.as_view()),
    path('api/comprovante/<int:pk>/', ComprovantesViewSet.as_view()),
    path('gera_planilha_cracha/<int:pk>', gen_report_cracha),
    path('admin/', admin.site.urls),
    path('sermons/', include('apps.pregacoes.urls')),
    path('<conferencia>/', include('apps.inscricao.urls')),
    path(r'favicon.ico', RedirectView.as_view(url='/static/ico/favicon.ico')),
    path('', include('cms.urls')),
]

router = DefaultRouter()
router.register(r'api/account', AccountViewSet, basename='api_account')
router.register(r'api/financeiro', FinanceiroViewSet, basename='api_financeiro')

urlpatterns = urlpatterns + router.urls

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
