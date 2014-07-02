
"""
   Build common resources required by package widget(s)

.. note::
   We include `jquery_ui_js` as a resource used by elfinder_js
   (which in turn, adds `jquery_js`).  The base JqueryUIWidget
   adds `jquery_ui_css` so there's no requirement to add this.
"""

from tw2.jquery import base as jqbase
from tw2.jqplugins.ui import base as jquibase

from . import defaults

modname = 'tgextelfinder'

dict_img = dict(name=defaults._elfinder_name_,
                version=defaults._elfinder_version_,
                subdir="img"
                )

elfinder_images = jqbase.DirLink(
    modname=modname,
    filename=defaults._plugin_css_dirname_ % dict_img
    )

elfinder_css = jqbase.jQueryPluginCSSLink(
    resources=[elfinder_images], name=defaults._elfinder_name_,
    basename='%s.%s' % (defaults._elfinder_basename_, defaults._elfinder_debug_),
    version=defaults._elfinder_version_,
    modname = modname,
    )

elfinder_js = jqbase.jQueryPluginJSLink(
    resources = [jquibase.jquery_ui_js],
    name=defaults._elfinder_name_,
    basename='%s.%s' % (defaults._elfinder_basename_, defaults._elfinder_debug_),
    version=defaults._elfinder_version_,
    modname = modname,
    )

