This directory (CFA/examples) contains the example from the CFA 0.6 document
(include link to document here), in CDL format.  

They can be converted to valid netCDF4 by running the command:

    ncgen -4 example?.cdl

There is also a Makefile.  Individual examples can be converted using:

    make example?.nc

Or, to make all the examples:

   make
