"""Program to recreate example 1 from the CFA documentation"""
from CFAPython.CFADataset import CFADataset
from CFAPython import CFAFileFormat
from CFAPython import CFADataType

example1_path = "examples/test/example1.nc"

def example1_save():
    print("Example 1 save")

    # create the Dataset (AggregationContainer)
    cfa = CFADataset(example1_path, CFAFileFormat.CFANetCDF, "w")

    # add the CFA dimensions (AggregatedDimensions)
    cfa.addDim("time", CFADataType.CFADouble, 12)
    cfa.addDim("level", CFADataType.CFADouble, 1)
    cfa.addDim("latitude", CFADataType.CFADouble, 145)
    cfa.addDim("longitude", CFADataType.CFADouble, 192)

    # add the CFA variable (AggregationVariable), with the AggregatedDimensions
    # as above
    var = cfa.addVar("temp", CFADataType.CFADouble,
                     ("time", "level", "latitude", "longitude"))

    # set the AggregationInstructions
    var.setAggInstr(location="aggregation_location", 
                    file="aggregation_file",
                    format="aggregation_format", format_scalar=True,
                    address="aggregation_address")

    # set the number of Fragments along each AggregatedDimension
    var.setFragNum([2,1,1,1])
    var.setFrag(frag_loc=[0,0,0,0],
                file="January-June.nc", format="nc", address="temp", units="")
    var.setFrag(frag_loc=[1,0,0,0],
                file="July-December.nc", format="nc", address="temp", units="")
    print("----------------")

def example1_load():
    print("Example 1 load")
    # load in the CFA Dataset
    cfa = CFADataset(example1_path, CFAFileFormat.CFANetCDF, "r")

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

    # get the 1st fragment and output the data
    frag = var.getFrag([0,0,0,0])
    print("Location: ", frag.location)
    print("File: ", frag.file)
    print("Format: ", frag.format)
    print("Address: ", frag.address)
    print("Units: ", frag.units)
    print("Dtype: ", frag.cfa_dtype)

    print("----------------")

    # get the 2nd fragment and output the data
    frag = var.getFrag([1,0,0,0])
    print("Location: ", frag.location)
    print("File: ", frag.file)
    print("Format: ", frag.format)
    print("Address: ", frag.address)
    print("Units: ", frag.units)
    print("Dtype: ", frag.cfa_dtype)

if __name__ == "__main__":
    example1_save()
    example1_load()