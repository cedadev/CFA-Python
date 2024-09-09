
import CFAPython
from CFAPython.CFAGroup import CFAGroup
from CFAPython.CFAVariable import CFAVariable
from CFAPython.CFAExceptions import CFAException
from CFAPython import CFAFileFormat
from CFAPython.version import MAJOR_VERSION, MINOR_VERSION, REVISION

from netCDF4 import Dataset 

from ctypes import *

class _CFADataset(CFAGroup):
        
    def __init__(self, filename: str, mode: str='r', 
                 format: CFAFileFormat=CFAFileFormat.CFANetCDF, 
                 nc_object: object=None):
        
        super().__init__(0, nc_object)
        self.__mode = mode
        self.__format = format
        self.__filename = filename
        # if this is a CFA file then create the CFA instance
        if format == CFAFileFormat.CFANetCDF:
            # create a string buffer and encode the Python path into it
            cpath = c_char_p(filename.encode())
            # mode is either "r" or "w"
            self.__mode = mode
            if (self.__mode == "w"):
                # create the CFA object - this doesn't do any file manipulation yet
                cfa_id = c_int(0)
                cfa_err = CFAPython.lib().cfa_create(
                    cpath, c_int(format), byref(cfa_id)
                )
                if (cfa_err != 0):
                    raise CFAException(cfa_err)
                self._cfa_id = cfa_id
            elif (self.__mode == "r"):
                # get thet netCDF file id from the parent netCDF dataset
                cfa_id = c_int(0)
                cfa_err = CFAPython.lib().cfa_load(
                    cpath, c_int(self.nc_id), c_int(format), byref(cfa_id)
                )
                if (cfa_err != 0):
                    raise CFAException(cfa_err)
                self._cfa_id = cfa_id
            else:
                raise CFAException("Unknown mode")

    def close(self):
        """Serialise if self.mode == "w" and then close the CFA-netCDF file"""
        if self.__mode == 'w':
            # serialise the root group (i.e. this group)
            self.serialise()
            # write the global metadata
            self._nc_object.Conventions = f"CFA-{MAJOR_VERSION}.{MINOR_VERSION}.{REVISION}"
        
        cfa_err = CFAPython.lib().cfa_close(self._cfa_id)
        if (cfa_err != 0):
            raise CFAException(cfa_err)

    @property
    def id(self) -> int:
        "Return the CFA id for the Dataset"
        return self._cfa_id

    @property
    def path(self) -> str:
        """Return the path of the Dataset"""
        return self._container.path.decode('utf-8')

    @property
    def format(self) -> CFAPython.CFAFileFormat:
        """Return the format of the Dataset"""
        return CFAPython.CFAFileFormat(self._container.format)
    

class CFADataset(Dataset):
    """This is a wrapper class for the actual _CFADataset class.
    It inherits the netCDF4-python Dataset class and adds a .CFA member object which
    contains the CFA functionality."""

    # declare private atts, otherwise they will be written out into the netCDF file
    # as global variables
    _private_atts = ["CFA", "closed"]

    def __init__(self, filename, mode='r', clobber=True, format='NETCDF4',
                 diskless=False, persist=False, keepweakref=False,
                 memory=None, encoding=None, parallel=False, **kwargs):
        """Create a CFA object within a netCDF4 Dataset and either read it in from
        a CFA-netCDF file, or create the file to write to.
        (Comm and Info from netCDF4-python not supported as arguments currently)
        """
        # CFANetCDF files must be created as NETCDF4 files
        if format == CFAFileFormat.CFANetCDF:
            in_format = 'NETCDF4'
        else:
            in_format = format
        # create the netCDF Dataset 
        super().__init__(filename=filename, mode=mode, clobber=clobber, 
                         format=in_format, diskless=diskless, persist=persist, 
                         keepweakref=keepweakref, memory=memory, encoding=encoding, 
                         parallel=parallel, kwargs=kwargs)
        # only parse or serialise if the file is a CFA file
        if format == CFAFileFormat.CFANetCDF:
            self.CFA = _CFADataset(
                filename=filename, format=format, mode=mode, nc_object=self
            )
        else:
            self.CFA = None

        # parse - this will assign the netCDF variables and dimensions
        # to the CFA instances 
        if self.CFA and mode == 'r':
            self.CFA.parse()
        self.closed = False

    def close(self):
        self.CFA.close()
        super().close()
        self.closed = True

    def __del__(self):
        if not self.closed:
            raise CFAException("Dataset was not closed")

    def __getattr__(self, name) -> object:
        if name in CFADataset._private_atts:
            return self.__dict__[name]
        else:
            return Dataset.__getattr__(self, name)

    def __setattr__(self, name, value) -> None:
        """Override the __setattr__ for the Dataset so as to assign its
        private variables."""
        if name in CFADataset._private_atts:
            self.__dict__[name] = value
        else:
            Dataset.__setattr__(self, name, value)