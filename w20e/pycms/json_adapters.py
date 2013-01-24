from pyramid.renderers import JSON
from ZODB.blob import Blob
from datetime import datetime
from BTrees.OOBTree import OOBTree

def register_json_adapters(config):
    """ register custom JSON serializers """

    json_renderer = JSON()

    def blob_adapter(obj, request):
        return obj.open('r').read()

    def date_adapter(obj, request):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj

    def oobtree_adapter(obj, request):
        return dict([(k,v) for k,v in obj.items()])

    json_renderer.add_adapter(Blob, blob_adapter)
    json_renderer.add_adapter(datetime, date_adapter)
    json_renderer.add_adapter(OOBTree, oobtree_adapter)

    config.add_renderer('json', json_renderer)

