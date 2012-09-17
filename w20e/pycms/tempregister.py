from logging import getLogger
import datetime
from interfaces import ITemporaryObject
from BTrees.OOBTree import OOBTree
from w20e.hitman.utils import path_to_object, object_to_path

LOGGER = getLogger("w20e.pycms")


def init(event):

    """ Set up tempregister for site. """

    app = event.app_root

    # how long before we cleanup a temporary object (seconds)?
    timeout = event.registry.settings.get("pycms.tempregister.timout", 86400)

    if not hasattr(app, "_tempregister"):
        app._tempregister = TempRegister(timeout)
        app._tempregister.__parent__ = app
        app._tempregister.__name__ = "TempRegister"
        app._p_changed = 1

    if timeout != app._tempregister._timeout:
        app._tempregister._timeout = timeout
        app._p_changed = 1

# event handlers
#
def objectFinalized(event):

    LOGGER.debug("Finalized temp object %s" % event.object.uuid)

    tempregister = event.object.root._tempregister
    tempregister.unindex_object(event.object)


def objectAdded(event):

    LOGGER.debug("Adding temp object %s" % event.object.uuid)

    tempregister = event.object.root._tempregister
    tempregister.cleanup()
    tempregister.index_object(event.object)


class TempRegister(object):

    def __init__(self, timeout):

        self._register = OOBTree()
        self._timeout = timeout

    def unindex_object(self, object):

        if hash(object.uuid) in self._register:
            del self._register[hash(object.uuid)]
            self._p_changed = 1

    def index_object(self, object):

        self._register[hash(object.uuid)] = object_to_path(object)
        self._p_changed = 1


    def cleanup(self):

        now = datetime.datetime.now()

        uuids = [k for k in self._register.keys()]

        for uuid in uuids:

            path = self._register[uuid]
            object = path_to_object(path, self.__parent__)

            if object == None:
                del self._register[uuid]
                self._p_changed = 1

            elif ITemporaryObject.providedBy(object):

                # check timout..
                if (now - object.changed).seconds > self._timeout:

                    self.unindex_object(object)
                    object.__parent__.remove_content(object.id)
