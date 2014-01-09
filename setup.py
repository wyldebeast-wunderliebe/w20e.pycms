import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
version = open(os.path.join("w20e", "pycms", "version.txt")
               ).readlines()[0].strip()

requires = [
    'distribute',
    'pyramid>=1.4a',
    'pyramid_chameleon',
    'pyramid_zodbconn',
    'pyramid_tm',
    'pyramid_zcml',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'fanstatic>=1.0a4',
    'js.jquery',
    'pyramid_fanstatic',
    'pyramid_chameleon',
    'ZODB3',
    'repoze.catalog',
    'cssmin',
    'w20e.forms',
    'PasteScript>=1.3',
    ]

setup(name='w20e.pycms',
      version=version,
      description='Pyramid CMS',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
        ],
      author='D.A.Dokter, H.Bouma, W.G.Helmantel',
      author_email='dokter@w20e.com, bouma@w20e.com, helmantel@w20e.com',
      license='beer-ware',
      url='https://github.com/wyldebeast-wunderliebe/w20e.pycms/',
      keywords='cms pyramid',
      packages=find_packages(),
      namespace_packages=['w20e'],
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="w20e.pycms",
      entry_points = {
          'fanstatic.minifiers': [
              'jsmin = fanstatic.compiler:JSMIN_MINIFIER',
              'cssmin = fanstatic.compiler:CSSMIN_MINIFIER',
          ],
          'paste.global_paster_command': [
              'pycms_pack = w20e.pycms.pack:PackCommand'
          ]
      },
      paster_plugins=['pyramid'],
      message_extractors = { '.': [
          ('**.pt',   'lingua_xml', None ),
          ]},
      )
