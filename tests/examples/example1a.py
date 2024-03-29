"""Program to recreate example 1 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFAType

import os
import sys

# set the example path to be relative to this file
this_path = os.path.dirname(__file__)
example1a_path = os.path.join(this_path, "../../examples/test/example1a.nc")

def example1a_save():
    print("Example 1a save")

    # check the target directory exists
    dir = os.path.dirname(example1a_path)
    if not (os.path.exists(dir)):
        os.mkdir(dir)

    # create the Dataset (AggregationContainer)
    ds = CFADataset(example1a_path, mode="w", format=CFAFileFormat.CFANetCDF)
    # add the CFA dimensions (AggregatedDimensions)
    time_dim = ds.CFA.createDimension("time", CFAType.CFAInt, 12)
    assert(time_dim.nc is ds.dimensions["time"])

    level_dim = ds.CFA.createDimension("level", CFAType.CFADouble, 1)
    assert(level_dim.nc is ds.dimensions["level"])

    latitude_dim = ds.CFA.createDimension("latitude", CFAType.CFADouble, 73)
    assert(latitude_dim.nc is ds.dimensions["latitude"])
    
    longitude_dim = ds.CFA.createDimension("longitude", CFAType.CFADouble, 144)
    assert(longitude_dim.nc is ds.dimensions["longitude"])

    # defining the CFA dimensions also creates the netCDF Dimensions and the 
    # corresponding Dimension Variables.  We can now add metadata and data to these
    # Dimension Variables.
    time_var = ds.variables["time"]
    time_var.standard_name = "time"
    time_var.units = "days since 2001-01-01"

    level_var = ds.variables["level"]
    level_var.standard_name = "height_above_mean_sea_level"
    level_var.units = "m"

    latitude_var = ds.variables["latitude"]
    latitude_var.standard_name = "latitude"
    latitude_var.units = "degrees_north"

    longitude_var = ds.variables["longitude"]
    longitude_var.standard_name = "longitude"
    longitude_var.units = "degrees_east"

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as defined above
    var = ds.CFA.createVariable("temp", CFAType.CFADouble,
                       ("time", "level", "latitude", "longitude"))
    assert(var.nc is ds.variables["temp"])
    
    # set the AggregationInstructions
    var.setAggregationInstruction({
        "location": ("aggregation_location", False, CFAType.CFAInt), 
        "file"    : ("aggregation_file", False, CFAType.CFAString),
        "format"  : ("aggregation_format", True, CFAType.CFAString),
        "address" : ("aggregation_address", False, CFAType.CFAString),
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

    # add the metadata to the netCDF variable
    var.nc.standard_name = "air_temperature"
    var.nc.units = "K"
    var.nc.cell_methods = "time: mean"

    # add the data to the time Dimension Variable
    time_var[:] = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    # don't forget to close the dataset
    ds.close()

def example1a_load():
    print("Example 1a load")
    # load in the CFA Dataset
    ds = CFADataset(example1a_path, mode="r", format=CFAFileFormat.CFANetCDF)

    assert(ds.CFA.nc is ds)

    print("----------------")

    # get and print the CFA AggregatedDimensions
    print("GLOBAL AGGREGATED DIMENSIONS: ")

    cfa_dims = ds.CFA.getDimensions()
    
    for d in cfa_dims:
        assert(d.nc is ds.dimensions[d.name])
        print(d.name, d.size, d.type, d.nc)

    print("----------------")

    # get the temp variable
    var = ds.CFA.getVariable("temp")
    assert(var.nc is ds.variables["temp"])

    print(f"VARIABLE: {var.name} AGGREGATED DIMENSIONS: ")
    # get the AggregatedDimensions
    for d in var.dimensions:
        assert(d.nc is ds.dimensions[d.name])
        print(d.name, d.size, d.type, d.nc)

    print("----------------")
    print(f"FRAGMENT DEFINITION: {var.getFragmentDefinition()}")
    print("----------------")

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

    ds.close()

if __name__ == "__main__":
    if sys.argv[1] == "S":
        example1a_save()
    elif sys.argv[1] == "L":
        example1a_load()
    else:
        raise SystemExit(f"Command line option: {sys.argv[1]} not recognised.")