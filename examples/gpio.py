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
    handle = dev.ok

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
