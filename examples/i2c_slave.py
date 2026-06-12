import pyft4222 as ft
from pyft4222.result import Err, Ok
from pyft4222.stream import InterfaceType

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
handle = ft.open_by_idx(0)

# Use `isinstance` in Python 3.9
match handle:
    case Ok(handle):
        if handle.tag == InterfaceType.DATA_STREAM:
            # Initialize the FT4222 in I2C slave mode
            # The handle is uninitialized automatically at the end of scope
            with handle, handle.init_i2c_slave() as iic_slave:
                # Set an I2C device address
                iic_slave.set_address(0x0340)

                # Write data into the device buffer
                iic_slave.write(bytes([0xFF, 0x01, 0x02, 0x03]))

        else:
            print("FT4222 is in invalid mode!")

    case Err(err):
        print(f"Unable to open handle: {err}")
        exit(1)

