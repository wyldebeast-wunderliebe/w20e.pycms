from zope.interface import Interface


class Action(object):

    def __init__(self, name, target, label=None, icon=None,
                 ctype=[], permission="", condition=True):

        self.name = name
        self.label = label or name
        self.icon = icon
        self.target = target
        self.ctype = ctype
        self.permission = permission
        self.condition = condition


class IActions(Interface):

    """ Marker class """


class Actions(object):

    """ Object actions tool """

    def __init__(self):

        self.order = {}
        self.registry = {}

    def register_action(self, name, target, category, label=None, icon=None,
                        ctype=[], permission="", condition=True):

        if not category in self.registry:
            self.registry[category] = {}
            self.order[category] = []

        if ctype:
            ctype = [typ.strip() for typ in ctype.split(",")]

        self.registry[category][name] = Action(name,
                                               target,
                                               label=label,
                                               icon=icon,
                                               ctype=ctype,
                                               permission=permission,
                                               condition=condition)
        self.order[category].append(name)

    def get_actions(self, category, ctype=None):

        """ Return actions that actually have a target..."""

        actions = self.registry.get(category, {}).values()

        actions = [action for action in actions if action.target]

        if ctype:
            actions = [a for a in actions if (ctype in a.ctype or not a.ctype)]

        def sort_actions(x, y):

            return cmp(self.order[category].index(x.name),
                       self.order[category].index(y.name))

        return sorted(actions, sort_actions)
