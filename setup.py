from setuptools import setup, Extension
import os
import tempfile
import urllib.request
import zipfile
from io import BytesIO
import time

MAJOR_VERSION = '0'
MINOR_VERSION = '0'

CFA_C_VERSION_TAG = "0.0.0"

CFA_C_URL = "https://github.com/cedadev/CFA-C/archive/refs/tags/"

# create a temporary directory to store the downloaded CFA-C source code
# it has to be global so that the tmp_dir object doesn't go out of scope and 
# then get deleted
tmp_dir = tempfile.TemporaryDirectory()

def fetch_cfa_c_source():
    # download the CFA-C source from GitHub, at the tagged version, as a zipfile
    cfa_zip_url = CFA_C_URL + "v" + CFA_C_VERSION_TAG + ".zip"
    cfa_url_obj = urllib.request.urlopen(cfa_zip_url)
    # read / stream the data
    cfa_url_data = cfa_url_obj.read()
    # open the zipfile
    cfa_zip = zipfile.ZipFile(BytesIO(cfa_url_data))
    # unzip the files to the temporary directory
    cfa_zip.extractall(tmp_dir.name)


def build_cfa_extension():
    # fetch the CFA-C source code from GitHub
    fetch_cfa_c_source()
    # build the sources list for the CFA-C library
    sources = [ "cfa.c",
                "cfa_var.c",
                "cfa_mem.c",
                "cfa_info.c",
                "cfa_dim.c",
                "cfa_cont.c",
                "parsers/cfa_netcdf.c" ]

    # append the temporary directory path to the sources and collate into a list
    cfa_sources = []
    src_dir = os.path.join(tmp_dir.name, "CFA-C-"+CFA_C_VERSION_TAG+"/src")
    for s in sources:
        cfa_sources.append(os.path.abspath(os.path.join(src_dir, s)))

    # create the Extension class to pass to setup
    cfa_c = Extension(name='CFAPython.cfa',
                define_macros=[('MAJOR_VERSION', MAJOR_VERSION),
                               ('MINOR_VERSION', MINOR_VERSION)],
                include_dirs=[src_dir,
                              os.path.join(src_dir, 'parsers')],
                extra_compile_args=["-D_DEBUG"],
                libraries=['netcdf'],
                language='c',
                sources=cfa_sources)
    return [cfa_c]


setup(name='CFAPython',
    version=MAJOR_VERSION + '.' + MINOR_VERSION,
    description='Python bindings for the CFA-C library',
    author='Neil Massey',
    author_email='neil.massey@stfc.ac.uk',
    url='https://github.com/cedadev/CFA-python',
    long_description = '''
Python bindings for the CFA-C library.
''',
    packages=["CFAPython"],
    ext_modules = build_cfa_extension()
)