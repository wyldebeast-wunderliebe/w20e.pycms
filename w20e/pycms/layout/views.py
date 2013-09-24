from registry import ILayouts
from w20e.pycms.events import ContentChanged


class LayoutView(object):

    """ View that provides the layout change/set action"""

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def set_layout(self):

        layout_id = self.request.params['layout']

        layouts = self.request.registry.getUtility(ILayouts)

        layout = layouts.get_layout(layout_id)

        if layout:
            self.context.set_layout(layout)
            self.request.registry.notify(ContentChanged(self.context))

        return {"msg": "Layout has been set to %s" % layout_id, 
                "status": "success"}
