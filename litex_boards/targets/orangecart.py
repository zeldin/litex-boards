#!/usr/bin/env python3

# This file is Copyright (c) Marcus Comstedt <marcus@mc.pp.se>
# License: BSD

import os
import sys
import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import orangecart

from litex.build.lattice.trellis import trellis_args, trellis_argdict

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.soc_sdram import *
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        clk48_raw = platform.request("clk48")

        reset_delay = Signal(64, reset=int(sys_clk_freq*500e-6))
        self.clock_domains.cd_por = ClockDomain()
        self.reset = Signal()

        self.clock_domains.cd_sys = ClockDomain()

        platform.add_period_constraint(self.cd_sys.clk, 1e9/sys_clk_freq)

        # POR reset logic- POR generated from sys clk, POR logic feeds sys clk
        # reset.
        self.comb += [
            self.cd_por.clk.eq(self.cd_sys.clk),
            self.cd_sys.rst.eq(reset_delay != 0),
        ]

        self.submodules.pll = pll = ECP5PLL()
        pll.register_clkin(clk48_raw, 48e6)

        pll.create_clkout(self.cd_sys, sys_clk_freq, 0)

        self.sync.por += \
            If(reset_delay != 0,
                reset_delay.eq(reset_delay - 1)
            )
        self.specials += AsyncResetSynchronizer(self.cd_por, self.reset)


# BaseSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCCore):
    def __init__(self, revision=None, device="25F", hyperram_device="S70KS1281",
                 sys_clk_freq=int(48e6), toolchain="trellis", **kwargs):
        platform = orangecart.Platform(revision=revision, device=device ,toolchain=toolchain)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq,
            ident          = "LiteX SoC on OrangeCart",
            ident_version  = True,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        # HyperRAM -------------------------------------------------------------------------------
        if not self.integrated_main_ram_size:
            raise Exception("HyperRAM not implemented yet")

        # Leds -------------------------------------------------------------------------------------
        self.submodules.leds = LedChaser(
            pads         = Cat(*[platform.request("user_led", i) for i in range(3)]),
            sys_clk_freq = sys_clk_freq)
        self.add_csr("leds")

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC on OrangeCart")
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    parser.add_argument("--toolchain", default="trellis", help="Gateware toolchain to use, trellis (default) or diamond")
    builder_args(parser)
    soc_sdram_args(parser)
    trellis_args(parser)
    parser.add_argument("--sys-clk-freq", default=48e6,         help="System clock frequency (default=48MHz)")
    parser.add_argument("--device",       default="25F",        help="ECP5 device (default=25F)")
    parser.add_argument("--hyperram-device", default="S70KS1281", help="HyperRAM device (default=S70KS1281)")
    parser.add_argument("--with-spi-sdcard", action="store_true", help="Enable SPI-mode SDCard support")
    args = parser.parse_args()

    soc = BaseSoC(
        toolchain    = args.toolchain,
        device       = args.device,
        hyperram_device = args.hyperram_device,
        sys_clk_freq = int(float(args.sys_clk_freq)),
        **soc_sdram_argdict(args))
    if args.with_spi_sdcard:
        soc.add_spi_sdcard()
    builder = Builder(soc, **builder_argdict(args))
    builder_kargs = trellis_argdict(args) if args.toolchain == "trellis" else {}
    builder.build(**builder_kargs, run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".bit"))

if __name__ == "__main__":
    main()
