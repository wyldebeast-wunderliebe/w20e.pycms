from pyramid.renderers import JSON
from ZODB.blob import Blob

def register_json_adapters(config):
    """ register custom JSON serializers """

    json_renderer = JSON()

    def blob_adapter(obj, request):
        return obj.open('r').read()

    json_renderer.add_adapter(Blob, blob_adapter)

    config.add_renderer('json', json_renderer)

