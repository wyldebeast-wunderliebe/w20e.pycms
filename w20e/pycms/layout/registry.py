from interfaces import ILayouts


def add_layouts(event):

    if event['renderer_name'].endswith("layout/templates/action.pt"):

        layouts = event['request'].registry.getUtility(ILayouts)

        valid_layouts = []

        for layout in layouts.list_layouts():

            valid_layouts.append(layout)

        event['layouts'] = valid_layouts


class Layouts(object):

    """ Layouts utility tool """

    def __init__(self):

        self.registry = {}
        self.if_registry = {}
        self.blocks = {}

    def register_block(self, name, block):

        self.blocks[name] = block

    def register_layout(self, name, layout):

        self.registry[name] = layout
        self.if_registry[layout.interface] = layout

    def get_layout(self, layout_name):

        return self.registry.get(layout_name, None)

    def get_layout_by_if(self, layout_if):

        return self.if_registry.get(layout_if, None)

    def list_layouts(self):

        return self.registry.values()
