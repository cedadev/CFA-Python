from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import (C_AggregationVariable, C_FragmentDimension,
                                     C_Fragment)
from CFAPython.CFAExceptions import CFAException
from CFAPython.CFADimension import CFADimension
from CFAPython.CFAFragment import CFAFragment

from ctypes import c_size_t, pointer, c_char_p, c_int

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
        cfa_err = CFAPython.lib.cfa_get_var(
            self.__parent_id, self.__cfa_id, pointer(cfa_var_p)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_var_p[0]

    @property
    def name(self) -> str:
        """Return the name of the variable"""
        return self._variable.name.decode('utf-8')

    @property
    def ndims(self) -> str:
        """Get the number of dimensions the variable is defined over"""
        return self._variable.cfa_ndim

    @property
    def _dim_ids(self) -> list[int]:
        """Get the CFADimension ids that this CFAVariable is defined over"""
        variable = self._variable
        dimids = []
        for d in range(0, self.ndims):
            dimids.append(variable.cfa_dim_idp[d])
        return dimids

    def setAggInstr(self, 
                    location = "", location_scalar = False,
                    file = "", 
                    format = "", format_scalar = False,
                    address = ""):
        """Set the aggration instructions - that is the location, file, format,
        and address fields in the AggregationInstructions associated with this
        variable."""
        if len(location) > 0:
            cinstruction = c_char_p("location".encode())
            cvalue = c_char_p(location.encode())
            cfa_err = CFAPython.lib.cfa_var_def_agg_instr(
                self.__parent_id, self.__cfa_id,
                cinstruction, cvalue, 
                location_scalar
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)

        if len(file) > 0:
            cinstruction = c_char_p("file".encode())
            cvalue = c_char_p(file.encode())
            cfa_err = CFAPython.lib.cfa_var_def_agg_instr(
                self.__parent_id, self.__cfa_id,
                cinstruction, cvalue,
                False
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)

        if len(format) > 0:
            cinstruction = c_char_p("format".encode())
            cvalue = c_char_p(format.encode())
            cfa_err = CFAPython.lib.cfa_var_def_agg_instr(
                self.__parent_id, self.__cfa_id,
                cinstruction, cvalue,
                format_scalar
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)

        if len(address) > 0:
            cinstruction = c_char_p("address".encode())
            cvalue = c_char_p(address.encode())
            cfa_err = CFAPython.lib.cfa_var_def_agg_instr(
                self.__parent_id, self.__cfa_id,
                cinstruction, cvalue,
                False
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)

    def setFragNum(self, frag_def: list[int]):
        """Set the Fragment definitions, i.e. how many times each dimension
        is subdivided."""
        # create the fragment location as a pointer to a size_t array
        if len(frag_def) != 0:
            frag_def_c = (c_int * len(frag_def))(0)
            for d in range(0, len(frag_def)):
                frag_def_c[d] = frag_def[d]
        else:
            frag_def_c = None
        cfa_err = CFAPython.lib.cfa_var_def_frag_num(
            self.__parent_id, self.__cfa_id, frag_def_c
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)

    def setFrag(self, frag_loc: list[int] = [], data_loc: list[int] = [],
                file: str = "", format: str = "", 
                address: str = "", units: str = ""):
        """Set the data for a fragment"""
        # create the fragment location as a pointer to a size_t array
        if frag_loc and len(frag_loc) != 0:
            frag_loc_c = (c_size_t * len(frag_loc))(0)
            for d in range(0, len(frag_loc)):
                frag_loc_c[d] = frag_loc[d]
        else:
            frag_loc_c = None

        # create the data location as a pointer to a size_t array
        if data_loc and len(data_loc) != 0:
            data_loc_c = (c_size_t * len(data_loc))(c_size_t(0))
            for d in range(0, len(data_loc)):
                data_loc_c[d] = data_loc[d]
        else:
            data_loc_c = None

        # create all the details as C strings
        if file and len(file) > 0:
            cfile = c_char_p(file.encode())
        else:
            cfile = None
        if address and len(address) > 0:
            caddress = c_char_p(address.encode())
        else:
            caddress = None
        if format and len(format) > 0:
            cformat = c_char_p(format.encode())
        else:
            cformat = None
        if units and len(units) > 0:
            cunits = c_char_p(units.encode())
        else:
            cunits = None

        cfa_err = CFAPython.lib.cfa_var_put1_frag(
                self.__parent_id, self.__cfa_id,
                frag_loc_c,
                data_loc_c,
                cfile,
                cformat,
                caddress,
                cunits
        )
        if cfa_err != 0:
            raise CFAException(cfa_err)

    def getDims(self) -> list[object]:
        """Get the list of CFADimensions defined for this variable"""
        variable = self._variable
        dims = []
        for d in self._dim_ids:
            dims.append(CFADimension(self.__parent_id, d))
        return dims

    def getDim(self, dimname: str) -> object:
        """Get a single dimension attached to this variable, matching the
        name"""
        dims = self.getDims()
        for dim in dims:
            if dim.name == dimname:
                return dim
        raise CFAException("Dimension {} not found".format(dimname))

    def getDimName(self, dimnum: int) -> str:
        """Get the name of a dimension attached to this variable"""
        dims = self.getDims()
        if dimnum >= len(dims):
            raise CFAException(
                "Dimension number {} is out of range".format(dimnum)
            )
        return dims[dimnum].name
        
    def getFragDef(self) -> list[int]:
        """Get the fragment definition for this variable.  This returns a
        list of integers, the length of the number of dimensions this variable
        is defined over.  Each element in the list is the number of times the
        corresponding dimension is divided by."""
        frag_def = []
        for d in range(0, self.ndims):
            # get the fragment definition
            frag_dim = C_FragmentDimension()
            frag_dim_p = pointer(frag_dim)
            cfa_err = CFAPython.lib.cfa_var_get_frag_dim(
                    self.__parent_id, self.__cfa_id, d, pointer(frag_dim_p)
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            frag_def.append(frag_dim_p[0].length)
        return frag_def

    def getFragDimLen(self, dimname: str) -> int:
        """Get the number of fragments along a particular dimensions"""
        frag_dim_lens = self.getFragDef()
        dims = self.getDims()
        for d in range(0, len(dims)):
            if dims[d].name == dimname:
                return frag_dim_lens[d]
        raise CFAException("Dimension {} not found".format(dimname))

    def getFrag(self, frag_loc: list[int] = [], data_loc: list[int] = []):
        """Get a fragment in a CFAVariable, either from a Fragment Location,
        or a Data Location."""
        # create the return fragment
        frag = C_Fragment()
        frag_p = pointer(frag)

        # create the fragment location as a pointer to a size_t array
        if len(frag_loc) != 0:
            frag_loc_c = (c_size_t * len(frag_loc))(0)
            for d in range(0, len(frag_loc)):
                frag_loc_c[d] = frag_loc[d]
        else:
            frag_loc_c = None

        # create the data location as a pointer to a size_t array
        if len(data_loc) != 0:
            data_loc_c = (c_size_t * len(data_loc))(c_size_t(0))
            for d in range(0, len(data_loc)):
                data_loc_c[d] = data_loc[d]
        else:
            data_loc_c = None

        cfa_err = CFAPython.lib.cfa_var_get1_frag(
            self.__parent_id, self.__cfa_id, frag_loc_c, data_loc_c,
            pointer(frag_p)
        )
        
        if (cfa_err != 0):
            raise CFAException(cfa_err)        
        return CFAFragment(frag_p[0], self.ndims)