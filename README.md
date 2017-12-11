# nfc-rw
A simple NFC tag reader/writer in Python.

Tested with the *SONY RC-S380* NFC reader/writer.

### Requirement

You will need:

- SONY RC-S380 NFC reader/writer
- Python 2.7
- The nfc library 
- The ndef library

### Dependencies

There are two libraries you will need to install.

Installing using `pip` is recommended.

```
pip install nfcpy
pip install ndeflib
```

### Run

```
python nfc-rw.py
```

### Usage

1. Plug in the RC-S380 into your usb port
2. Run the script
3. Place NFC tag on the RC-S380
4. Choose action by typing a letter and pressing enter
5. When you're done, eject the tag
6. Remove tag from the RC-S380
7. `Contorl + c` to end script or place another tag on the device to continue

### Actions

| key | name | action |
|-----|------|--------|
|  d  | Dump | Dumps the raw data stored in the tag to console without any formatting |
|  e  | Eject | Lets the script know you want to remove the tag before doing so |
|  f  | Format | Overwrites all the data stored in the tag with `0`s |
|  i  | Identify | Logs the tag type and product name to console |
|  r  | Read | Prints formatted records stored in the tag to console |
|  w  | Write | Writes the text inside `payload.txt` as a text record to tag |
