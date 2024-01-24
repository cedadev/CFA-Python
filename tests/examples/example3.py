"""Program to recreate example 3 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFAType

import os.path

# set the example path to be relative to this file
this_path = os.path.dirname(__file__)
example3_path = os.path.join(this_path, "../../examples/test/example3.nc")

def example3_save():
    print("Example 3 save")

    # check the target directory exists
    dir = os.path.dirname(example3_path)
    if not (os.path.exists(dir)):
        os.mkdir(dir)

    # create the Dataset (AggregationContainer)
    cfa = CFADataset(example3_path, CFAFileFormat.CFANetCDF, "w")

    # add the CFA dimensions (AggregatedDimensions)
    cfa.addDim("time", CFAType.CFADouble, 12)
    cfa.addDim("level", CFAType.CFADouble, 1)
    cfa.addDim("latitude", CFAType.CFADouble, 73)
    cfa.addDim("longitude", CFAType.CFADouble, 144)

    # add the CFA group / container
    grp = cfa.addGrp("aggregation")

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as above
    var = cfa.addVar("temp", CFAType.CFADouble,
                     ("time", "level", "latitude", "longitude"))

    # set the AggregationInstructions
    var.setAggInstr(location="/aggregation/location", 
                    file="/aggregation/file",
                    format="/aggregation/format", format_scalar=True,
                    address="/aggregation/address")

    # set the number of Fragments along each AggregatedDimension
    var.setFragNum([2,1,1,1])
    var.setFrag(frag_loc=[0,0,0,0],
                file=None, format=None, address="temp1", units="")
    var.setFrag(frag_loc=[1,0,0,0],
                file=None, format=None, address="temp2", units="")

    # note that the temp2 local variable has not been created as that would
    # require interfacing with the Python netCDF-4 routines, which I have yet
    # to write / figure out how to do
    print("----------------")

def example3_load():
    print("Example 3 load")
    # load in the CFA Dataset
    cfa = CFADataset(example3_path, CFAFileFormat.CFANetCDF, "r")

    # get and print the CFA AggregatedDimensions
    time = cfa.getDim("time")
    print(time.name, time.len, time.type)
    level = cfa.getDim("level")
    print(level.name, level.len, level.type)
    latitude = cfa.getDim("latitude")
    print(latitude.name, latitude.len, latitude.type)

    print("----------------")

    # get the temp variable
    var = cfa.getVar("temp")
    print(var.name)

    # get the AggregatedDimensions
    for d in var.getDims():
        print(d.name, d.len, d.type)

    print(var.getFragDef())

    print("----------------")

    # get the fragment definition
    frag_def = var.getFragDef()
    print(frag_def)

    # get the 1st fragment and output the data
    frag = var.getFrag(frag_loc=[0,0,0,0])
    print("Location: ", frag.location)
    print("File: ", frag.file)
    print("Format: ", frag.format)
    print("Address: ", frag.address)
    print("Units: ", frag.units)
    print("Dtype: ", frag.cfa_dtype)

    print("----------------")

    # get the 2nd fragment and output the data
    frag = var.getFrag(data_loc=[6,0,0,0])
    print("index: ", frag.index)
    print("Location: ", frag.location)
    print("File: ", frag.file)
    print("Format: ", frag.format)
    print("Address: ", frag.address)
    print("Units: ", frag.units)
    print("Dtype: ", frag.cfa_dtype)

if __name__ == "__main__":
    #example3_save()
    example3_load()