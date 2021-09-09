# PyFT4222

A libft4222 library python wrapper.

# Description



# Building



# Installation

The pyft4222 package can be installed using pip:

```
pip install pyft4222
```

Use virtual environment prefferably.


## udev rule

The FT4222 device is not accesible by all users by default.
You can create a rule in `/etc/udev/rules.d/99-ftdi.conf` to
make the device available to all users.

```
# FTDI's ft4222 USB-I2C Adapter
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="601c", GROUP="plugdev", MODE="0666"
```

# Documentation

Use mypy or other language server that supports Python types.
Library functions are easier to use with type hints.

WIP


# Examples

Open an SPI master stream:

```python
import pyft4222 as ft
from pyft4222.stream import InterfaceType
from pyft4222.wrapper import ResType
from pyft4222.wrapper.spi import ClkPhase, ClkPolarity
from pyft4222.wrapper.spi.master import ClkDiv, SsoMap

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
dev = ft.open_by_idx(0)

# Check if it was opened successfully
if dev.tag == ResType.OK:
    handle = dev.result

    # Check if the FT4222 mode is as expected
    if handle.tag == InterfaceType.DATA_STREAM:
        # Initialize FT4222 in spi master mode using a single-bit
        # full-duplex transfer
        spi_master = handle.init_single_spi_master(
            ClkDiv.CLK_DIV_2,
            ClkPolarity.CLK_IDLE_LOW,
            ClkPhase.CLK_TRAILING,
            SsoMap.SS_0,
        )

        # Write and read back data simultaneously
        read_data = spi_master.single_read_write(bytes([0x01, 0x02, 0x03, 0x04]))

        print("Data read:")
        print(read_data)

        # Close the device handle
        spi_master.close()
    else:
        print("FT4222 is in invalid mode!")
else:
    print("Couldn't open the handle")
    print(dev.err)
```

Open an I2C slave stream:

```python
import pyft4222 as ft
from pyft4222.stream import InterfaceType
from pyft4222.wrapper import ResType

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
dev = ft.open_by_idx(0)

# Check if it was opened successfully
if dev.tag == ResType.OK:
    handle = dev.result

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
```

Open GPIO stream:

```python
import pyft4222 as ft
from pyft4222.stream import InterfaceType
from pyft4222.wrapper import ResType
from pyft4222.wrapper.gpio import Direction, PortId

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
dev = ft.open_by_idx(0)

# Check if it was opened successfully
if dev.tag == ResType.OK:
    handle = dev.result

    # Check if the FT4222 mode is as expected
    if handle.tag == InterfaceType.GPIO:
        gpio = handle.init_gpio(
            (
                Direction.OUTPUT,
                Direction.INPUT,
                Direction.OUTPUT,
                Direction.OUTPUT,
            )
        )
        # Disable suspend out, else we cannot control GPIO2
        gpio.set_suspend_out(False)
        # Disable wakeup interrupt, else we cannot control GPIO3
        gpio.set_wakeup_interrupt(False)

        # Set GPIO port 0 into a logical 1 state
        gpio.write(PortId.PORT_0, True)

        # Read GPIO1 input state
        port1_state = gpio.read(PortId.PORT_1)
        print(port1_state)

        # Close the device handle
        gpio.close()
    else:
        print("FT4222 is in invalid mode!")
else:
    print("Couldn't open the handle")
    print(dev.err)
```

