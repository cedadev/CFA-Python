
import CFAPython
from CFAPython.CFAGroup import CFAGroup
from CFAPython.CFAExceptions import CFAException

from ctypes import *

class CFADataset(CFAGroup):
    def __init__(self, path: str, format: CFAPython.CFAFileFormat,
                 mode: str) -> object:
        """Create a CFA object and either read it in from a CFA-netCDF file, or 
        create the file to write to.
        Args:
            path (str): the path at which the file is located
            format (CFAPython.CFAFileFormat): the format the file is in, either
                CFANetCDF, or CFAUnknown
            mode (str): read ("r") or write ("w")
        Returns:
            CFAFile: object containing the CFAFile details
        """
        # initialise the CFAGroup base class with no parent
        super().__init__()
        # create a string buffer and encode the Python path into it
        cpath = c_char_p(path.encode())
        # mode is either "r" or "w"
        self.__mode = mode
        # now determine whether we parse the file (read) or do nothing so far
        # (write)
        if (self.__mode == "w"):
            # create the CFA object - this doesn't do any file manipulation yet
            cfa_id = c_int(0)
            cfa_err = CFAPython.lib.cfa_create(cpath,c_int(format), 
                                               byref(cfa_id))
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            self._cfa_id = cfa_id
        elif (self.__mode == "r"):
            cfa_id = c_int(0)
            cfa_err = CFAPython.lib.cfa_load(cpath, c_int(format),
                                             byref(cfa_id))
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            self._cfa_id = cfa_id
        else:
            raise CFAException("Unknown mode")

    def __del__(self):
        """Serialise if self.mode == "w" and then close the CFA-netCDF file"""
        if (self.__mode == "w"):
            cfa_err = CFAPython.lib.cfa_serialise(self._cfa_id)
            if (cfa_err != 0):
                raise CFAException(cfa_err)
        cfa_err = CFAPython.lib.cfa_close(self._cfa_id)
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
