
from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregatedDimension
from CFAPython.CFAExceptions import CFAException

from ctypes import c_int, pointer

class CFADimension:
    def __init__(self, parent_id: int = -1, id: int = -1):
        """Create a CFA Dimension from a parent_id and an id"""
        self.__parent_id = parent_id
        self.__cfa_id = id

    @property
    def _dimension(self) -> object:
        """Get the underlying CFA-C AggregatedDimension for this CFADimension.
        Hidden (private) as we want users to access the property functions
        instead of querying the C_AggregatedDimension structure directly."""
        cfa_dim = C_AggregatedDimension()
        cfa_dim_p = pointer(cfa_dim)
        cfa_err = CFAPython.lib.cfa_get_dim(
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
    def len(self) -> int:
        """Return the length of the dimension"""
        return self._dimension.length

    @property
    def type(self) -> int:
        """Return the datatype of the dimension"""
        return CFAPython.CFAType(self._dimension.cfa_dtype.type)