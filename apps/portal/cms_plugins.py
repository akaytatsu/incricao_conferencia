from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import ColunaCMSPlugin


@plugin_pool.register_plugin
class ColunaPlugin(CMSPluginBase):
    model = ColunaCMSPlugin
    module = "Coluna"
    name = "Coluna"
    allow_children = True
    render_template = "portal/plugins/coluna.html"


@plugin_pool.register_plugin
class PregracaoRecentePlugin(CMSPluginBase):
    module = "Pregações"
    name = "Pregação Recente"
    render_template = "portal/plugins/pregacao_recente.html"


@plugin_pool.register_plugin
class EventosProximosPlugin(CMSPluginBase):
    module = "Eventos"
    name = "Proximos Eventos"
    render_template = "portal/plugins/eventos_proximos.html"


@plugin_pool.register_plugin
class BannerProximoEventoPlugin(CMSPluginBase):
    module = "Banner"
    name = "Proximo Evento"
    render_template = "portal/plugins/banner_proximo_evento.html"


@plugin_pool.register_plugin
class BannerCarrouselPlugin(CMSPluginBase):
    module = "Banner"
    name = "Carrousel Banner"
    render_template = "portal/plugins/banner_carrousel.html"


@plugin_pool.register_plugin
class BannerCarrouselGigantePlugin(CMSPluginBase):
    module = "Banner"
    name = "Carrousel Banner Gigante"
    render_template = "portal/plugins/banner_carrousel_gigante.html"


@plugin_pool.register_plugin
class BannerUnicoPlugin(CMSPluginBase):
    module = "Banner"
    name = "Banner Unico"
    render_template = "portal/plugins/banner_unico.html"
