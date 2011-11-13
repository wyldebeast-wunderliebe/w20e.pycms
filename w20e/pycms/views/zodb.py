from base import AdminView
from eye.views import _build_tree
from eye.views import as_json as base_as_json
import pprint
from eye.models import Node


class ZODBView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)
        self.node = Node(context)


    def as_tree(self):

        tree = _build_tree(self.node, 2, 1)
        if type(tree) == dict:
            tree = [tree]

        return tree


    def as_json(self):

        info = {
            'info': cgi.escape(pprint.pformat(self.node.context)),
            }

        return info
