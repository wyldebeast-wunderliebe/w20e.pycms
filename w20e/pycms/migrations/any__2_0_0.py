from persistent.mapping import PersistentMapping
from repoze.catalog.query import Eq, Or
from w20e.pycms.layout.blocks.text import Text


def migrate(app):

    """ Set page._blocks to PersistentMapping. Also move page text to block """

    cat = app._catalog

    res = cat.query(Or(Eq('ctype', "page"), Eq('ctype', "site")), as_object=1)

    for obj in res:

        block = Text("maintext", text=obj.__data__['text'])

        if not hasattr(obj, "_blocks"):
            setattr(obj, "_blocks", PersistentMapping())

        obj.save_block("main", block.id, block)

    return True
