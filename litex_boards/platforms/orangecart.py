# This file is Copyright (c) 2021 Marcus Comstedt <marcus@mc.pp.se>
# License: BSD

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.dfu import DFUProg

# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("clk48", 0, Pins("C8"),  IOStandard("LVCMOS33")),
    ("rst_n", 0, Pins("M8"), IOStandard("LVCMOS33")),

    ("usr_btn", 0, Pins("F12"), IOStandard("LVCMOS18"), Misc("PULLMODE=UP")),

    ("rgb_led", 0,
        Subsignal("r", Pins("T6"), IOStandard("LVCMOS33")),
        Subsignal("g", Pins("R6"), IOStandard("LVCMOS33")),
        Subsignal("b", Pins("R8"), IOStandard("LVCMOS33")),
    ),

    ("user_led", 0, Pins("T6"), IOStandard("LVCMOS33")), # rgb_led.r
    ("user_led", 1, Pins("R6"), IOStandard("LVCMOS33")), # rgb_led.g
    ("user_led", 2, Pins("R8"), IOStandard("LVCMOS33")), # rgb_led.b

    ("hyperram", 0,
        Subsignal("dq", Pins(
            "G15 B16 C15 D16 C16 F15 F16 E15"),
            IOStandard("LVCMOS18")),
        Subsignal("rwds", Pins("F14"), IOStandard("LVCMOS18")),
        Subsignal("reset_n", Pins("J13"), IOStandard("LVCMOS18")),
        Subsignal("cs_n", Pins("K14"), IOStandard("LVCMOS18")),
        Subsignal("ck_p", Pins("J16"), IOStandard("SSTL18D_II")),
        Subsignal("psc_p", Pins("G16"), IOStandard("SSTL18D_II")),
        Misc("SLEWRATE=FAST")
    ),

    ("usb", 0,
        Subsignal("d_p", Pins("R5"), Misc("PULLMODE=DOWN")),
        Subsignal("d_n", Pins("T4"), Misc("PULLMODE=DOWN")),
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
        Misc("SLEWRATE=FAST"),
        IOStandard("LVCMOS33"),
    ),

    ("sdcard", 0,
        Subsignal("clk",  Pins("A10")),
        Subsignal("cmd",  Pins("E11"), Misc("PULLMODE=UP")),
        Subsignal("data", Pins("C9 E9 C11 B11"), Misc("PULLMODE=UP")),
        Subsignal("cd",   Pins("A11"), Misc("PULLMODE=UP")),
        IOStandard("LVCMOS33"), Misc("SLEWRATE=FAST")
    ),

    ("serial", 0,
        Subsignal("tx", Pins("D8"), IOStandard("LVCMOS33")),
        Subsignal("rx", Pins("E8"), IOStandard("LVCMOS33"))
    ),

    ("c64expansionport", 0,
        Subsignal("d_en_n", Pins("T3")),
        Subsignal("d_dir", Pins("T2")),
        Subsignal("a_en_n", Pins("L1 E2")),
        Subsignal("a_dir", Pins("L5 E1")),

        Subsignal("a", Pins("M6 R4 P4 N4 N5 M5 M3 L4 H5 G4 J1 J2 G1 G2 F1 F2")),
        Subsignal("d", Pins("M1 N3 P2 N1 R3 P1 R2 R1")),
        Subsignal("phi2", Pins("C2")),
        Subsignal("nmi_out", Pins("G5")),
        Subsignal("reset_in_n", Pins("B1")),
        Subsignal("reset_out", Pins("C1")),
        Subsignal("romh_n", Pins("C3")),
        Subsignal("dma_out", Pins("M2")),
        Subsignal("ba", Pins("K2")),
        Subsignal("roml_n", Pins("L2")),
        Subsignal("io2_n", Pins("K1")),
        Subsignal("exrom", Pins("D1")),
        Subsignal("game", Pins("D3")),
        Subsignal("io1_n", Pins("F5")),
        Subsignal("dotclk", Pins("B2")),
        Subsignal("rw_in", Pins("E3")),
        Subsignal("rw_out_n", Pins("F3")),
        Subsignal("irq_out", Pins("F4")),
        IOStandard("LVCMOS33"), Misc("SLEWRATE=SLOW")
    ),

    ("clockport", 0,
        Subsignal("iowr_n", Pins("G3")),
        Subsignal("iord_n", Pins("H3")),
        Subsignal("rtc_cs_n", Pins("H4")),
        Subsignal("spare_cs_n", Pins("J5")),
        IOStandard("LVCMOS33"), Misc("SLEWRATE=SLOW")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    # "Pmod" connector
    ("GPIO", "- B9 B10 C10 A9")
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
        return DFUProg(vid="1209", pid="5a0c", alt="0")

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk48", loose=True), 1e9/48e6)
