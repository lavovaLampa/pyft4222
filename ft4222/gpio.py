from ft4222 import CommonHandle
from typing import Generic, List, Type, TypeVar

from wrapper import FtHandle
from wrapper.ft4222 import Ft4222Exception, Ft4222Status, GpioTrigger
from wrapper.ft4222.common import uninitialize

from wrapper.ft4222.gpio import GpioHandle, PortId
from wrapper.ft4222.gpio import get_trigger_status, read, read_trigger_queue, set_input_trigger, set_waveform_mode, write

T = TypeVar('T', bound=CommonHandle[FtHandle])


class Gpio(Generic[T], CommonHandle[GpioHandle]):
    _mode_handle: Type[T]

    def __init__(self, ft_handle: GpioHandle, mode_handle: Type[T]):
        super().__init__(ft_handle)
        self._mode_handle = mode_handle

    def read(self, port_id: PortId) -> bool:
        if self._handle is not None:
            return read(self._handle, port_id)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def write(self, port_id: PortId, state: bool) -> None:
        if self._handle is not None:
            write(self._handle, port_id, state)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def set_input_trigger(self, port_id: PortId, trigger: GpioTrigger) -> None:
        if self._handle is not None:
            set_input_trigger(self._handle, port_id, trigger)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def get_queued_trigger_event_count(self, port_id: PortId) -> int:
        if self._handle is not None:
            return get_trigger_status(self._handle, port_id)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def read_trigger_queue(self, port_id: PortId, max_read_size: int) -> List[GpioTrigger]:
        if self._handle is not None:
            return read_trigger_queue(self._handle, port_id, max_read_size)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def set_waveform_mode(self, enable: bool) -> None:
        if self._handle is not None:
            set_waveform_mode(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized!"
            )

    def close(self) -> None:
        self.uninitialize().close()

    def uninitialize(self) -> T:
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            return self._mode_handle(uninitialize(handle))
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "GPIO has been uninitialized already!"
            )
