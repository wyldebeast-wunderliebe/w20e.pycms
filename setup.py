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
    ]

setup(name='w20e.pycms',
      version=version,
      description='Pyramid CMS',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='D.A.Dokter, H.Bouma',
      author_email='dokter@w20e.com, bouma@w20e.com',
      license='beer-ware',
      url='https://github.com/wyldebeast-wunderliebe/w20e.pycms/',
      keywords='cms pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="w20e.pycms",
      entry_points = """\
      [paste.global_paster_command]
      pycms_pack = w20e.pycms:PackCommand
      """,
      paster_plugins=['pyramid'],
      )
