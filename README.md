CFA Classes
===========

Reference implementation of CFA (Climate Forecast Aggregation) Conventions in Python 3 (3.9+).

Installation
------------

There is now a `setup.py` which will compile and install the required CFA-C 
library.  This superceeds any previous installation instructions.  The user is
no longer required to compile the CFA-C library themselves.

1. Create a virtual environment (can name it anything)

        python3 -m venv CFA-python-venv

1. Activate the virtual environment:

        source CFA-python-venv/bin/activate

1. Clone the `CFA-Python` repository:

        git clone https://github.com/cedadev/CFA-Python.git

1. Go into the clone and install

        cd CFA-Python
        pip install ./

1. Run the example

        python test/examples/example1.py