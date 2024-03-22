class CFAException(Exception):
    """Generic CFA Exception.  Outputs sensible error message."""
    def __init__(self, code: int, *args):
        super().__init__(args)
        self.code = code

    def __str__(self):
        # trap any netCDF error first
        if self.code > -500:
            return f"NetCDF error : ({self.code})"

        # specific CFA errors
        if self.code == -500:
            error_string = "memory error"
        elif self.code == -501:
            error_string = "memory leak"
        elif self.code == -502:
            error_string = "bounds error in dynamic array"
        elif self.code == -503:
            error_string = "end of string found"
        elif self.code == -504:
            error_string = "not a CFAType"
        elif self.code == -510:
            error_string = "CFAContainer not found"
        elif self.code == -520:
            error_string = "CFADimension not found"
        elif self.code == -530:
            error_string = "CFAVariable not found"
        elif self.code == -531:
            error_string = "aggregation instructions not found"
        elif self.code == -532:
            error_string = "fragments have already been defined"
        elif self.code == -533:
            error_string = "fragments are not defined"
        elif self.code == -534:
            error_string = "fragment dimension not found"
        elif self.code == -535:
            error_string = "fragment not found"
        elif self.code == -536:
            error_string = "no fragment index given or defined"
        elif self.code == -537:
            error_string = "fragment datum not found"
        elif self.code == -540:
            error_string = "unsupported CFA file format"
        elif self.code == -541:
            error_string = "not a CFA file"
        elif self.code == -542:
            error_string = "unsupported CFA version in file"
        elif self.code == -543:
            error_string = "input or output file not created"
        elif self.code == -550:
            error_string = "aggregation data attribute error"
        elif self.code == -551:
            error_string = "aggregation dimension attribute error"
        elif self.code == -552:
            error_string = "aggregration instructions not defined"
        elif self.code == -553:
            error_string = "unrecognised aggregation instruction"

        return f"CFA error : {error_string} ({self.code})"