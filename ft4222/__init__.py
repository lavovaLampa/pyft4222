from abc import ABC
from typing import Generic, Optional, TypeVar

from wrapper import SYSTEM_TYPE, FtHandle
from wrapper.ftd2xx import DriverVersion, PurgeType, ShortDeviceInfo, close_handle, get_device_info, get_driver_version, purge_buffers, reset_device
from wrapper.ft4222 import Ft4222Exception, Ft4222Status, GpioTrigger
from wrapper.ft4222.common import ClockRate, Version, chip_reset, get_clock, get_version, set_clock, set_interrupt_trigger, set_suspend_out, set_wakeup_interrupt

T = TypeVar('T', bound=FtHandle)


class CommonHandle(Generic[T], ABC):
    _handle: Optional[T]

    def __init__(self, ft_handle: T):
        self._handle = ft_handle

    def close(self) -> None:
        if self._handle is not None:
            close_handle(self._handle)
            self._handle = None
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is already closed!"
            )

    def set_clock(self, clk_rate: ClockRate) -> None:
        if self._handle is not None:
            set_clock(self._handle, clk_rate)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def get_clock(self) -> ClockRate:
        if self._handle is not None:
            return get_clock(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def set_suspend_out(self, enable: bool) -> None:
        if self._handle is not None:
            set_suspend_out(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def set_wakeup_interrup(self, enable: bool) -> None:
        if self._handle is not None:
            set_wakeup_interrupt(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def set_interrupt_trigger(self, trigger: GpioTrigger) -> None:
        if self._handle is not None:
            set_interrupt_trigger(self._handle, trigger)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def get_version(self) -> Version:
        if self._handle is not None:
            return get_version(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def get_device_info(self) -> ShortDeviceInfo:
        if self._handle is not None:
            result = get_device_info(self._handle)
            if result is not None:
                return result
            else:
                raise Ft4222Exception(
                    Ft4222Status.OTHER_ERROR,
                    "Unknown error!"
                )
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    if SYSTEM_TYPE == "Windows":
        def get_driver_version(self) -> DriverVersion:
            if self._handle is not None:
                return get_driver_version(self._handle)
            else:
                raise Ft4222Exception(
                    Ft4222Status.DEVICE_NOT_OPENED,
                    "This handle is closed!"
                )

    def reset_device(self) -> None:
        if self._handle is not None:
            reset_device(self._handle)
            # Handle must be closed after the device is reset
            self.close()
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def purge(self, purge_type_mask: PurgeType) -> None:
        if self._handle is not None:
            purge_buffers(self._handle, purge_type_mask)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )

    def chip_reset(self) -> None:
        if self._handle is not None:
            chip_reset(self._handle)
            self._handle = None
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "This handle is closed!"
            )
