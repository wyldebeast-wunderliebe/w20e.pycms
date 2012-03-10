import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
version = open(os.path.join("w20e", "pycms", "version.txt")
               ).readlines()[0].strip()

requires = [
    'pyramid>=1.3b2',
    'pyramid_zodbconn',
    'pyramid_tm',
    'pyramid_zcml',
    'pyramid_debugtoolbar',
    'pyramid_mailer',
    'ZODB3',
    'repoze.catalog',
    'cssmin',
    'w20e.hitman',
    'PasteScript>=1.3',
    'eye',
    ]

setup(name='w20e.pycms',
      version=version,
      description='Pyramid CMS',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='D.A.Dokter',
      author_email='dokter@w20e.com',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="w20e.pycms",
      entry_points = """\
      [paste.app_factory]
      main = w20e.pycms:main
      [paste.global_paster_command]
      pycms_pack = w20e.pycms:PackCommand
      """,
      paster_plugins=['pyramid'],
      )
