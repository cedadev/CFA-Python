from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_Fragment
from ctypes import cast, c_size_t, pointer, POINTER

class CFAFragment:
    def __init__(self, frag: C_Fragment, ndims: int):
        # we need the number of dimensions to form the returns of the index
        # and location
        self.__ndims = ndims
        self.__fragment = frag

    @property
    def location(self) -> list[(int, int)]:
        """Return the location in the Dataset of the Fragment.
        This is returned as a list of pairs.  List length is the number of
        dimensions, the pairs contain (start, stop)"""
        if self.__fragment.location:
            loc_list = []
            loc = self.__fragment.location
            for d in range(0, self.__ndims):
                loc_list.append((loc[d*2], loc[d*2+1]))
            return loc_list
        else:
            return None

    @property
    def index(self):
        """Return the fragment index - i.e. which position in the fragments
        array that this fragment occupies"""
        if self.__fragment.index:
            idx_list = []
            idx = self.__fragment.index
            for d in range(0, self.__ndims):
                idx_list.append(idx[d])
            return idx_list
        else:
            return None

    @property
    def file(self):
        """Return the file of the fragment"""
        if self.__fragment.file:
            return self.__fragment.file.decode('utf-8')
        else:
            return None

    @property
    def format(self):
        """Return the format of the fragment"""
        if self.__fragment.format:
            return self.__fragment.format.decode('utf-8')
        else:
            return None

    @property
    def address(self):
        """Return the address (variable) of the fragment"""
        if self.__fragment.address:
            return self.__fragment.address.decode('utf-8')
        else:
            return None

    @property
    def units(self):
        """Return the units that the fragment is in"""
        if self.__fragment.units:
            return self.__fragment.units.decode('utf-8')
        else:
            return None

    @property
    def cfa_dtype(self):
        """Return an integer representing the type.
        See cfa.h for more details.  These also match the nctypes from netCDF"""
        if self.__fragment.cfa_dtype:
            return self.__fragment.cfa_dtype.type
        else:
            return None
