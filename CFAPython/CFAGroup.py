
from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregationContainer
from CFAPython.CFAExceptions import CFAException
from CFAPython.CFADimension import CFADimension

from ctypes import c_int, pointer

class CFAGroup:
    def __init__(self, parent_id: int = -1, id: int = -1):
        """Create a CFA Aggregation Container which will be assigned to a 
        group when written to a CFA-netCDF file."""
        self.__parent_id = parent_id
        # cfa_id - save in the class
        self._cfa_id = id

    @property
    def _container(self) -> object:
        """Get the underlying CFA-C AggregationContainer for this CFAGroup.
        Hidden (private) as we don't want users to access this method as it
        returns a C_AggregationContainer structure."""
        cfa_cont = C_AggregationContainer()
        cfa_cont_p = pointer(cfa_cont)
        cfa_err = CFAPython.lib.cfa_get(self._cfa_id, 
                                        pointer(cfa_cont_p))
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_cont_p[0]

    @property
    def _dim_ids(self) -> list[int]:
        """Get the Dimension ids - this function is hidden as we want users
        to call getDimension()"""
        container = self._container # call this just once
        dimids = []
        for d in range(0, container.n_dims):
            dimids.append(container.cfa_dimids[d])
        return dimids
    
    def getDims(self) -> list[object]:
        """Get the list of CFADimensions contained in this container (group)"""
        dims = []
        for d in self._dim_ids:
            dims.append(CFADimension(self._cfa_id, d))
        return dims

    @property
    def ngroups(self) -> int:
        """Return the number of containers (groups) in this container (group).
        """
        return self._container.n_conts

    @property
    def nvars(self) -> int:
        """Return the number of variables in this container."""
        return self._container.n_vars

    @property
    def ndims(self) -> int:
        """Return the number of dimensions in this container."""
        return self._container.n_dims