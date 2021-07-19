from ctypes import cdll
from ctypes import POINTER, byref
from ctypes import c_void_p, c_uint, c_bool, c_uint16

from enum import IntEnum, auto
from pathlib import Path
from typing import Final, List, NewType, Tuple

from . import Ft4222Status, GpioTrigger
from .. import FtHandle

MODULE_PATH: Final[Path] = Path(__file__).parent

try:
    ftlib = cdll.LoadLibrary(
        str(MODULE_PATH / '..' / 'dlls' / 'libft4222.so.1.4.4.44'))
except OSError as e:
    print("Unable to load shared library!")
    exit(1)

GpioHandle = NewType('GpioHandle', c_void_p)

_GPIO_COUNT: Final[int] = 4


class Direction(IntEnum):
    GPIO_OUTPUT = 0,
    GPIO_INPUT = auto()


class PortId(IntEnum):
    PORT_0 = 0
    PORT_1 = auto()
    PORT_2 = auto()
    PORT_3 = auto()


_init = ftlib.FT4222_GPIO_Init
_init.argtypes = [c_void_p, c_uint * 4]
_init.restype = Ft4222Status

_read = ftlib.FT4222_GPIO_Read
_read.argtypes = [c_void_p, c_uint, POINTER(c_bool)]
_read.restype = Ft4222Status

_write = ftlib.FT4222_GPIO_Write
_write.argtypes = [c_void_p, c_uint, c_bool]
_write.restype = Ft4222Status

_set_input_trigger = ftlib.FT4222_GPIO_SetInputTrigger
_set_input_trigger.argtypes = [c_void_p, c_uint, c_uint]
_set_input_trigger.restype = Ft4222Status

_get_trigger_status = ftlib.FT4222_GPIO_GetTriggerStatus
_get_trigger_status.argtypes = [c_void_p, c_uint, POINTER(c_uint16)]
_get_trigger_status.restype = Ft4222Status

_read_trigger_queue = ftlib.FT4222_GPIO_ReadTriggerQueue
_read_trigger_queue.argtypes = [
    c_void_p, c_uint, POINTER(c_uint), c_uint16, POINTER(c_uint16)]
_read_trigger_queue.restype = Ft4222Status

_set_waveform_mode = ftlib.FT4222_GPIO_SetWaveFormMode
_set_waveform_mode.argtypes = [c_void_p, c_bool]
_set_waveform_mode.restype = Ft4222Status


# FIXME: Better argument typing!
def init(
    ft_handle: FtHandle,
    dirs: Tuple[Direction, Direction, Direction, Direction]
) -> GpioHandle:
    """Initialize the GPIO interface of the FT4222H.

    NOTE: The GPIO interface is available on the 2nd USB interface in mode 0 or on the 4th USB interface in mode 1.

    Args:
        ft_handle:      Handle to an opened FT4222 device
        dirs:           Tuple of directions to be set for each GPIO index - [0, 1, 2, 3]

    Raises:
        RuntimeError:   TODO

    Returns:
        GpioHandle:     Handle to initialized FT4222 device in GPIO mode
    """
    dir_array = (c_uint * _GPIO_COUNT)(dirs)

    result: Ft4222Status = _init(ft_handle, dir_array)

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')

    return GpioHandle(ft_handle)


def read(ft_handle: GpioHandle, port_id: PortId) -> bool:
    """Read the status of a specified GPIO pin or interrupt register.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in GPIO mode
        port_id:        GPIO port index

    Raises:
        RuntimeError:   TODO

    Returns:
        bool:           Is the port active/high?
    """
    gpio_state = c_bool()

    result: Ft4222Status = _read(
        ft_handle,
        port_id,
        byref(gpio_state)
    )

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')

    return gpio_state.value


def write(ft_handle: GpioHandle, port_id: PortId, state: bool) -> None:
    """Write value to the specified GPIO pin.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in GPIO mode
        port_id:        GPIO port index
        state:          State to set

    Raises:
        RuntimeError:   TODO
    """
    result: Ft4222Status = _write(
        ft_handle,
        port_id,
        state
    )

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')


def set_input_trigger(
    ft_handle: GpioHandle,
    port_id: PortId,
    trigger: GpioTrigger
) -> None:
    """Set software trigger conditions on the specified GPIO pin.

    This function allows developers to monitor value changes of the GPIO pins.
    Values that satisfy the trigger condition will be stored in a queue.

    For example, if 'FT4222.GpioTrigger.RISING' is set on 'PortId.GPIO_0',
    and 'PortId.GPIO_0' then changes value from 0 to 1,
    the event GPIO_TRIGGER_RISING will be recorded into the queue.

    Developers can query the queue status using 'GPIO.get_trigger_status()' and 'GPIO.read_trigger_queue()' functions.

    NOTE: This function can only set GPIO trigger conditions.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in GPIO mode
        port_id:        GPIO port index
        trigger:        Trigger type mask (using OR operator)

    Raises:
        RuntimeError:   TODO
    """
    result: Ft4222Status = _set_input_trigger(
        ft_handle,
        port_id,
        trigger
    )

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')


def get_trigger_status(ft_handle: GpioHandle, port_id: PortId) -> int:
    """Get the size of trigger event queue.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in GPIO mode
        port_id:        GPIO port index

    Raises:
        RuntimeError:   TODO

    Returns:
        int:            Number of triggers in event queue for selected GPIO port
    """
    queue_size = c_uint16()

    result: Ft4222Status = _get_trigger_status(
        ft_handle,
        port_id,
        byref(queue_size)
    )

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')

    return queue_size.value


def read_trigger_queue(
    ft_handle: GpioHandle,
    port_id: PortId,
    max_read_size: int
) -> List[GpioTrigger]:
    """Get events recorded in the trigger event queue.

    After calling this function, all events will be removed from the event queue.

    Args:
        ft_handle:                  Handle to an initialized FT4222 device in GPIO mode
        port_id:                    GPIO port index
        max_read_size:              Number of event to read from queue

    Raises:
        RuntimeError:               TODO

    Returns:
        List[FT4222.GpioTrigger]:   List of trigger events (if any)
    """
    event_buffer = (c_uint * max_read_size)()
    events_read = c_uint16()

    result: Ft4222Status = _read_trigger_queue(
        ft_handle,
        port_id,
        event_buffer,
        len(event_buffer),
        byref(events_read)
    )

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')

    return list(map(lambda x: GpioTrigger(x), event_buffer[:events_read.value]))


def set_waveform_mode(ft_handle: GpioHandle, enable: bool) -> None:
    """Enable or disable WaveForm Mode.

    When WaveForm mode is enabled, the device will record all GPIO status periodically.
    The peeking time depends on the system clock.
    The default setting of WaveForm mode is disabled.

    Args:
        ft_handle:      Handle to an initialized FT4222 device in GPIO mode
        enable:         Enable WaveForm mode?

    Raises:
        RuntimeError:   TODO
    """
    result: Ft4222Status = _set_waveform_mode(ft_handle, enable)

    if result != Ft4222Status.OK:
        raise RuntimeError('TODO')
