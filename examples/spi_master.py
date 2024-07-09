import pyft4222 as ft
from pyft4222.stream import InterfaceType
from pyft4222.wrapper.spi import ClkPhase, ClkPolarity
from pyft4222.wrapper.spi.master import ClkDiv, SsoMap

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
handle = ft.open_by_idx(0).unwrap()

# Check if the FT4222 mode is as expected
if handle.tag == InterfaceType.DATA_STREAM:
    # Initialize FT4222 in SPI master mode using a single-bit
    # full-duplex transfer
    with handle, handle.init_single_spi_master(
        ClkDiv.CLK_DIV_2,
        ClkPolarity.CLK_IDLE_LOW,
        ClkPhase.CLK_TRAILING,
        SsoMap.SS_0,
    ) as spi_master:
        # Write and read back data simultaneously
        read_data = spi_master.single_read_write(bytes([0x01, 0x02, 0x03, 0x04]))

        print("Data read: ")
        print(read_data)

else:
    print("FT4222 is in invalid mode!")
