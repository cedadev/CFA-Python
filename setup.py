from setuptools import setup, Extension
import os
import tempfile
import urllib.request
import zipfile
from io import BytesIO
import shutil
import site
import sys
from CFAPython.version import MAJOR_VERSION, MINOR_VERSION, REVISION

CFA_C_VERSION_TAG = "0.0.6"

CFA_C_URL = "https://github.com/cedadev/CFA-C/archive/refs/tags/"
CFA_C_LOCAL = "/Users/neil.massey/Coding/CFA-C"

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

def fetch_cfa_c_source_local():
    # Local version of fetching the source to enable faster development
    shutil.copytree(CFA_C_LOCAL, 
                    os.path.join(tmp_dir.name, "CFA-C-"+CFA_C_VERSION_TAG))

def get_netcdf_library_path_mac():
    lib_dirs = []
    for s in site.getsitepackages():
        lib_dir = os.path.join(s, "netCDF4/.dylibs")
        lib_dirs.append(lib_dir)
    return lib_dirs

def get_netcdf_library_path():
    # this is probably path specific, this works for Mac
    if sys.platform == 'darwin':
        return get_netcdf_library_path_mac()
    else:
        raise NotImplementedError("Platform is currently not supported")

def get_netcdf_libraries():
    # get the names of the netcdf libraries, by searching the library path
    # for "netcdf"
    path = get_netcdf_library_path()
    libraries = []
    for d in path:
        for f in os.listdir(d):
            if "netcdf" in f:
                # on the mac, libraries are suffixed by "dylib", but the linker doesn't
                # want that
                if sys.platform == 'darwin':
                    lib_name = f.strip(".dylib")
                    libraries.append(lib_name)
                else:
                    raise NotImplementedError("Platform is currently not supported")
    return libraries
            

def build_cfa_extension():
    # fetch the CFA-C source code from GitHub or local
    if True:
        fetch_cfa_c_source_local()
    else:
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
 
    lib_dirs = get_netcdf_library_path()
    # create the Extension class to pass to setup
    cfa_c = Extension(name='CFAPython.cfa',
                define_macros=[('MAJOR_VERSION', MAJOR_VERSION),
                               ('MINOR_VERSION', MINOR_VERSION)],
                include_dirs=[src_dir,
                              os.path.join(src_dir, 'parsers')],
                extra_compile_args=["-D_DEBUG"],
                library_dirs=lib_dirs,
                libraries=get_netcdf_libraries(),
                language='c',
                sources=cfa_sources)
    return [cfa_c]

if __name__ == "__main__":
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
