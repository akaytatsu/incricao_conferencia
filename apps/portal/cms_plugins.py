from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    ColunaCMSPlugin, TituloPaginaCMSPlugin, TextoComponenteCMSPlugin, TituloComponenteCMSPlugin,
    TituloH3ComponenteCMSPlugin
)


@plugin_pool.register_plugin
class ColunaPlugin(CMSPluginBase):
    model = ColunaCMSPlugin
    module = "Alinhamento"
    name = "Coluna"
    allow_children = True
    render_template = "portal/plugins/align/coluna.html"


@plugin_pool.register_plugin
class LinhaPlugin(CMSPluginBase):
    module = "Alinhamento"
    name = "Linha"
    allow_children = True
    render_template = "portal/plugins/align/linha.html"


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


@plugin_pool.register_plugin
class BannerTituloPaginaPlugin(CMSPluginBase):
    model = TituloPaginaCMSPlugin
    module = "Banner"
    name = "Titulo da Página"
    render_template = "portal/plugins/banner_titulo_pagina.html"


@plugin_pool.register_plugin
class TituloPaginaPlugin(CMSPluginBase):
    model = TituloComponenteCMSPlugin
    module = "Componentes Página"
    name = "Titulo"
    render_template = "portal/plugins/componentes/titulo.html"


@plugin_pool.register_plugin
class LocalizacaoPaginaPlugin(CMSPluginBase):
    module = "Componentes Página"
    name = "Localização"
    render_template = "portal/plugins/componentes/localizacao.html"


@plugin_pool.register_plugin
class TextoPaginaPlugin(CMSPluginBase):
    model = TextoComponenteCMSPlugin
    module = "Componentes Página"
    name = "Texto"
    render_template = "portal/plugins/componentes/texto.html"


@plugin_pool.register_plugin
class TituloH3PaginaPlugin(CMSPluginBase):
    model = TituloH3ComponenteCMSPlugin
    module = "Componentes Página"
    name = "Titulo H3"
    render_template = "portal/plugins/componentes/titulo_h3.html"
