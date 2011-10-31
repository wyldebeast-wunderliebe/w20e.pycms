from pyramid.view import render_view


class BlockContainer(object):

    """ Hold blocks """

    def __init__(self, refs=False):

        self.blocks = []
        self.blockrefs = {}
        self.refs = refs


    def add_block(self, block):

        self.blocks.append(block)

        if self.refs:
            self._add_refs(block)


    def _add_refs(self, block):

        self.blockrefs[block.id] = block
        
        for subblock in getattr(block, 'blocks', []):

            self._add_refs(subblock)


    def get_blocks(self):

        return self.blocks


    def get_block_by_ref(self, block_ref):

        return self.blockrefs.get(block_ref, None)


    def clear_blocks(self):

        self.blocks = []
        self.blockrefs.clear()


class Block(dict):

    type = ""

    def __init__(self, block_id, **props):

        self.id = block_id
        self['id'] = block_id

        defaults = {'width': "50%", 'height': "200px", 
                    "top": "10px", "left": "10px"}
        defaults.update(props)

        self.update(defaults)


class Group(Block, BlockContainer):

    def __init__(self, group_id, **props):

        Block.__init__(self, group_id, **props)
        BlockContainer.__init__(self)


class BlockView(object):

    """ Base view for blocks """

    def __init__(self, context, request):

        self.context = context
        self.request = request


    def __call__(self):

        return {}


    @property
    def height(self):

        return self.context.get('height', '')


    @property
    def top(self):

        return self.context.get('top', '')


    @property
    def left(self):

        return self.context.get('left', '')


    @property
    def width(self):

        return self.context.get('width', '')


    @property
    def type(self):

        return self.context.type


    @property
    def id(self):

        return self.context['id']


    @property
    def style(self):

        _style = ""

        if self.width:
            _style += "width: %s;" % self.width

        if self.height:
            _style += "height: %s;" % self.height

        if self.top:
            _style += "top: %s;" % self.top

        if self.left:
            _style += "left: %s;" % self.left

        return _style


    @property
    def extra_classes(self):

        return self.context.get('class', '')

    
    @property
    def config(self):

        return '<dl class="config">' + "".join(["<dt>%s</dt><dd>%s</dd>" % (key, self.context[key]) for key in self.context.keys()]) + "</dl>"



class GroupView(BlockView):

    """ Base view for blocks that are groups """

    def __init__(self, context, request):

        self.context = context
        self.request = request


    @property
    def content(self):

        html = []

        for block in self.context.blocks:

            html.append(render_view(block, self.request))

        return "".join(html)
