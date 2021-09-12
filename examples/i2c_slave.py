import pyft4222 as ft
from pyft4222.stream import InterfaceType
from pyft4222.wrapper import Result

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
dev = ft.open_by_idx(0)

# Check if it was opened successfully
if dev.tag == Result.OK:
    handle = dev.ok

    # Check if the FT4222 mode is as expected
    if handle.tag == InterfaceType.DATA_STREAM:
        # Initialize FT4222 in I2C slave mode
        i2c_slave = handle.init_i2c_slave()
        # Set an I2C device address
        i2c_slave.set_address(0x0340)

        # Write data into the device buffer
        i2c_slave.write(bytes([0xFF, 0x01, 0x02, 0x03]))

        # Finally, close the device handle
        i2c_slave.close()
    else:
        print("FT4222 is in invalid mode!")
else:
    print("Couldn't open the handle")
    print(dev.err)
