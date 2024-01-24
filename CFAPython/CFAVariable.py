from __future__ import annotations
from collections import namedtuple

import CFAPython
from CFAPython import CFAType
import CFAPython._CFADatatypes as CFADatatypes
from CFAPython.CFAExceptions import CFAException
from CFAPython.CFADimension import CFADimension

from ctypes import *

class CFAVariable:
    def __init__(self, parent_id: int = -1, id: int = -1):
        """Create a CFA Variable from a parent_id and an id"""
        self.__parent_id = parent_id
        self.__cfa_id = id

    @property
    def _variable(self) -> object:
        """Get the underlying CFA-C AggregationVariable for this CFAVariable.
        Hidden as we don't users to access this method."""
        cfa_var = CFADatatypes.C_AggregationVariable()
        cfa_var_p = pointer(cfa_var)
        cfa_err = CFAPython.lib.cfa_get_var(
            self.__parent_id, self.__cfa_id, pointer(cfa_var_p)
        )
        if (cfa_err != 0):
            raise CFAException(cfa_err)
        return cfa_var_p.contents

    @property
    def name(self) -> str:
        """Return the name of the variable"""
        return self._variable.name.decode('utf-8')

    @property
    def ndims(self) -> int:
        """Get the number of dimensions the variable is defined over"""
        return self._variable.cfa_ndim
    
    @property
    def ninstr(self) -> int:
        """Get the number of Aggregation Instructions"""
        return self._variable.n_instr

    @property
    def _dim_ids(self) -> list[int]:
        """Get the CFADimension ids that this CFAVariable is defined over"""
        variable = self._variable
        dimids = []
        for d in range(0, self.ndims):
            dimids.append(variable.cfa_dim_idp[d])
        return dimids

    def setAggInstr(self, agg_instrs: dict) -> None:
        """Set the aggration instructions - that is the location, file, format,
        and address fields in the AggregationInstructions associated with this
        variable, as well as arbitrary aggregation instructions."""
        for item, value in agg_instrs.items():
            cterm = c_char_p(item.encode())
            cdata = c_char_p(value[0].encode())
            cscalar = value[1]
            ctype = c_int(value[2])
            cfa_err = CFAPython.lib.cfa_var_def_agg_instr(
                self.__parent_id, self.__cfa_id,
                cterm, cdata, cscalar, ctype
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)

    def setFragNum(self, frag_def: list[int]) -> None:
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

    def setFrag(self, frag_loc: iter = None, data_loc: iter = None,
                frag: dict = None) -> None:
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
            data_loc_c = (c_size_t * len(data_loc))(0)
            for d in range(0, len(data_loc)):
                data_loc_c[d] = data_loc[d]
        else:
            data_loc_c = None

        for item, value in frag.items():
            cterm = c_char_p(item.encode())

            c_agg_instr = CFADatatypes.C_AggregationInstruction()
            c_agg_instr_p = pointer(c_agg_instr)
            # get the AggregationInstruction type
            cfa_err = CFAPython.lib.cfa_var_get_agg_instr(
                self.__parent_id, self.__cfa_id,
                cterm, pointer(c_agg_instr_p)
            )
            if cfa_err != 0:
                raise CFAException(cfa_err)
            
            # switch on the type to get the data in the correct format
            T = c_agg_instr_p.contents.type.type
            length = 1
            if T == CFAType.CFANat:
                raise CFAException(-504)
            elif T == CFAType.CFAByte:
                cdata = pointer(c_byte(value))
            elif T == CFAType.CFAChar:
                cdata = pointer(c_char(value))
            elif T == CFAType.CFAShort:
                cdata = pointer(c_short(value))
            elif T == CFAType.CFAInt:
                cdata = pointer(c_int(value))
            elif T == CFAType.CFAFloat:
                cdata = pointer(c_float(value))
            elif T == CFAType.CFADouble:
                cdata = pointer(c_double(value))
            elif T == CFAType.CFAUByte:
                cdata = pointer(c_ubyte(value))
            elif T == CFAType.CFAUShort:
                cdata = pointer(c_ushort(value))
            elif T == CFAType.CFAUInt:
                cdata = pointer(c_uint(value))
            elif T == CFAType.CFAInt64:
                cdata = pointer(c_longlong(value))
            elif T == CFAType.CFAUInt64:
                cdata = pointer(c_ulonglong(value))
            elif T == CFAType.CFAString:
                cdata = c_char_p(value.encode())
                length = c_int(len(value)+1)
            else:
                # not a type error
                raise CFAException(-504)

            cfa_err = CFAPython.lib.cfa_var_put1_frag(
                    self.__parent_id, self.__cfa_id,
                    frag_loc_c, data_loc_c,
                    cterm, cdata, length
            )
            if cfa_err != 0:
                raise CFAException(cfa_err)

    def getDims(self) -> list[object]:
        """Get the list of CFADimensions defined for this variable"""
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
            frag_dim = CFADatatypes.C_FragmentDimension()
            frag_dim_p = pointer(frag_dim)
            cfa_err = CFAPython.lib.cfa_var_get_frag_dim(
                    self.__parent_id, self.__cfa_id, d, pointer(frag_dim_p)
            )
            if (cfa_err != 0):
                raise CFAException(cfa_err)
            frag_def.append(frag_dim_p.contents.length)
        return frag_def

    def getFragDimLen(self, dimname: str) -> int:
        """Get the number of fragments along a particular dimensions"""
        frag_dim_lens = self.getFragDef()
        dims = self.getDims()
        for d in range(0, len(dims)):
            if dims[d].name == dimname:
                return frag_dim_lens[d]
        raise CFAException("Dimension {} not found".format(dimname))

    def getFrag(self, frag_loc: list[int] = [], 
                data_loc: list[int] = []) -> object:
        """Get a fragment in a CFAVariable, either from a Fragment Location,
        or a Data Location."""

        # create the fragment location as a pointer to a size_t array
        if len(frag_loc) != 0:
            frag_loc_c = (c_size_t * len(frag_loc))(0)
            for d in range(0, len(frag_loc)):
                frag_loc_c[d] = frag_loc[d]
        else:
            frag_loc_c = None

        # create the data location as a pointer to a size_t array
        if len(data_loc) != 0:
            data_loc_c = (c_size_t * len(data_loc))(0)
            for d in range(0, len(data_loc)):
                data_loc_c[d] = data_loc[d]
        else:
            data_loc_c = None

        # return the fragment as a dictionary - need to get the value for
        # each key in the AggregationInstructions
        V = self._variable
        cfa_frag = {} # return dictionary

        # Get the index - this is outside the terms
        cdata = (c_size_t * self.ndims)(0)
        cfa_err = CFAPython.lib.cfa_var_get1_frag(
            self.__parent_id, self.__cfa_id, frag_loc_c, data_loc_c,
            "index".encode(), cdata,
        )
        data = [cdata[d] for d in range(0, self.ndims)]
        cfa_frag["index"] = data

        for i in range(0, self.ninstr):
            # get the term from the aggregation
            cterm = V.cfa_instructionsp[i].term
            T = V.cfa_instructionsp[i].type.type
            term = cterm.decode()
            data = None

            if term == "location":
                # Get the location (in the Aggregated Data)
                data_loc_dims = 2 * self.ndims
                cdata = (c_size_t * data_loc_dims)(0)
                cfa_err = CFAPython.lib.cfa_var_get1_frag(
                    self.__parent_id, self.__cfa_id, frag_loc_c, data_loc_c,
                    cterm, cdata,
                )
                # transform data
                data = [cdata[d] for d in range(0, self.ndims)]
            else:
                if T == CFAType.CFANat:
                    raise CFAException(-504)
                elif T == CFAType.CFAByte:
                    cdata = pointer(c_byte(0))
                elif T == CFAType.CFAChar:
                    cdata = pointer(c_char(0))
                elif T == CFAType.CFAShort:
                    cdata = pointer(c_short(0))
                elif T == CFAType.CFAInt:
                    cdata = pointer(c_int(0))
                elif T == CFAType.CFAFloat:
                    cdata = pointer(c_float(0))
                elif T == CFAType.CFADouble:
                    cdata = pointer(c_double(0))
                elif T == CFAType.CFAUByte:
                    cdata = pointer(c_ubyte(0))
                elif T == CFAType.CFAUShort:
                    cdata = pointer(c_ushort(0))
                elif T == CFAType.CFAUInt:
                    cdata = pointer(c_uint(0))
                elif T == CFAType.CFAInt64:
                    cdata = pointer(c_longlong(0))
                elif T == CFAType.CFAUInt64:
                    cdata = pointer(c_ulonglong(0))
                elif T == CFAType.CFAString:
                    cdata = c_char_p(1*1024)
                else:
                    # not a type error
                    raise CFAException(-504)
                
                cfa_err = CFAPython.lib.cfa_var_get1_frag(
                    self.__parent_id, self.__cfa_id, frag_loc_c, data_loc_c,
                    cterm, pointer(cdata)
                )
                if (cfa_err != 0):
                    raise CFAException(cfa_err)
                
                if T == CFAType.CFAString:
                    data = cdata.value.decode('utf-8')
                else:
                    data = cdata.contents.value
                                
            cfa_frag[term] = data
            
        return cfa_frag