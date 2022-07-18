from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_Fragment

class CFAFragment:
    def __init__(self, frag: C_Fragment):
        self.fragment = frag

    @property
    def location(self):
        raise NotImplementedError

    @property
    def index(self):
        raise NotImplementedError

    @property
    def file(self):
        raise NotImplementedError

    @property
    def format(self):
        raise NotImplementedError

    @property
    def address(self):
        if self.fragment.address:
            return self.fragment.address.decode('utf-8')
        else:
            return None

    @property
    def units(self):
        raise NotImplementedError

    @property
    def cfa_dtype(self):
        raise NotImplementedError