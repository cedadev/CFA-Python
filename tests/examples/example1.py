"""Program to recreate example 1 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFAType

import os

# set the example path to be relative to this file
this_path = os.path.dirname(__file__)
example1_path = os.path.join(this_path, "../../examples/test/example1.nc")

def example1_save():
    print("Example 1 save")

    # check the target directory exists
    dir = os.path.dirname(example1_path)
    if not (os.path.exists(dir)):
        os.mkdir(dir)

    # create the Dataset (AggregationContainer)
    ds = CFADataset(example1_path, mode="w", format=CFAFileFormat.CFANetCDF)
    # add the CFA dimensions (AggregatedDimensions)
    time = ds.CFA.createDimension("time", CFAType.CFAInt, 12)
    assert(time.nc is ds.dimensions["time"])

    level = ds.CFA.createDimension("level", CFAType.CFADouble, 1)
    assert(level.nc is ds.dimensions["level"])

    latitude = ds.CFA.createDimension("latitude", CFAType.CFADouble, 73)
    assert(latitude.nc is ds.dimensions["latitude"])
    
    longitude = ds.CFA.createDimension("longitude", CFAType.CFADouble, 144)
    assert(longitude.nc is ds.dimensions["longitude"])

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as above
    var = ds.CFA.createVariable("temp", CFAType.CFADouble,
                       ("time", "level", "latitude", "longitude"))
    assert(var.nc is ds.variables["temp"])
    # add the metadata to the netCDF variable
    var.nc.standard_name = "air_temperature"
    var.nc.units = "K"
    var.nc.cell_methods = "time: mean"
    
    # set the AggregationInstructions
    var.setAggregationInstruction({
        "location": ("aggregation_location", False, CFAType.CFAInt), 
        "file"    : ("aggregation_file", False, CFAType.CFAString),
        "format"  : ("aggregation_format", True, CFAType.CFAString),
        "address" : ("aggregation_address", False, CFAType.CFAString)
    })

    # set the number of Fragments along each AggregatedDimension
    var.setFragmentDefinition([2,1,1,1])
    var.setFragment(
        frag_loc=[0,0,0,0], 
        frag={
            "file"   : "January-June.nc", 
            "format" : "nc", 
            "address": "temp"
        })
    var.setFragment(
        frag_loc=[1,0,0,0],
        frag={
            "file"   : "July-December.nc", 
            "format" : "nc", 
            "address": "temp"
        })
    print("----------------")

def example1_load():
    print("Example 1 load")
    # load in the CFA Dataset
    ds = CFADataset(example1_path, mode="r", format=CFAFileFormat.CFANetCDF)

    assert(ds.CFA.nc is ds)

    # get and print the CFA AggregatedDimensions
    print("GLOBAL CFA DIMENSIONS: ")

    time = ds.CFA.getDimension("time")
    assert(time.nc is ds.dimensions["time"])
    print(time.name, time.size, time.type, time.nc)

    level = ds.CFA.getDimension("level")
    assert(level.nc is ds.dimensions["level"])
    print(level.name, level.size, level.type, level.nc)

    latitude = ds.CFA.getDimension("latitude")
    assert(latitude.nc is ds.dimensions["latitude"])
    print(latitude.name, latitude.size, latitude.type, latitude.nc)

    longitude = ds.CFA.getDimension("longitude")
    assert(longitude.nc is ds.dimensions["longitude"])
    print(longitude.name, longitude.size, longitude.type, longitude.nc)

    print("----------------")

    # get the temp variable
    var = ds.CFA.getVariable("temp")
    assert(var.nc is ds.variables["temp"])

    print(f"VARIABLE {var.name} DIMENSIONS: ")
    # get the AggregatedDimensions
    for d in var.dimensions:
        print(d.name, d.size, d.type, d.nc)

    print(f"FRAGMENT DEFINITION: {var.getFragmentDefinition()}")
    print("----------------")

    # get the fragment definition
    frag_def = var.getFragmentDefinition()

    # get the 1st fragment and output the data
    frag = var.getFragment(frag_loc=[0,0,0,0])
    print("Index: ", frag["index"])
    print("Location: ", frag["location"])
    print("File: ", frag["file"])
    print("Format: ", frag["format"])
    print("Address: ", frag["address"])
    print("----------------")

    # get the 2nd fragment and output the data
    frag = var.getFragment(data_loc=[6,0,0,0])
    print("Index: ", frag["index"])
    print("Location: ", frag["location"])
    print("File: ", frag["file"])
    print("Format: ", frag["format"])
    print("Address: ", frag["address"])

if __name__ == "__main__":
    example1_save()
    #example1_load()