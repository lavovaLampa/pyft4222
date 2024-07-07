import pyft4222 as ft
from pyft4222.gpio import Gpio
from pyft4222.result import Err, Ok
from pyft4222.stream import InterfaceType
from pyft4222.wrapper.gpio import Direction, PortId

# Print out list of connected devices
for dev in ft.get_device_info_list():
    print(dev)

# Open device using 'device index'
result = ft.open_by_idx(0)

# Check if it was opened successfully
# If using Python < 3.10, use "isinstance(dev, Ok)"
match result:
    case Ok(handle):
        # Check if the FT4222 mode is as expected
        if handle.tag == InterfaceType.GPIO:
            # The handle is automatically closed at the end of the scope
            with handle:
                # The handle is automatically uninitialized at the end of the scope
                with handle.init_gpio(
                    (
                        Direction.INPUT,
                        Direction.INPUT,
                        Direction.OUTPUT,
                        Direction.OUTPUT,
                    )
                ) as gpio:
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
        print("Couldn't open the handle")
        print(err)
