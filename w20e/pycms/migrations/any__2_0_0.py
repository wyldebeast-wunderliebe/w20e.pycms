from persistent.mapping import PersistentMapping
from repoze.catalog.query import Eq
from w20e.pycms.layout.blocks.text import Text


def migrate(app):

    """ Set page._blocks to PersistentMapping. Also move page text to block """

    cat = app._catalog
    
    res = cat.query(Eq('ctype', "page"))

    for result in res[1]:
        obj = cat.get_object(result)

        block = Text("maintext", text=obj.__data__['text'])

        if not hasattr(obj, "_blocks"):
            setattr(obj, "_blocks", PersistentMapping())

        obj.save_block("main", block.id, block)

    return True
