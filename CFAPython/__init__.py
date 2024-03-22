import ctypes
from importlib.machinery import EXTENSION_SUFFIXES
import os.path
import netCDF4      # this import has to remain to get the dynamic libraries loaded
from enum import IntEnum

from CFAPython.CFAExceptions import CFAException

# load the CFA-C library
this_path = os.path.dirname(__file__)
libpath = os.path.join(this_path, "cfa" + EXTENSION_SUFFIXES[0])
lib = ctypes.CDLL(libpath)

# define the file format enum
class CFAFileFormat(IntEnum):
    # these values should match those in CFA.h:
    # CFAFileFormat::CFA_NETCDF,
    # CFAFileFormat::CFA_UNKNOWN
    CFANetCDF = 0,
    CFAUnknown = -1

# define the datatype enum
class CFAType(IntEnum):
    # these values must match those in CFA.h
    CFANat    = 0,              # /**< Not A Type */
    CFAByte   = 1,              # /**< signed 1 byte integer */
    CFAChar   = 2,              # /**< ISO/ASCII character */
    CFAShort  = 3,              # /**< signed 2 byte integer */
    CFAInt    = 4,              # /**< signed 4 byte integer */
    #CFALong  = 4,
    CFAFloat  = 5,              # /**< single precision floating point number */
    CFADouble = 6,              # /**< double precision floating point number */
    CFAUByte  = 7,              # /**< unsigned 1 byte int */
    CFAUShort = 8,              # /**< unsigned 2-byte int */
    CFAUInt   = 9,              # /**< unsigned 4-byte int */
    CFAInt64  = 10,             # /**< signed 8-byte int */
    CFAUInt64 = 11,             # /**< unsigned 8-byte int */
    CFAString = 12              # /**< really a char* */

def CFATypeToNumpy(cfa_type: CFAType):
    """Return the specifier required by Numpy (and netCDF4-python) for a CFAType"""
    if cfa_type == CFAType.CFANat:
        raise CFAException(-504)    # not a type (NAT)
    elif cfa_type == CFAType.CFAByte:                # /**< signed 1 byte integer */
        return 'i1'
    elif cfa_type == CFAType.CFAChar:                # /**< ISO/ASCII character */
        return 'c'
    elif cfa_type == CFAType.CFAShort:               # /**< signed 2 byte integer */
        return 'i2'
    elif cfa_type == CFAType.CFAInt:                 # /**< signed 4 byte integer */
        return 'i4'
    #CFALong  = 4,
    elif cfa_type == CFAType.CFAFloat:               # /**< single precision floating point number */
        return 'f4'
    elif cfa_type == CFAType.CFADouble:              # /**< double precision floating point number */
        return 'f8'
    elif cfa_type == CFAType.CFAUByte:               # /**< unsigned 1 byte int */
        return 'u1'
    elif cfa_type == CFAType.CFAUShort:              # /**< unsigned 2-byte int */
        return 'u2'
    elif cfa_type == CFAType.CFAUInt:                # /**< unsigned 4-byte int */
        return 'u4'
    elif cfa_type == CFAType.CFAInt64:               # /**< signed 8-byte int */
        return 'i8'
    elif cfa_type == CFAType.CFAUInt64:              # /**< unsigned 8-byte int */
        return 'u8'
    elif cfa_type == CFAType.CFAString:              # /**< really a char* */
        return str