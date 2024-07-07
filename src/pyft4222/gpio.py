from pyft4222.handle import GenericProtocolHandle, StreamHandleType
from pyft4222.wrapper import Ft4222Exception, Ft4222Status, GpioTrigger
from pyft4222.wrapper.gpio import (
    GpioHandle,
    PortId,
    get_trigger_status,
    read,
    read_trigger_queue,
    set_input_trigger,
    set_waveform_mode,
    write,
)


class Gpio(GenericProtocolHandle[GpioHandle, StreamHandleType]):
    """A class encapsulating GPIO functions."""

    def read(self, port_id: PortId) -> bool:
        """Read state of the given GPIO port.

        Args:
            port_id:            ID of the port to read

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bool:               Port state (True -> '1', False -> '0')
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        return read(self._handle, port_id)

    def write(self, port_id: PortId, state: bool) -> None:
        """Set state of the given GPIO port.

        Args:
            port_id:    ID of the port to set
            state:      New port state (True -> '1', False -> '0')

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        write(self._handle, port_id, state)

    def set_input_trigger(self, port_id: PortId, triggers: GpioTrigger) -> None:
        """Set software trigger conditions for the selected GPIO port.

        Args:
            port_id:        GPIO port ID
            triggers:       OR-map of triggers to enable

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        set_input_trigger(self._handle, port_id, triggers)

    def get_queued_trigger_event_count(self, port_id: PortId) -> int:
        """Get the size of trigger event queue.

        Args:
            port_id:            GPIO port ID

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of pending events in the event queue
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        return get_trigger_status(self._handle, port_id)

    def read_trigger_queue(
        self, port_id: PortId, event_read_count: int
    ) -> list[GpioTrigger]:
        """Read events from the trigger event queue.

        Args:
            port_id:            GPIO port ID
            event_read_count:   Number of events to read from queue

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            list[GpioTrigger]:  List of trigger events
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        return read_trigger_queue(self._handle, port_id, event_read_count)

    def set_waveform_mode(self, enable: bool) -> None:
        """Enable or disable the waveform mode.

        TODO: Add description

        Args:
            enable:             Enable waveform mode?

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is None:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

        set_waveform_mode(self._handle, enable)
