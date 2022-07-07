from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregationVariable
from CFAPython.CFAExceptions import CFAException

from ctypes import c_int, pointer

class CFAVariable:
    def __init__(self, parent_id: int = -1, id: int = -1):
        """Create a CFA Variable from a parent_id and an id"""
        self.__parent_id = parent_id
        self.__cfa_id = id

    @property
    def _variable(self) -> object:
        """Get the underlying CFA-C AggregationVariable for this CFAVariable.
        Hidden as we don't users to access this method."""
        cfa_var = C_AggregationVariable()
        cfa_var_p = pointer(cfa_var)
        cfa_err = CFAPython.lib.cfa_get_var(self.__parent_id, 
            self.__cfa_id,
            pointer(cfa_var_p)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_var_p[0]

    @property
    def name(self) -> str:
        """Return the name of the dimension"""
        return self._variable.name.decode('utf-8')