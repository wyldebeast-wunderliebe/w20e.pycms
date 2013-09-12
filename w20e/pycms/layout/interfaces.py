from zope.interface import Interface


class ILayout(Interface):

    """ Any content has a layout."""


class ILayouts(Interface):

    """ Marker class for layouts registry """


class IBaseLayout(ILayout):

    """ Base implementation """


class ILayoutMixin(Interface):

    """ Marker interface for content types that have a layout """
