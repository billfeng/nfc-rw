import sys
import nfc
import ndef

END = '\033[0m'
RED = '\033[91m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'

def startup(targets):
    """ Device ready, waiting for tag. """
    print YELLOW + "Waiting to read NFC tag...\n" + END
    return targets

def dump(tag):
    """ Dump the data stored in the tag to standard output """
    print "Dumping tag content:"
    print BLUE + str("\n".join(["  " + line for line in tag.dump()])) + "\n" + END

def identify(tag):
    """ Print out the tag type and ID """
    print "Type: " + BLUE + str(tag.type) + END
    print "Name: " + BLUE + str(tag.product) + "\n" + END

def erase(tag):
    """ Format tag & over write with 0s """
    tag.format(None, 0)
    print GREEN + "Format success!" + "\n" + END

def read(tag):
    """ Read & print records """
    print "Current Records:"
    if len(tag.ndef.records) > 0:
        prettyprint(tag)
    else:
        print BLUE + "\nNone\n" + END

def write(tag):
    """ Read records from file and write to tag """
    try:
        payloadfile = open("payload.txt", "r")
        payload = payloadfile.readline()
        payloadfile.close()
        if len(str(payload)) > tag.ndef.capacity:
            print RED + "Length of message is too long!\n" + END
        else:
            tag.ndef.records = [ndef.TextRecord(payload)]
            print GREEN + "Write success!\n" + END
            # Print new records
            print "New Records:"
            prettyprint(tag)
    except IOError as err:
        print RED + "Reading from file failed: " + str(err) + "\n" + END
    except nfc.tag.TagCommandError as err:
        print RED + "Write to tag failed: " + str(err) + "\n" + END
    except ValueError as err:
        print RED + "Bad input: " + str(err) + "\n" + END

def prettyprint(tag):
    """ Helper function for printing the tag. Used by read() and write() """
    for record in tag.ndef.records:
        print ""
        if record.type == "urn:nfc:wkt:T":
            print "Type: " + BLUE + "Text Record" + END
            print "Name: " + BLUE + record.name + END
            print "Lang: " + BLUE + record.language + END
            print "Enco: " + BLUE + record.encoding + END
            print "Text: " + BLUE + record.text + END
        else:
            print "Type: " + BLUE + record.type + END
            print "Data: " + BLUE + record.data + END
    print ""

def standby(tag):
    """ Choose action """
    print YELLOW + "d) Dump e) Eject f) Format i) Identify r) Read w) Write " + END
    key = raw_input("Action: ")
    print ""
    if tag.is_present:
        # Execute action
        if key == 'd' or key == 'D':
            dump(tag)
        elif key == 'e' or key == 'E':
            print GREEN + "Tag ejected. You can safely remove the tag.\n" + END
            return True
        elif key == 'f' or key == 'F':
            erase(tag)
        elif key == 'i' or key == 'I':
            identify(tag)
        elif key == 'r' or key == 'R':
            read(tag)
        elif key == 'w' or key == 'W':
            write(tag)
        else:
            print RED + "Invalid input.\n" + END
        return False
    else:
        print RED + "Tag is not within communication range.\n" + END
        return True

def engaged(tag):
    """ Tag is engated, identify tag. """
    print GREEN + str(tag) + " engaged.\n" + END
    done = False
    while not done:
        done = standby(tag)
    return True

def released(tag):
    """ Tag is released. """
    print "Tag released. "
    print YELLOW + "Waiting to read NFC tag...\n" + END


device = nfc.ContactlessFrontend('usb')
print ""
sys.stdout.write(GREEN + "Connected to " + END)
print BLUE + str(device.device.vendor_name) + " " + str(device.device.product_name) + "\n" + END
if device:
    while device.connect(rdwr={
        'on-startup': startup,
        'on-connect': engaged,
        'on-release': released,
    }):
        pass

print "\n"
sys.stdout.write(RED + "Disconnected from " + END)
print BLUE + str(device.device.vendor_name) + " " + str(device.device.product_name) + "\n" + END
