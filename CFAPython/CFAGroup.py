
from __future__ import annotations
from typing import Iterable

import CFAPython
from CFAPython._CFADatatypes import C_AggregationContainer
from CFAPython.CFAExceptions import CFAException
from CFAPython.CFADimension import CFADimension
from CFAPython.CFAVariable import CFAVariable
from netCDF4 import Variable

from ctypes import c_int, c_char_p, pointer, byref, sizeof

class CFAGroup:
    def __init__(self, id: int=-1, nc_object: object=None):
        """Create a CFA Aggregation Container which will be assigned to a 
        group when written to a CFA-netCDF file."""
        # cfa_id - save in the class
        self._cfa_id = id
        self._nc_object = nc_object
        self._dimensions = []
        self._variables = []
        self._groups = []
        self.__serialised = False

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
        return cfa_cont_p.contents

    @property
    def _dim_ids(self) -> list[int]:
        """Get the CFADimension ids - this function is hidden as we want users
        to call getDimensions() or getDimension()"""
        container = self._container # call this just once
        dimids = []
        for d in range(0, container.n_dims):
            dimids.append(container.cfa_dimids[d])
        return dimids

    @property
    def _var_ids(self) -> list[int]:
        """Get the CFAVariable ids - this function is hidden as we want users
        to call getVariables() or getVariable()"""
        container = self._container # call this just once
        varids = []
        for v in range(0, container.n_vars):
            varids.append(container.cfa_varids[v])
        return varids

    @property
    def _grp_ids(self) -> list[int]:
        """Get the CFAGroup ids - this function is hidden as we want users
        to call getGroups() or get getGroup()"""
        container = self._container # call this just once
        grpids = []
        for g in range(0, container.n_conts):
            grpids.append(container.cfa_contids[g])
        return grpids

    def parse(self) -> None:
        """Parse the dataset that this group belongs to (or is) and attach r
        eferences:
        1. netCDF Groups to the CFA Groups
        2. netCDF Dimensions to the CFA Dimensions
        3. netCDF Variables to the CFA Variables"""
        # do this group first, then do the sub groups

        # reset the dimensions in case parse called twice
        self._dimensions = []
        for d in self._dim_ids:
            # get the CFADimension from the underlying CFA-C representation
            dim = CFADimension(self._cfa_id, d)
            # get the netCDF dimension and assign to the CFADimension
            dim._nc_object = self._nc_object.dimensions[dim.name]
            self._dimensions.append(dim)

        # reset the variables in case parse called twice
        self._variables = []
        for v in self._var_ids:
            # get the CFAVariable from the underlying CFA-C representation
            var = CFAVariable(self._cfa_id, v)
            # get the netCDF variable and assign to the CFAVariable
            var._nc_object = self._nc_object.variables[var.name]
            self._variables.append(var)
            var.parse(self)

        # reset the groups in case parse called twice
        self._groups = []
        for g in self._grp_ids:
            grp = CFAGroup(g)
            # get the netCDF group and assign to the CFAGroup
            grp._nc_object = self._nc_object.groups[grp.name]
            self._groups.append(grp)
            # parse the sub groups from this group
            grp.parse()

    def serialise(self) -> None:
        """Serialise the CFA Group into the netCDF Group.
        Note: CFA Dataset is derived from CFA Group, so serialising the root group
        will serialise the Dataset."""
        # Don't serialise if already serialised
        if self.__serialised:
            return
        
        # recursively serialise any groups
        for g in self._groups:
            g.serialise()

        # no need to serialise the dimensions - all the necessary steps for the CFA
        # dimensions are performed by dimension.CFA.createDimension
        
        # serialise the variables - write out the CFA fragments and the aggregation
        # instructions
        for v in self._variables:
            cfa_err = CFAPython.lib._serialise_cfa_fragments_netcdf(
                self.nc_id, self.cfa_id, v.cfa_id
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            
            cfa_err = CFAPython.lib._serialise_cfa_aggregation_instructions(
                self.nc_id, v.nc_id, self.cfa_id, v.cfa_id                 
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)
        # indicate already serialised, so close doesn't try to serialise again
        self.__serialised = True

    def createDimension(self, dimname: str, datatype: CFAPython.CFAType=4, 
                        size: int=1) -> object:
        """Add a dimension"""
        # create the CFA Dimension
        cfa_dim_id = c_int(-1)
        cname = c_char_p(dimname.encode())
        cfa_err = CFAPython.lib.cfa_def_dim(
            self._cfa_id, cname, size, datatype, pointer(cfa_dim_id)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        # create the netCDF Dimension and append to dimensions list
        dim = CFADimension(self._cfa_id, cfa_dim_id)
        dim._nc_object = self._nc_object.createDimension(dimname, size)
        self._dimensions.append(dim)
        # create the netCDF Variable to go with this Dimension
        dimtype = CFAPython.CFATypeToNumpy(datatype)
        self._nc_object.createVariable(dimname, dimtype, (dim._nc_object,))
        return dim

    @property
    def dimensions(self) -> list[object]:
        """Get the list of CFADimensions in this container (CFAGroup)"""
        return self._dimensions

    def getDimensions(self) -> list[object]:
        """Just a wrapper for the above function"""
        return self.dimensions

    def getDimension(self, dimname: str) -> object:
        """Get a single dimension, matching the name"""
        dims = self.dimensions
        for dim in dims:
            if dim.name == dimname:
                return dim
        raise CFAException("Dimension {} not found".format(dimname))

    def createVariable(self, varname: str, datatype: str="int", 
                       dimensions: Iterable[str]=[]) -> object:
        """Add a variable to the group"""
        cfa_var_id = c_int(-1)
        cname = c_char_p(varname.encode())
        cfa_err = CFAPython.lib.cfa_def_var(
            self._cfa_id, cname, datatype, pointer(cfa_var_id)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        
        # the variable has been created in the CFA representation, now define
        # the dimensions
        # dimension ids returned in iteration - get the dimension ids from the
        # dimnames
        cfa_dim_ids = (c_int * len(dimensions))()
        d = 0
        for dim in dimensions:
            cdimname = c_char_p(dim.encode())
            cfa_err = CFAPython.lib.cfa_inq_dim_id(
                self._cfa_id, cdimname, byref(cfa_dim_ids, sizeof(c_int)*d)
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            d += 1

        # add the AggregatedDimension names to the AggregationVariable 
        cfa_err = CFAPython.lib.cfa_var_def_dims(
            self._cfa_id, cfa_var_id, len(dimensions), cfa_dim_ids
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)

        var = CFAVariable(self._cfa_id, cfa_var_id)
        # create the netCDF variable - which has no dimensions
        vartype = CFAPython.CFATypeToNumpy(datatype)
        var._nc_object = self._nc_object.createVariable(varname, vartype)
        self._variables.append(var)
        return var

    @property
    def variables(self) -> list[object]:
        """Get the list of CFAVariables in this container (CFAGroup)"""
        return self._variables
    
    def getVariables(self) -> list[object]:
        """Just a wrapper to variables property above"""
        return self.variables

    def getVariable(self, varname: str) -> object:
        """Get a single variable, matching the name"""
        vars = self.variables
        for var in vars:
            if var.name == varname:
                return var
        raise CFAException("Variable {} not found".format(varname))

    def createGroup(self, grpname: str) -> object:
        """Create a group in this group and return the group"""
        cfa_grp_id = c_int(-1)
        cname = c_char_p(grpname.encode())
        cfa_err = CFAPython.lib.cfa_def_cont(
            self._cfa_id, cname, pointer(cfa_grp_id)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        
        grp = CFAGroup(self._cfa_id, cfa_grp_id)
        grp._nc_object = self._nc_object.createGroup(grpname)
        self._groups.append(grp)
        return grp

    @property
    def groups(self) -> list[object]:
        """Get the list of CFAGroups in this container"""
        return self._groups
    
    def getGroups(self) -> list[object]:
        """Wrapper for groups property"""
        return self.groups

    def getGroup(self, grpname: str) -> object:
        """Get a single group by name"""
        grps = self.getGrps()
        for grp in grps:
            if grp.name == grpname:
                return grp
        raise CFAException("Group {} not found".format(grpname))

    @property
    def ngroups(self) -> int:
        """Return the number of containers (groups) in this container (group).
        """
        return self._container.n_conts

    @property
    def nvariables(self) -> int:
        """Return the number of variables in this container."""
        return self._container.n_vars

    @property
    def ndimensions(self) -> int:
        """Return the number of dimensions in this container."""
        return self._container.n_dims

    @property
    def name(self) -> str:
        """Return the name of the group."""
        return self._container.name.decode('utf-8')
    
    @property
    def nc(self) -> object:
        """Return the netcdf object this group maps to"""
        return self._nc_object

    @property
    def nc_id(self) -> object:
        """Return the underlying id (in the C library) of the group this maps to"""
        return self._nc_object._grpid
    
    @property
    def cfa_id(self) -> object:
        """Return the CFA id this group maps to."""
        return self._cfa_id