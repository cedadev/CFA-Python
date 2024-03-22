"""Program to recreate example 3 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFAType

import os.path
import sys

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
    ds = CFADataset(example3_path, mode="w", format=CFAFileFormat.CFANetCDF)

    # add the CFA dimensions (AggregatedDimensions)
    ds.CFA.createDimension("time", CFAType.CFADouble, 12)
    time_var = ds.variables["time"]
    time_var.standard_name = "time"
    time_var.units = "days since 2001-01-01"

    ds.CFA.createDimension("level", CFAType.CFADouble, 1)
    level_var = ds.variables["level"]
    level_var.standard_name = "height_above_mean_sea_level"
    level_var.units = "m"
    
    ds.CFA.createDimension("latitude", CFAType.CFADouble, 73)
    latitude_var = ds.variables["latitude"]
    latitude_var.standard_name = "latitude"
    latitude_var.units = "degrees_north"

    ds.CFA.createDimension("longitude", CFAType.CFADouble, 144)
    longitude_var = ds.variables["longitude"]
    longitude_var.standard_name = "longitude"
    longitude_var.units = "degrees_east"

    # add the CFA group / container
    grp = ds.CFA.createGroup("aggregation")

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as above
    var = ds.CFA.createVariable("temp", CFAType.CFADouble,
                            ("time", "level", "latitude", "longitude"))
    # set the metadata via the .nc member
    var.nc.standard_name = "air_temperature"
    var.nc.units = "K"
    var.nc.cell_methods = "time: mean"

    # set the AggregationInstructions
    var.setAggregationInstruction({
        "location" : ("/aggregation/location", False, CFAType.CFAInt),
        "file"     : ("/aggregation/file", False, CFAType.CFAString),
        "format"   : ("/aggregation/format", True, CFAType.CFAString),
        "address"  : ("/aggregation/address", False, CFAType.CFAString)
    })

    # set the number of Fragments along each AggregatedDimension
    var.setFragmentDefinition([2,1,1,1])
    var.setFragment(
        frag_loc=[0,0,0,0],
        frag={
            "file"    : None, 
            "format"  : None, 
            "address" : "temp1",
        })
    var.setFragment(
        frag_loc=[1,0,0,0],
        frag={
            "file"    : None, 
            "format"  : None, 
            "address" : "temp2", 
        })

    # Variables can now be created in the Dataset, and in the group, and add metadata
    var1 = grp._nc_object.createVariable("temp1", "f8", ("time", "latitude", "longitude"))
    var1.units = "Kelvin"
    var2 = grp._nc_object.createVariable("temp2", "f8", ("time", "latitude", "longitude"))
    var2.units = "degreesC"

    # add the time data for the time dimension
    time_var._nc_object[:] = 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334

    # add the temperature data for the two variables
    var1[0,0,0:6] = 270.3, 272.5, 274.1, 278.5, 280.3, 283.6
    var2[0,0,0:6] = 4.5, 3.0, 0.0, -2.6, -5.6, -10.2
    ds.close()

def example3_load():
    print("Example 3 load")
    # load in the CFA Dataset
    ds = CFADataset(example3_path, mode="r", format=CFAFileFormat.CFANetCDF)

    # get and print the CFA AggregatedDimensions
    time = ds.CFA.getDimension("time")
    print(time.name, time.size, time.type)

    level = ds.CFA.getDimension("level")
    print(level.name, level.size, level.type)

    latitude = ds.CFA.getDimension("latitude")
    print(latitude.name, latitude.size, latitude.type)

    print("----------------")

    # get the temp variable
    var = ds.CFA.getVariable("temp")
    print(var.name)

    # get the AggregatedDimensions
    for d in var.getDimensions():
        print(d.name, d.size, d.type)

    print("----------------")

    # get the fragment definition
    frag_def = var.getFragmentDefinition()
    print(frag_def)

    # get the 1st fragment and output the data
    frag = var.getFragment(frag_loc=[0,0,0,0])
    print("Location: ", frag["location"])
    print("File: ", frag["file"])
    print("Format: ", frag["format"])
    print("Address: ", frag["address"])

    print("----------------")

    # get the 2nd fragment and output the data
    frag = var.getFragment(data_loc=[6,0,0,0])
    print("index: ", frag["index"])
    print("Location: ", frag["location"])
    print("File: ", frag["file"])
    print("Format: ", frag["format"])
    print("Address: ", frag["address"])

    ds.close()

if __name__ == "__main__":
    if sys.argv[1] == "S":
        example3_save()
    elif sys.argv[1] == "L":
        example3_load()
    else:
        raise SystemExit(f"Command line option: {sys.argv[1]} not recognised.")