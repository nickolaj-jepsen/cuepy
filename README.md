# cuepy 0.1.2 (Prerelease)
A python wrapper for the Corsair Utility Engine SDK

##Notice!
This is a prerelease, the api will probably change.

Furthermore, i have only tested this on Windows 10 x64 with my Corsair k70 RGB nordic, so there might be compatibility issues

## Documentation

###Install
using pip:

```
pip install cuepy
```

or 

```
git clone https://github.com/fire-proof/cuepy 
cd cuepy 
python setup.py install
```

###Usage

```python
>>> from cuepy import CorsairSDK
>>> sdk = CorsairSDK(path_to_sdk_dll) # eg. "C:\\cuesdk\\CUESDK.x64_2013.dll"

>>> sdk.device_count()
1

>>> sdk.device_info(0)
{'capsMask': 1,
 'logicalLayout': 3,
 'model': b'K70 RGB',
 'physicalLayout': 2,
 'type': 2}

>>> device = sdk.device(0)

>>> device.set_led(1, [255,255,255])
True
```

###Keyboard Layouts
####K70 Nordic
![GitHub Logo](/docs/k70_nordic.png)
