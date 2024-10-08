
from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregatedDimension
from CFAPython.CFAExceptions import CFAException

from ctypes import c_int, pointer

class CFADimension:
    def __init__(self, parent_id: int = -1, id: int = -1, nc_object: object=None):
        """Create a CFA Dimension from a parent_id and an id"""
        self.__parent_id = parent_id
        self.__cfa_id = id
        self._nc_object = nc_object

    def __str__(self):
        return (f"{self.name}: {self.__class__}: name={self.name}, size={self.size}, "
                f"type={self.type}")
    
    def __repr__(self):
        return self.__str__()

    @property
    def _dimension(self) -> object:
        """Get the underlying CFA-C AggregatedDimension for this CFADimension.
        Hidden (private) as we want users to access the property functions
        instead of querying the C_AggregatedDimension structure directly."""
        cfa_dim = C_AggregatedDimension()
        cfa_dim_p = pointer(cfa_dim)
        cfa_err = CFAPython.lib().cfa_get_dim(
            self.__parent_id, self.__cfa_id, pointer(cfa_dim_p)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_dim_p.contents

    @property
    def name(self) -> str:
        """Return the name of the dimension"""
        return self._dimension.name.decode('utf-8')

    @property
    def size(self) -> int:
        """Return the length of the dimension"""
        return self._dimension.length

    @property
    def type(self) -> int:
        """Return the datatype of the dimension"""
        return CFAPython.CFAType(self._dimension.cfa_dtype.type)
    
    @property
    def nc(self) -> object:
        """Return the netcdf object this dimension maps to."""
        return self._nc_object

    @property
    def nc_id(self) -> object:
        """Return the underlying id (in the C library) of the dimension this maps to"""
        return self._nc_object._dimid
    
    @property
    def cfa_id(self) -> object:
        """Return the CFA id this dimension maps to."""
        return self.__cfa_id