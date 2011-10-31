from base import AdminView


class ImageView(object):


    def __init__(self, context, request):

        self.context = context
        self.request = request


    def __call__(self):

        # caching headers should not be set here hardcoded,
        # but it'll have to do for now..
        self.request.response.cache_expires(86400)
        self.request.response.cache_control.public = True
        return self.context.data


    def thumbnail(self):

        # caching headers should not be set here hardcoded,
        # but it'll have to do for now..
        self.request.response.cache_expires(86400)
        self.request.response.cache_control.public = True
        return self.context.thumbnail


class ImageAdminView(AdminView):

    pass
