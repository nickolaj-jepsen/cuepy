from ctypes import WinDLL

from cuepy.calls import perform_protocol_handshake, get_device_count, get_device_info, get_led_positions, \
    get_led_id_for_key_name, set_leds_color, request_control, get_last_error
from cuepy.exceptions import error_id

from cuepy.stuct import LedColor


class CorsairSDK(object):
    """
    Class that represents an SDK connection
    """

    def __init__(self, corsair_sdk_dll_path):
        """
        Create a new SDK object and perform the protocol handshake

        :param corsair_sdk_dll_path: Path to a sdk dll that matches the python version
        :type corsair_sdk_dll_path: str
        """
        self._corsair_sdk_path = corsair_sdk_dll_path
        self.corsair_sdk = WinDLL(corsair_sdk_dll_path)
        self._perform_protocol_handshake()

    def _raise_corsair_error(self, error=None, message=""):
        """
        Raise error message based on the last reported error from the SDK

        :param error: specify error type
        :type error: int
        :param message: specify error message
        :type message: str
        """
        if error is None:
            error = self.last_error()
        raise error(message)

    def _perform_protocol_handshake(self):
        """
        Perform handshake with the CUE

        :returns: info about the sdk
        :rtype: dict
        """
        return perform_protocol_handshake(self.corsair_sdk)

    def device_count(self):
        """
        Find amount of CUE devices

        :returns: amount of CUE devices
        :rtype: int
        """
        device_count = get_device_count(self.corsair_sdk)
        if device_count == -1:
            self._raise_corsair_error()
        return device_count

    def led_id_from_char(self, char):
        """
        Get id of a led by the letter
        Only between A-Z

        :param char: Character to find led_id from
        :type char: str
        :returns: id for led
        :rtype: int
        """
        led_id = get_led_id_for_key_name(self.corsair_sdk, bytes(char))
        if led_id == 0:
            self._raise_corsair_error()
        return led_id

    def set_led(self, led_id, color):
        """
        Set color of an led

        :param led_id: id of led to set color
        :type led_id: int
        :param color: list of rgb values of new colors. eg. [255, 255, 255]
        :type color: list
        :returns: true if successful
        :rtype: bool
        """
        if not set_leds_color(self.corsair_sdk, LedColor(led_id, *color)):
            self._raise_corsair_error()
        return True

    def set_multiple_leds(self, led_dict):
        """
        Set color of a dict of leds

        :param led_dict: a dict of leds and colors. eg. {1: [255, 255, 255]}
        :type led_dict: dict
        :returns: true if successful
        :rtype: bool
        """
        raise NotImplementedError

    def request_control(self, device_id, access_mode=True):
        """
        Request exclusive control of device

        :param device_id: id of device
        :type device_id: int
        :param access_mode: True=exclusive, False=shared
        :type access_mode: bool
        :returns: true if successful
        :rtype: bool
        """
        if access_mode:
            if not request_control(self.corsair_sdk, device_id):
                self._raise_corsair_error()
            return True
        else:
            raise NotImplementedError

    def last_error(self):
        """
        Return the last error reported by the SDK

        :returns: exception representing the last error
        :rtype: Exception
        """
        return error_id[get_last_error(self.corsair_sdk)]

    def device_info(self, device_id):
        """
        Return device information

        :param device_id: id of device
        :type device_id: int
        :returns: dict containing information about device
        :rtype: dict
        """
        return self.device(device_id).device_info()

    def device(self, device_id, *args, **kwargs):
        """
        Return a Device object based on id

        :param device_id: id of device
        :type device_id: int
        :param args: extra parameters
        :param kwargs: extra parameters
        :returns: Device object
        :rtype: Device
        """
        return Device(device_id, self._corsair_sdk_path, *args, **kwargs)


class Device(CorsairSDK):
    """
    Class that represents a device
    """
    def __init__(self, device_id, corsair_sdk_dll_path, control=False):
        """
        Create a new device object and check if it exists

        :param device_id: id of device
        :type device_id: int
        :param corsair_sdk_dll_path: Path to a sdk dll that matches the python version
        :type corsair_sdk_dll_path: str
        :param control: whether to request exclusive access or not
        :type control: bool
        """
        super(Device, self).__init__(corsair_sdk_dll_path)
        self.device_id = device_id
        # Check if device exists
        self.device_info()

        if control:
            request_control(self.corsair_sdk, 0)

    def device_info(self, device_id=None):
        """
        Return device information, if device_id is not specified, return for this device

        :param device_id: id of device
        :type device_id: int
        :returns: dict containing information about device
        :rtype: dict
        """
        if device_id is None:
            device_id = self.device_id
        return get_device_info(self.corsair_sdk, device_id)

    def led_positions(self):
        """
        Return information about led positions

        :returns: information about led positions
        :rtype: dict
        """
        return get_led_positions(self.corsair_sdk, self.device_id)
