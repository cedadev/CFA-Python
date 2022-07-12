
from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_AggregationContainer
from CFAPython.CFAExceptions import CFAException
from CFAPython.CFADimension import CFADimension
from CFAPython.CFAVariable import CFAVariable

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
        cfa_err = CFAPython.lib.cfa_get(
            self._cfa_id, pointer(cfa_cont_p)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_cont_p[0]

    @property
    def _dim_ids(self) -> list[int]:
        """Get the CFADimension ids - this function is hidden as we want users
        to call getDims() or getDim()"""
        container = self._container # call this just once
        dimids = []
        for d in range(0, container.n_dims):
            dimids.append(container.cfa_dimids[d])
        return dimids

    @property
    def _var_ids(self) -> list[int]:
        """Get the CFAVariable ids - this function is hidden as we want users
        to call getVars() or getVar()"""
        container = self._container # call this just once
        varids = []
        for v in range(0, container.n_vars):
            varids.append(container.cfa_varids[v])
        return varids

    @property
    def _grp_ids(self) -> list[int]:
        """Get the CFAGroup ids - this function is hidden as we want users
        to call getGrp() or get getGrps()"""
        container = self._container # call this just once
        grpids = []
        for g in range(0, container.n_conts):
            grpids.append(container.cfa_contids[g])
        return grpids

    
    def getDims(self) -> list[object]:
        """Get the list of CFADimensions in this container (CFAGroup)"""
        dims = []
        for d in self._dim_ids:
            dims.append(CFADimension(self._cfa_id, d))
        return dims

    def getDim(self, dimname) -> object:
        """Get a single dimension, matching the name"""
        dims = self.getDims()
        for dim in dims:
            if dim.name == dimname:
                return dim
        raise CFAException("Dimension {} not found".format(dimname))

    def getDimName(self, dimnum: int) -> str:
        """Get the name of a dimension in this container / group"""
        dims = self.getDims()
        if dimnum >= len(dims):
            raise CFAException(
                "Dimension number {} is out of range".format(dimnum)
            )
        return dims[dimnum].name

    def getVars(self) -> list[object]:
        """Get the list of CFAVariables in this container (CFAGroup)"""
        vars = []
        for v in self._var_ids:
            vars.append(CFAVariable(self._cfa_id, v))
        return vars

    def getVarName(self, varnum: int) -> str:
        """Get the name of a variable in this container / group"""
        vars = self.getVars()
        if varnum >= len(vars):
            raise CFAException(
                "Variable number {} is out of range".format(varnum)
            )
        return vars[varnum].name

    def getVar(self, varname) -> object:
        """Get a single variable, matching the name"""
        vars = self.getVars()
        for var in vars:
            if var.name == varname:
                return var
        raise CFAException("Variable {} not found".format(varname))

    def getGrps(self) -> list[object]:
        """Get the list of CFAGroups in this container"""
        grps = []
        for g in self._grp_ids:
            grps.append(CFAGroup(self._cfa_id, g))
        return grps

    def getGrp(self, grpname) -> object:
        """Get a single group by name"""
        grps = self.getGrps()
        for grp in grps:
            if grp.name == grpname:
                return grp
        raise CFAException("Group {} not found".format(grpname))

    def getGrpName(self, grpnum: int) -> str:
        """Get the name of a variable in this container / group"""
        grps = self.getGrps()
        if grpnum >= len(grps):
            raise CFAException(
                "Group number {} is out of range".format(grpnum)
            )
        return grps[grpnum].name

    @property
    def ngrps(self) -> int:
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

    @property
    def name(self) -> str:
        """Return the name of the group."""
        return self._container.name.decode('utf-8')