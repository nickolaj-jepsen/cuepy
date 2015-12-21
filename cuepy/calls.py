from ctypes import c_int, c_bool, POINTER, c_char

from cuepy.stuct import ProtocolDetailsStruct, DeviceInfoStruct, LedPositions, LedColor


def perform_protocol_handshake(dll):
    func = dll["CorsairPerformProtocolHandshake"]
    func.restype = ProtocolDetailsStruct
    result = func()
    return {
        "sdkVersion": result.sdkVersion,
        "serverVersion": result.serverVersion,
        "sdkProtocolVersion": result.sdkProtocolVersion,
        "serverProtocolVersion": result.serverProtocolVersion,
        "breakingChanges": result.breakingChanges,
    }


def get_device_count(dll):
    func = dll["CorsairGetDeviceCount"]
    func.restype = c_int
    return func()


def get_device_info(dll, device):
    func = dll["CorsairGetDeviceInfo"]
    func.argtypes = [c_int]
    func.restype = POINTER(DeviceInfoStruct)
    result = func(device)

    return {
        "type": result[device].type,
        "model": result[device].model,
        "physicalLayout": result[device].physicalLayout,
        "logicalLayout": result[device].logicalLayout,
        "capsMask": result[device].capsMask,
    }


def get_led_positions(dll, device):
    func = dll["CorsairGetLedPositions"]
    func.restype = POINTER(LedPositions)
    result = func()

    leds = {}

    for x in range(result[device].numberOfLeds):
        x = result[device].pLedPosition[x]
        leds[x.ledId] = {
            "top": x.top,
            "left": x.left,
            "height": x.height,
            "width": x.width,
        }

    return {
        "numberOfLeds": result[device].numberOfLeds,
        "pLedPosition": leds
    }


def get_led_id_for_key_name(dll, char):
    func = dll["CorsairGetLedIdForKeyName"]
    func.restype = c_int
    func.argtypes = [c_char]
    result = func(char)
    return result


def set_leds_color(dll, color_struct, amount=1):
    func = dll["CorsairSetLedsColors"]
    func.restype = c_bool
    func.argtypes = [c_int, POINTER(LedColor)]
    result = func(amount, color_struct)
    return result


def request_control(dll, access_mode):
    func = dll["CorsairRequestControl"]
    func.restype = c_bool
    func.argtypes = [c_int]
    result = func(access_mode)
    return result


def get_last_error(dll):
    func = dll["CorsairGetLastError"]
    func.restype = c_int
    result = func()
    return result
