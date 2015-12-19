from _ctypes import Structure, POINTER
from ctypes import c_char_p, c_int, c_bool, c_double


class ProtocolDetailsStruct(Structure):
    _fields_ = [
        ("sdkVersion", c_char_p),
        ("serverVersion", c_char_p),
        ("sdkProtocolVersion", c_int),
        ("serverProtocolVersion", c_int),
        ("breakingChanges", c_bool)
    ]


class DeviceInfoStruct(Structure):
    _fields_ = [
        ("type", c_int),
        ("model", c_char_p),
        ("physicalLayout", c_int),
        ("logicalLayout", c_int),
        ("capsMask", c_int)
    ]


class LedPosition(Structure):
    _fields_ = [
        ("ledId", c_int),
        ("top", c_double),
        ("left", c_double),
        ("height", c_double),
        ("width", c_double)
    ]


class LedPositions(Structure):
    _fields_ = [
        ("numberOfLeds", c_int),
        ("pLedPosition", POINTER(LedPosition)),
    ]


class LedColor(Structure):
    _fields_ = [
        ("ledId", c_int),
        ("r", c_int),
        ("g", c_int),
        ("b", c_int),
    ]

    def __repr__(self):
        return "<LedColor(id:{id}, r:{r}, g:{g}, b:{b})>".format(id=self.ledId,
                                                                 r=self.r,
                                                                 g=self.g,
                                                                 b=self.b)
