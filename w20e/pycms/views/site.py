from .base import AdminView
from ..interfaces import IMailer


class SiteView(AdminView):

    """ Site admin view """

    def __init__(self, context, request):

        AdminView.__init__(self, context, request)


    def pack_database(self):
        """ pack the database """

        db = self.db

        old_size = db.getSize()
        result = db.pack() or "Database has been packed succesfully"
        new_size = db.getSize()
        return "pack result: {0} \nOld Data.fs size: {1}\n" \
                "New Data.fs size: {2}\n" \
                "check disk to see size of blobdir".format(
                        result, old_size, new_size)

    @property
    def db(self):

        from pyramid_zodbconn import get_connection
        conn = get_connection(self.request)
        db = conn.db()

        return db

    def catalog_entries(self):

        return [{'id': obj[0], 'path': obj[1]} for obj in \
                self.context._catalog.list_objects()]

    def robots_txt(self):

        self.request.response.content_type = 'text/plain'

        return {}
