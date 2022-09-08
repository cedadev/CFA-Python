import ctypes
from importlib.machinery import EXTENSION_SUFFIXES
import os.path

from enum import IntEnum

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
class CFADataType(IntEnum):
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
    CFAUInt64 = 11              # /**< unsigned 8-byte int */
