
import CFAPython
from CFAPython.CFAGroup import CFAGroup
from CFAPython.CFAExceptions import CFAException
from CFAPython import CFAFileFormat

from netCDF4 import Dataset 

from ctypes import *

class _CFADataset:
        
    def __init__(self, filename, mode='r', format=CFAFileFormat.CFANetCDF, x_id=0):
        self.__mode = mode
        self.__format = format
        self.__filename = filename
        self._cfa_id = 0
        self._x_id = x_id
        # if this is a CFA file then create the CFA instance
        if format == CFAFileFormat.CFANetCDF:
            # create a string buffer and encode the Python path into it
            cpath = c_char_p(filename.encode())
            # mode is either "r" or "w"
            self.__mode = mode
            if (self.__mode == "w"):
                pass
            #     # create the CFA object - this doesn't do any file manipulation yet
            #     cfa_id = c_int(0)
            #     cfa_err = CFAPython.lib.cfa_create(
            #         cpath, c_int(format), byref(cfa_id)
            #     )
            #     if (cfa_err != 0):
            #         raise CFAException(cfa_err)
            #     self._cfa_id = cfa_id
            elif (self.__mode == "r"):
                # get thet netCDF file id from the parent netCDF dataset
                cfa_id = c_int(0)
                cfa_err = CFAPython.lib.cfa_load(
                    cpath, c_int(self._x_id), c_int(format), byref(cfa_id)
                )
                if (cfa_err != 0):
                    raise CFAException(cfa_err)
                self._cfa_id = cfa_id
            else:
                raise CFAException("Unknown mode")


    def serialise(self):
        pass
        # if (self.__mode == "w"):
        #     grpid = c_int(self._grpid)
        #     cfa_err = CFAPython.lib.cfa_serialise(
        #         c_int(self._cfa_id), grpid
        #     )
        #     if (cfa_err != 0):
        #         raise CFAException(cfa_err)


    def __del__(self):
        """Serialise if self.mode == "w" and then close the CFA-netCDF file"""
        # if (self.__mode == "w"):
        #     grpid = c_int(self._grpid)
        #     cfa_err = CFAPython.lib.cfa_serialise(
        #         c_int(self._cfa_id), grpid
        #     )
        #     if (cfa_err != 0):
        #         raise CFAException(cfa_err)
        # cfa_err = CFAPython.lib.cfa_close(c_int(self._cfa_id))
        # if (cfa_err != 0):
        #     raise CFAException(cfa_err)
        pass


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
    _private_atts = ["CFA",]

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
        # only parse if the file is a CFA file
        if format == CFAFileFormat.CFANetCDF:
            self.CFA = _CFADataset(
                filename=filename, format=format, mode=mode, x_id=self._grpid
            )
        else:
            self.CFA = None


    def __getattr__(self, name):
        if name in CFADataset._private_atts:
            return self.__dict__[name]
        else:
            return Dataset.__getattr__(self, name)


    def __setattr__(self, name, value):
        """Override the __setattr__ for the Dataset so as to assign its
        private variables."""
        if name in CFADataset._private_atts:
            self.__dict__[name] = value
        else:
            Dataset.__setattr__(self, name, value)