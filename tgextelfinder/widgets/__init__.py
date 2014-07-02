
import tw2.core as twc

from tw2.jqplugins.ui.base import JQueryUIWidget
from . import base

class ElfinderWidget(JQueryUIWidget):

    attrs = {'style': 'margin:10px 80px;'}

    resources = [base.elfinder_js, base.elfinder_css]

    # looks like it's using the template in your tw2.jqplugins version
    template = 'mako:tw2.jqplugins.elfinder.templates.widget'

    options = twc.Param(
            '(dict) A dict of options to pass to the widget', default={})

