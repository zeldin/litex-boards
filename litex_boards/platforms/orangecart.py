# This file is Copyright (c) 2021 Marcus Comstedt <marcus@mc.pp.se>
# License: BSD

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.dfu import DFUProg

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("clk48", 0, Pins("C8"),  IOStandard("LVCMOS33")),
    ("rst_n", 0, Pins("M8"), IOStandard("LVCMOS33")),

    ("usr_btn", 0, Pins("F12"), IOStandard("SSTL18_I")),

    ("rgb_led", 0,
        Subsignal("r", Pins("T6"), IOStandard("LVCMOS33")),
        Subsignal("g", Pins("R6"), IOStandard("LVCMOS33")),
        Subsignal("b", Pins("R8"), IOStandard("LVCMOS33")),
    ),

    ("user_led", 0, Pins("T6"), IOStandard("LVCMOS33")), # rgb_led.r
    ("user_led", 1, Pins("R6"), IOStandard("LVCMOS33")), # rgb_led.g
    ("user_led", 2, Pins("R8"), IOStandard("LVCMOS33")), # rgb_led.b

    ("usb", 0,
        Subsignal("d_p", Pins("R5")),
        Subsignal("d_n", Pins("T4")),
        Subsignal("pullup", Pins("N6")),
        IOStandard("LVCMOS33")
    ),

    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("N8"), IOStandard("LVCMOS33")),
        #Subsignal("clk",  Pins("N9"), IOStandard("LVCMOS33")),
        Subsignal("dq",   Pins("T8 T7 M7 N7"), IOStandard("LVCMOS33")),
    ),
    ("spiflash", 0,
        Subsignal("cs_n", Pins("N8"), IOStandard("LVCMOS33")),
        #Subsignal("clk",  Pins("N9"), IOStandard("LVCMOS33")), # Note: CLK is bound using USRMCLK block
        Subsignal("miso", Pins("T7"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("T8"), IOStandard("LVCMOS33")),
        Subsignal("wp",   Pins("M7"), IOStandard("LVCMOS33")),
        Subsignal("hold", Pins("N7"), IOStandard("LVCMOS33")),
    ),

    ("spisdcard", 0,
        Subsignal("clk",  Pins("A10")),
        Subsignal("mosi", Pins("E11"), Misc("PULLMODE=UP")),
        Subsignal("cs_n", Pins("B11"), Misc("PULLMODE=UP")),
        Subsignal("miso", Pins("C9"), Misc("PULLMODE=UP")),
        Misc("SLEW=FAST"),
        IOStandard("LVCMOS33"),
    ),

    ("sdcard", 0,
        Subsignal("clk",  Pins("A10")),
        Subsignal("cmd",  Pins("E11"), Misc("PULLMODE=UP")),
        Subsignal("data", Pins("C9 E9 C11 B11"), Misc("PULLMODE=UP")),
        IOStandard("LVCMOS33"), Misc("SLEW=FAST")
    ),

    ("serial", 0,
        Subsignal("tx", Pins("D8"), IOStandard("LVCMOS33")),
        Subsignal("rx", Pins("E8"), IOStandard("LVCMOS33"))
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
]



# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk48"
    default_clk_period = 1e9/48e6

    def __init__(self, revision=None, device="25F", **kwargs):
        self.revision = revision
        io         = _io
        connectors = _connectors
        LatticePlatform.__init__(self, f"LFE5U-{device}-6BG256C", io, connectors, **kwargs)

    def create_programmer(self):
        return DFUProg(vid="1209", pid="000c", alt="0") # FIXME

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk48", loose=True), 1e9/48e6)
