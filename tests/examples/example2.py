"""Program to recreate example 2 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFAType

import os.path

# set the example path to be relative to this file
this_path = os.path.dirname(__file__)
example2_path = os.path.join(this_path, "../../examples/test/example2.nc")

def example2_save():
    print("Example 2 save")

    # check the target directory exists
    dir = os.path.dirname(example2_path)
    if not (os.path.exists(dir)):
        os.mkdir(dir)

    # create the Dataset (AggregationContainer)
    ds = CFADataset(example2_path, mode="w", format=CFAFileFormat.CFANetCDF)

    # add the CFA dimensions (AggregatedDimensions)
    time_dim = ds.CFA.createDimension("time", CFAType.CFADouble, 12)
    time_var = ds.variables["time"]
    time_var.standard_name = "time"
    time_var.units = "days since 2001-01-01"

    level_dim = ds.CFA.createDimension("level", CFAType.CFADouble, 1)
    level_var = ds.variables["level"]
    level_var.standard_name = "height_above_mean_sea_level"
    level_var.units = "m"

    latitude_dim = ds.CFA.createDimension("latitude", CFAType.CFADouble, 73)
    latitude_var = ds.variables["latitude"]
    latitude_var.standard_name = "latitude"
    latitude_var.units = "degrees_north"

    longitude_dim = ds.CFA.createDimension("longitude", CFAType.CFADouble, 144)
    longitude_var = ds.variables["longitude"]
    longitude_var.standard_name = "longitude"
    longitude_var.units = "degrees_east"

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as above
    var = ds.CFA.createVariable("temp", CFAType.CFAShort,
                       ("time", "level", "latitude", "longitude"))
    assert(var.nc is ds.variables["temp"])

    # set the AggregationInstructions
    var.setAggregationInstruction({
        "location" : ("aggregation_location", False, CFAType.CFAInt),
        "file"     : ("aggregation_file", False, CFAType.CFAString),
        "format"   : ("aggregation_format", True, CFAType.CFAString),
        "address"  : ("aggregation_address", False, CFAType.CFAString),
    })

    # set the number of Fragments along each AggregatedDimension
    var.setFragmentDefinition([2,1,1,1])
    var.setFragment(
        frag_loc=[0,0,0,0],
        frag={
            "file"   : "January-June.nc", 
            "format" : "nc", 
            "address": "temp", 
        })
    var.setFragment(
        frag_loc=[1,0,0,0],
        frag={
            "file"   : None,
            "format" : None,
            "address": "temp2",
        }
    )

    # Variables can be created in the Dataset
    temp2_var = ds.createVariable("temp2", "f8", ("time", "latitude", "longitude"))
    temp2_var.units = "degreesC"
    temp2_var[0, 0, 0:6] = [4.5, 3.0, 0.0, -2.6, -5.6, -10.2]

    print("----------------")
    ds.close()

def example2_load():
    print("Example 2 load")
    # load in the CFA Dataset
    ds = CFADataset(example2_path, mode="r", format=CFAFileFormat.CFANetCDF)

    # get and print the CFA AggregatedDimensions
    time = ds.CFA.getDimension("time")
    print(time.name, time.size, time.type)

    level = ds.CFA.getDimension("level")
    print(level.name, level.size, level.type)

    latitude = ds.CFA.getDimension("latitude")
    print(latitude.name, latitude.size, latitude.type)

    longitude = ds.CFA.getDimension("longitude")
    print(longitude.name, longitude.size, longitude.type)

    print("----------------")

    # get the temp variable
    var = ds.CFA.getVariable("temp")
    print(var.name)

    # get the AggregatedDimensions
    for d in var.getDimensions():
        print(d.name, d.size, d.type)

    print(var.getFragmentDefinition())

    print("----------------")

    # get the fragment definition
    frag_def = var.getFragmentDefinition()
    print(frag_def)

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
    example2_save()
    example2_load()