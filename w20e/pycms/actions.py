from zope.interface import Interface


class Action(object):

    def __init__(self, name, target, ctype=[], permission="", condition=True):

        self.name = name
        self.target = target
        self.ctype = ctype
        self.permission = permission
        self.condition = condition or True


class IActions(Interface):

    """ Marker class """


class Actions(object):

    """ Object actions tool """

    def __init__(self):

        self.registry = {}


    def register_action(self, name, target, category, ctype=[],
                        permission="", condition=True):

        if not self.registry.has_key(category):
            self.registry[category] = []

        if ctype:
            ctype = [typ.strip() for typ in ctype.split(",")]

        self.registry[category].append(
            Action(name, target, ctype, permission, condition)
            )


    def get_actions(self, category, ctype=None):

        actions = self.registry.get(category, [])
        if not ctype:
            return actions
        else:
            return [action for action in actions if (ctype in action.ctype or not action.ctype)]
