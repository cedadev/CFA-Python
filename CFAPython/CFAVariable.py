from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregatedDimension
from CFAPython.CFAExceptions import CFAException

from ctypes import c_int, pointer

class CFAVariable:
    def __init__(self, parent_id: int = -1, id: int = -1):
        """Create a CFA Variable from a parent_id and an id"""
        self.__parent_id = parent_id
        self.__cfa_id = id