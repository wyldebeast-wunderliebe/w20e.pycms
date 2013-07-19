from registry import ILayouts
from w20e.hitman.events import ContentChanged


class LayoutView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

    def set_layout(self):

        layout_id = self.request.params['layout']

        layouts = self.request.registry.getUtility(ILayouts)

        layout = layouts.get_layout(layout_id)

        if layout:
            self.context.set_layout(layout.interface)
            self.request.registry.notify(ContentChanged(self.context))

        return {"msg": "Layout has been set to %s" % layout_id, 
                "status": "success"}
