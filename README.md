# PyFT4222

A libft4222 library python wrapper.

## Building

Run `uv build`.

## Development

### Type-checking

Run `uv run pyright`. Check `pyproject.toml` for pyright configuration (basically strict + additional warnings).

### Linting

Run `ruff check`. Check `pyproject.toml` for enabled rules.

### Formatting

Run `ruff format`.

## Installation

The pyft4222 package can be installed using pip:

```sh
pip install pyft4222
```

Use virtual environment preferably.

### udev rule

The FT4222 device is not accessible by all users by default.
You can create a rule in `/etc/udev/rules.d/50-ftdi.rules` to
make the device available to all users.

```conf
# FTDI's ft4222 USB-I2C Adapter
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="601c", MODE="0660", TAG+="uaccess"
```

## Documentation

Use mypy or other language server that supports Python types.
Library functions are easier to use with type hints.

WIP

## Examples

Open an SPI master stream:

```python
import pyft4222 as ft
from pyft4222.result import Err, Ok
from pyft4222.stream import InterfaceType
from pyft4222.wrapper.spi import ClkPhase, ClkPolarity
from pyft4222.wrapper.spi.master import ClkDiv, SsoMap

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
handle = ft.open_by_idx(0)


# Use `isinstance` in Python 3.9
match handle:
    case Ok(handle):
        # Check if the FT4222 mode is as expected
        if handle.tag == InterfaceType.DATA_STREAM:
            # Initialize FT4222 in SPI master mode using a single-bit
            # full-duplex transfer
            with (
                handle,
                handle.init_single_spi_master(
                    ClkDiv.CLK_DIV_2,
                    ClkPolarity.CLK_IDLE_LOW,
                    ClkPhase.CLK_TRAILING,
                    SsoMap.SS_0,
                ) as spi_master,
            ):
                # Write and read back data simultaneously
                read_data = spi_master.single_read_write(bytes([0x01, 0x02, 0x03, 0x04]))

                print("Data read: ")
                print(read_data)

        else:
            print("FT4222 is in invalid mode!")

    case Err(err):
        print(f"Unable to open handle: {err}")
        exit(1)
```

Open an I2C slave stream:

```python
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

```

Open GPIO stream:

```python
import pyft4222 as ft
from pyft4222.result import Err, Ok
from pyft4222.stream import InterfaceType
from pyft4222.wrapper.gpio import Direction, PortId

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
handle = ft.open_by_idx(0)

# Use `isinstance` in Python 3.9
match handle:
    case Ok(handle):
        # Check if the FT4222 mode is as expected
        if handle.tag == InterfaceType.GPIO:
            # The handle is automatically closed at the end of the scope
            with (
                handle,
                handle.init_gpio(
                    (
                        Direction.INPUT,
                        Direction.INPUT,
                        Direction.OUTPUT,
                        Direction.OUTPUT,
                    )
                ) as gpio,
            ):
                # Disable suspend out, else we cannot control GPIO2
                gpio.set_suspend_out(False)
                # Disable wakeup interrupt, else we cannot control GPIO3
                gpio.set_wakeup_interrupt(False)

                # Set GPIO port 0 into a logical 1 state
                gpio.write(PortId.PORT_0, True)

                # Read GPIO port 1 input state
                port1_state = gpio.read(PortId.PORT_1)
                print(port1_state)

        else:
            print("FT4222 is in invalid mode!")

    case Err(err):
        print(f"Unable to open handle: {err}")
        exit(1)
```
