from __future__ import annotations

import CFAPython
from CFAPython._CFADatatypes import C_Fragment

class CFAFragment:
    def __init__(self, frag: C_Fragment):
        self.fragment = frag

    @property
    def address(self):
        return self.fragment.address.decode('utf-8')