CFA Classes
===========

Reference implementation of CFA (Climate Forecast Aggregation) Conventions in Python 3 (3.8+).

Installation
------------
(These are temporary installation instructions until I write a setup.py that
will take care of installing the CFA-C library)
CFA-Python requires a compiled version of the CFA-C library to be installed in
the path: 

    ../CFA-C/lib/libcfa.so

This path can be changed in the file:

    CFAPython/__init__/py

Follow these steps to install:

1. Make a common directory

        mkdir CFA

1. Clone the `CFA-C` repository:

        git clone https://github.com/cedadev/CFA-C.git CFA/CFA-C

1. Compile the `CFA-C` shared library

        cd CFA/CFA-C
        make all
        cd ../../

1. Clone the `CFA-Python` repository:

        git clone https://github.com/cedadev/CFA-Python CFA/CFA-Python

1. Run the example

        cd CFA/CFA-Python
        python test/examples/example1.py