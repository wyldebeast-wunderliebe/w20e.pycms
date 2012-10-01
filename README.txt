w20e.pycms
==========

Only fools and nerds create their own CMS nowadays. Hurray! Anyway, so
here it is, w20e.pycms. Using the Pyramid framework as its base,
building on top of good old Zope (and some Plone) concepts. The CMS is
created using these main concepts:

* ZODB as database
* ZCML as configuration/glue language
* small core
* optional components (like search, catalog, sharing); just include what
  you like

The CMS is a framework, not an out of the box app. What you'll need to
do is create your own Pyramid app, using the CMS as base. We've tried
to make this as easy as possible: use w20e.pycms.sitemaker (to be
found on github or pypi) to obtain a paster template for your app. Run
paster to create your app, and there you go...


Why?
----

w20e.pycms is Yet Another CMS, but without using the acronym.  Why,
for the flying spaghetti monsters sake another CMS? Well, you know how
it goes. You use Plone for some years, find out that when your
favourite tool is a hammer, all problems have a rather strong tendency
towards nailishness... Then Pyramid comes along, giving you the best
of Plone (ZODB, Zope Component Architecture, ZCML, Chameleon, etc.)
for creating lightweight apps. Then you need a Page with
WYSIWYG... then you need search... sharing. Then you wake up with a
basic CMS in your hands. May as well share it so you can decide for
yourself whether it is worth your while. I mean, you dont __have__ to
use it!

Anyway, read on if you like...

For whom..?
-----------

w20e.pycms is not for the faint of heart, nor for people that cannot
read Python code, hate programming, think that the use of XML for
configuration is sooo 1990, are convinced that Windows 95 was the best
OS ever or would preferrably use a rocket launcher to deal with vermin
in the kitchen. It _is_ on the other hand, for those that rank
fuckit.js among the best JS libraries ever, enjoy Terry Pratchett,
love buildout en ZCML and think that beer is so much more that just a
breakfast drink.

Features
--------

Our little CMS gives you a framework to build your sites upon, if
you're not targeting the enterprise market. If you do, be gone (to the
plone.org site)!

PyCMS gives you:

 * ZODB for storing data
 * blobstorage
 * user & group management
 * search, using repoze.catalog (optional)
 * creating and maintaining pages
 * an easily extendable framework for new content types
 * a lot of ZCML configuration
 * CMS design based on (Twitter) Bootstrap


Getting started
---------------

We assume that you know how to use buildout, create virtual
environments, like to use paster, etc. But this is only one way to get
things going...

First, create a package for your project, requiring:

  w20e.pycms

The easiest way to do so, is using our paster template
pycms_project. Install the w20e.pycms.sitemaker package (get it from
github), something along these lines:

  # virtualenv <env>
  # cd <env>; ./bin/activate
  # ./bin/easy_install w20e.pycms.sitemaker
  # cd <wherever you'd like your app sources>
  # paster create -t pycms_project <package name>

If you really want to do it by hand, create an __init__ file for your
Pyramid app like this:

  from w20e.pycms import make_pycms_app


  def main(global_config, **settings):

    return make_pycms_app(__package__, **settings)

and Bob might be your Uncle.

Secondly, create a buildout and virtualenv for your stuff. Why not use
w20e.buildoutskel? Install it using easy_install, and

  # cd <whereever you want your buildout files>
  # paster create -t buildout

and answer <package name> to the project name question, and pycms to
the type question.
You now have a bunch of buildout files, almost ready to run your app!

You most likely will consider creating a buildout-my.cfg that extends
buildout-base.cfg, and adds some develop paths, like:

develop =
  <that path where your pycms app was created, and where the setup.py resides...>

Last, run python bootstrap.py and then buildout with your config file.

Now it's time to rev up the engine, and see what has happend. Run your
app like so (within the buildout dir):

  # ./bin/paster serve dvl.ini [--reload]

Direct your favorite browser (most likely Lynx or Mosaic) to
http://localhost:6543/ and sit back and relax!


Configuration

-------------

You may or may not be totally satisfied with the result so far. If
this is utterly your idea of a superduper web app, good on ya! If not,
read on...


- Add the default management and public css / js files (if you want):

 add this to your configure.zcml:

 <include package="w20e.pycms" file="public_resources.zcml"/>
 <include package="w20e.pycms" file="manage_resources.zcml"/>

- Include any other CSS and JS you like, using the pycms zcml directives:

  <pycms:css
    cssfile="your.css"
    csstarget="public"
    media="screen"
    />

  <pycms:js
    jsfile="your.js"
    jstarget="public"
    />

- Override assets like favicon and robots.txt:

  <asset
    to_override="w20e.pycms:static/favicon.png"
    override_with="yourapp:static/favicon.png.png"
    />

- Most likely you'll want to override the 'content' macro, that is
  called to display a page. To do this, make your own pt file, make
  that extend 'main.macros['master'], and let it fill the 'body' slot:

<metal:define-macro define-macro="master"
                    metal:extend-macro="main.macros['master']">

  <html xmlns="http://www.w3.org/1999/xhtml"
      xml:lang="en"
      i18n:domain="w20e"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      >

    <head/>

    <body metal:fill-slot="body">
      Good morning Grommit...

      <metal:define-slot define-slot="content" />
    </body>
  </html>
  </metal:define-macro>

and add to your configure.zcml (always assuming you called your macro
main.pt):

  <pycms:macro
     name="body"
     ptfile="yourpackage:templates/main.pt"
     />


