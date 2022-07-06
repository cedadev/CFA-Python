### ctypes declarations of typthe structs used in the CFA-C library
from ctypes import *
# These values MUST match the #defines in the cfa.h header file
MAX_VARS = 256
MAX_DIMS = 256
MAX_CONTS = 256

class C_AggregationContainer(Structure):
    _fields_ = [("cfa_varids", c_int * MAX_VARS),
                ("n_vars", c_int),
                ("cfa_dimids", c_int * MAX_DIMS),
                ("n_dims", c_int),
                ("cfa_contids", c_int * MAX_CONTS),
                ("n_conts", c_int),
                ("path", c_char_p), 
                ("format", c_int),
                ("x_id", c_int),
                ("serialised", c_int),
                ("name", c_char_p)
            ]

class C_DataType(Structure):
    # cfa_type is just typedef for int
    _fields_ = [("type", c_int),
                ("size", c_size_t)
            ]

class C_AggregatedDimension(Structure):
    _fields_ = [("name", c_char_p),
                ("length", c_int),
                ("cfa_dtype", C_DataType)
            ]

class C_AggregationVariable(Structure):
    _fields_ = [("name", c_char_p),
                ("cfa_ndim", c_int),
                ("cfa_dim_idp", pointer(c_int)),
                ("cfa_frag_dim_idp", pointer(c_int)),
                ("cfa_dtype", C_DataType),
#                ("cfa_datap", AggregatedData),
#                ("cfa_instructionsp", AggregationInstructions)
            ]