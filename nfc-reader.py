import nfc
import nfc.ndef

def startup(targets):
    print "Waiting to read NFC tag...\n"
    return targets


def connected(tag):
    # if not tag.ndef or not tag.ndef.is_writeable:
    #     print "not a writeable nfc tag"
    #     return False
    print "Tag engaged. Tag data:\n"
    print tag.ndef.message.pretty()

    # smartposter = nfc.ndef.SmartPosterRecord("https://youtu.be/0E00Zuayv9Q")
    # smartposter.title = "PPAP"
    # new_message = nfc.ndef.Message(smartposter)

    # if len(str(new_message)) > tag.ndef.capacity:
    #     print "too long message"
    #     return True

    # if tag.ndef.message == new_message:
    #     print "already same record"
    #     return True

    # tag.ndef.message = new_message
    # print "new message:"
    # print tag.ndef.message.pretty()

    return True


def released(tag):
    print "\nTag released. Waiting to read NFC tag...\n"


device = nfc.ContactlessFrontend('usb')
print "\nSuccessfully connected to " + str(device) + "\n"
if device:
    while device.connect(rdwr={
        'on-startup': startup,
        'on-connect': connected,
        'on-release': released,
    }):
        pass
