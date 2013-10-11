import os
from chameleon import PageTemplateFile
from zope.interface import implements
from w20e.forms.rendering.interfaces import IControlRenderer
from w20e.forms.registry import Registry
from w20e.forms.rendering.control import Control


class ReferenceRenderer(object):

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        """ render Input to HTML """

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        tplfile = "%s/reference.pt" % os.path.dirname(__file__)

        tpl = PageTemplateFile(tplfile, encoding="utf-8")
        value = form.getFieldValue(renderable.bind, lexical=True)

        print >> out, tpl(
            control=renderable,
            value=value,
            fmtmap=fmtmap
            )


class Reference(Control):

    """ Reference control """