Using the CMS: core concepts
----------------------------

The core CMS consists solely of pages. Pages are just things with
text. Nothing serious. You may want to create your own content types,
actions, etc. Luckily that's not hard to do. Best way is to look at
existing code... Anyway, some examples here:


Actions
-------

You can register actions with your content. The currently used setup
mainly uses 'perspectives' or ways to look at your content. In the
management interface these are rendered as 'tabs'. Actions are
configured using zcml. Use the action statment as follows:

<pycms:action
  name="users"
  target="./users"
  category="perspective"
  ctype="site"
/>

ctype is an optional filter.


Content types
-------------

Create your own content types if you wish. You can register an icon,
and possible subtypes with your type using:

  <pycms:ctype
     name="your_type_id"
     factory=".models.yourtype.YourType"
     subtypes="someothertype,someevenothertype"
     icon="/static/img/yourtype_icon.png"
     />

Your actual model should extend either
  w20e.pycms.models.base.BaseContent
or
  w20e.pycms.models.base.BaseFolder.

You may want to use w20e.forms (read: should) for your model. You can
either create an xml form that describes your model, or if you insist
on doing things more Pythonic, create your form
programmatically. Checkout out w20e.forms for details.

A simple model looks like this:

from w20e.pycms.models.base import BaseContent


class SomethingSimple(BaseContent):

    """ Well, actually it's more like an 'object'... """

    def __init__(self, content_id, data=None):

        BaseContent.__init__(self, content_id, data)

    def base_id(self):

        return self.__data__['title']

    @property
    def title(self):

        return self.__data__['title']

You can configure how your form for editing and adding is
found. Default is that PyCMS looks for a file in <your package
home>/forms/<content type>.xml, so in this case:

  <package home>/forms/somethingsimple.xml

If you want something completely different, configure an adapter for your
content type that provides a form factory:

  <adapter
      factory=".your.Factory" 
      for=".your.content.Type" 
      provides="w20e.forms.interfaces.IFormFactory" />

And make sure it actually implements IFormFactory and can create a
form (w20e.forms.interfaces.IForm).


Natures
-------

An alternative for defining content types is defining 'natures'. Let's
face it: what is so special about an event? It is really just a page
thing with a start- and end date and a location, isn't it? And what
about news? Isn't that not very much like a page too? If you agree,
read on...

A page can be not only a page, but it can also be news-ish, or
event-ish. That is it's nature. You can register natures like so:

  <pycms:nature
      name="event"
      interface="w20e.pycms_events.interfaces.IEvent"
      />

This will make the nature show up in the 'natures' dropdown menu. Now
either you leave it like this, or you also modify the form for the
page with an w20e.forms.interfaces.IFormModifier implementation:

  <subscriber
      for="w20e.pycms_events.interfaces.IEvent"
      factory="w20e.pycms_events.models.event.Event"
      provides="w20e.forms.interfaces.IFormModifier"
      />

And create a class Event along these lines:

  from zope.interface import implements
  from w20e.forms.interfaces import IForm, IFormModifier
  from w20e.forms.data.field import Field
  from w20e.forms.model.fieldproperties import FieldProperties
  from w20e.forms.rendering.control import Input
  from w20e.forms.rendering.group import FlowGroup


  class Event(object):

      implements(IFormModifier)

      def __init__(self, form):

          self.form = form

      def modify(self, form):

          """ Add begin, end and location to form """

          form.data.addField(Field("start"))
          form.data.addField(Field("end"))
          form.data.addField(Field("location"))

          grp = FlowGroup("eventgroup", label="Event")
          grp.addRenderable(Input("start", "Start of event",
                                  extra_classes="datetime",
                                  bind="start"))
          grp.addRenderable(Input("end", "End of event", bind="end"))
          grp.addRenderable(Input("location", "Location", bind="location"))

          form.view.addRenderable(grp, pos=-1)

Or whatever you think should be added to the page form...


robots.txt
----------

The default robots.txt allows all. Override as per your liking...


Search
------

Would you like search enabled for your site?

Add this to your configure.zcml:

  <include package="w20e.pycms" file="search.zcml"/>


Sharing anyone?
---------------
Would you like search enabled for your site?

Add this to your configure.zcml:

  <include package="w20e.pycms_sharing"/>

and this to your setup dependencies (don't forget to run buildout):

  w20e.pycms_sharing


Settings
--------

pycms.acl.force_new = True|False
        Force new version of ACL. All your security data will be lost
pycms.catalog.force_new = True|False
        Force new version of catalog. All your entries will be lost, but you
        can just run reindex-catalog and all is well again...
pycms.admin_user = <user>:<pwd>
        Admin user and password, like so: pycms.admin_user = admin:pipo
pycms.admin_secret = <somesecret>
        This secret may be used as URL parameter to obtain admin permission
        Use it wisely!
pycms.minify_css = True|False
        Minify CSS. Defaults to False
pycms.minify_js = True|False
        Minify JS. Defaults to False
pycms.logged_in_redirect = <url>
pycms.rootclass = <full dotted classname>
        Defaults to w20e.pycms.models.site.Site
pycms.roottitle = <string>
        Defaults to "Welcome"
pycms.from_addr
        Send email as ...
pycms.bcc_addr
        Send also to bcc
pycms.after_add_redirect
        Where to go after successfull add
pycms.cancel_add_redirect
        Where to go after cancelled add
pycms.after_del_redirect
        Where to go after delete
pycms.tempregister.timout = <int>
        minimal amount of seconds before a temporary object might be removed
