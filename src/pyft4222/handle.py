from abc import ABC
from contextlib import AbstractContextManager
from types import TracebackType
from typing import Any, Generic, Optional, Type, TypeVar

from pyft4222.wrapper import (
    OS_TYPE,
    Ft4222Exception,
    Ft4222Status,
    FtHandle,
    GpioTrigger,
)
from pyft4222.wrapper.common import (
    ClockRate,
    InitializedHandle,
    SwChipVersion,
    chip_reset,
    get_clock,
    get_version,
    set_clock,
    set_interrupt_trigger,
    set_suspend_out,
    set_wakeup_interrupt,
    uninitialize,
)
from pyft4222.wrapper.ftd2xx import (
    BufferType,
    DriverVersion,
    ShortDeviceInfo,
    close_handle,
    get_device_info,
    purge_buffers,
    reset_device,
)

if OS_TYPE == "Windows":
    from pyft4222.wrapper.ftd2xx import get_driver_version

HandleType = TypeVar("HandleType", bound=FtHandle)
ContextType = TypeVar("ContextType")


class GenericHandle(
    Generic[HandleType, ContextType], AbstractContextManager[ContextType], ABC
):
    """An abstract class encapsulating common FT4222 functions."""

    _handle: Optional[HandleType]

    def __init__(self, ft_handle: HandleType):
        """Initialize GenericHandle with given FtHandle.

        Args:
            ft_handle:      Handle to an opened FT4222 device
        """
        self._handle = ft_handle

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if self._handle is not None:
            self.close()

        return False

    def close(self) -> None:
        """Close the current FT4222 handle.

        Note:
            A FT4222 stream must be opened again after calling this method.

        Raises:
            FtException:    In case of unexpected error
        """
        if self._handle is not None:
            close_handle(self._handle)
            self._handle = None

    def set_clock(self, clk_rate: ClockRate) -> None:
        """Set the FT4222 system clock frequency.

        Args:
            clk_rate:   Clock frequency to set

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_clock(self._handle, clk_rate)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def get_clock(self) -> ClockRate:
        """Get the current FT4222 system clock frequency.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            ClockRate:          System clock frequency
        """
        if self._handle is not None:
            return get_clock(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def set_suspend_out(self, enable: bool) -> None:
        """Enable or disable 'suspend out' function.

        By enabling the 'suspend out' function, the FT4222 will signalize
        entrance into suspend mode on GPIO2 pin.

        Warning:
            GPIO access is not possible while 'suspend out' function is enabled.

        Args:
            enable:     Enable 'suspend out' function?

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_suspend_out(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def set_wakeup_interrupt(self, enable: bool) -> None:
        """Enable or disable a wake-up/interrupt function.

        When wake-up/interrupt function is enabled, the GPIO3 acts
        as an input pin.
        While system is in normal mode, the GPIO3 acts as an interrupt pin.
        While system is in suspend mode, the GPIO3 acts as a wake-up pin.

        Warning:
            GPIO access is not possible while wake-up/interrupt is enabled.

        Args:
            enable:     Enable wake-up/interrupt function?

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_wakeup_interrupt(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def set_interrupt_trigger(self, trigger: GpioTrigger) -> None:
        """Set the trigger condition for wake-up/interrupt function.

        Note:
            By default, the trigger condition is 'GpioTrigger.RISING'.

        Warning:
            In case the device is suspended and the GPIO3 functions as interrupt,
            only 'GpioTrigger.RISING' and 'GpioTrigger.FALLING'
            modes are supported.
            The 'GpioTrigger.LEVEL_LOW' and 'GpioTrigger.LEVEL_HIGH' modes
            will react to edges instead!

        Args:
            trigger:        A wake-up/interrupt trigger to set

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_interrupt_trigger(self._handle, trigger)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def get_version(self) -> SwChipVersion:
        """Get version of the FT4222 chip and library.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SwChipVersion:      Version of FT4222 chip and library
        """
        if self._handle is not None:
            return get_version(self._handle)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def get_device_info(self) -> ShortDeviceInfo:
        """Get information about this opened device.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            ShortDeviceInfo:    Info about device belonging to the owned handle
        """
        if self._handle is not None:
            result = get_device_info(self._handle)
            if result is not None:
                return result
            else:
                raise Ft4222Exception(Ft4222Status.OTHER_ERROR, "Unknown error!")
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    if OS_TYPE == "Windows":

        def get_driver_version(self) -> DriverVersion:
            """Get D2XX driver version.

            Raises:
                Ft4222Exception:    In case of unexpected error

            Returns:
                DriverVersion:      Return driver version info
            """
            if self._handle is not None:
                return get_driver_version(self._handle)
            else:
                raise Ft4222Exception(
                    Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
                )

    def reset_device(self) -> None:
        """Send a reset command to the device.

        Note:
            This command closes the owned handle.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            reset_device(self._handle)
            # Handle must be closed after the device is reset
            self.close()
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def purge_buffers(self, buffer_mask: BufferType) -> None:
        """Purge the selected device buffers.

        Args:
            buffer_mask:    OR-mask selecting the buffer types to purge

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            purge_buffers(self._handle, buffer_mask)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )

    def chip_reset(self) -> None:
        """Software reset the FT4222 device.

        Note:
            This command closes the owned handle.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            chip_reset(self._handle)
            # Handle must be closed after the device is reset
            self.close()
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "This handle is closed!"
            )


InitializedHandleType = TypeVar("InitializedHandleType", bound=InitializedHandle)
StreamHandleType = TypeVar("StreamHandleType", bound=GenericHandle[FtHandle, Any])


class GenericProtocolHandle(
    Generic[InitializedHandleType, ContextType, StreamHandleType],
    GenericHandle[InitializedHandleType, ContextType],
    ABC,
):
    _stream_handle: StreamHandleType
    """Reference to the used stream handle"""

    def __init__(
        self, ft_handle: InitializedHandleType, stream_handle: StreamHandleType
    ):
        super().__init__(ft_handle)
        self._stream_handle = stream_handle

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if self._handle is not None:
            self.uninitialize()

        return False

    def close(self) -> None:
        """Un-initialize and close the owned handle.

        Note:
            A new handle must be opened and initialized
            after calling this method.

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        self.uninitialize().close()

    def uninitialize(self) -> StreamHandleType:
        """Un-initialize the owned handle from the current stream mode.

        The handle can be initialized into any other supported mode.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            C:                  A class encapsulating the opened stream type

        """
        if self._handle is not None:
            new_handle = uninitialize(self._handle)
            self._stream_handle._handle = new_handle
            self._handle = None
            return self._stream_handle
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED,
                "Handle is already uninitialized or invalid!",
            )
