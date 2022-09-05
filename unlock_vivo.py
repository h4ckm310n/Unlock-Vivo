import usb.core
import usb.util
import traceback


# Change Fastboot idVendor and idProduct to your own
FB_IDVENDOR = 0x18d1
FB_IDPRODUCT = 0xd00d


def init_phone():
    dev = usb.core.find(idVendor=FB_IDVENDOR, idProduct=FB_IDPRODUCT)
    if not dev:
        print('Not found, exit')
        exit(-1)
    intf = dev[0][(0, 0)]
    usb.util.claim_interface(dev, intf)
    print('Init phone: finished')
    return dev, intf, intf[0], intf[1]


def clear_halt():
    phone.clear_halt(in_end)
    phone.clear_halt(out_end)
    print('Clear halt: finished')


def create_vendor():
    data_size = 1024
    data = b'\x00' * data_size
    return data, data_size


def send_bulk(cmd):
    assert phone.write(out_end, cmd) == len(cmd)
    ret = phone.read(in_end, 100)
    sret = ''.join([chr(x) for x in ret])
    print('Received from device:', sret)
    return sret


def flash_vendor():
    vendor, vendor_size = create_vendor()
    send_bulk('getvar:has-slot:vendor')
    send_bulk('getvar:max-download-size')
    send_bulk('getvar:is-logical:vendor')
    send_bulk('download:' + hex(vendor_size)[2:])
    send_bulk(vendor)
    send_bulk('flash:vendor')
    print('Flash vendor: finished')


def unlock_vivo():
    flash_vendor()
    cmd = 'vivo_bsp unlock_vivo'
    send_bulk(cmd)
    print('Unlock: finished')


def lock_vivo():
    cmd = 'vivo_bsp lock_vivo'
    send_bulk(cmd)
    print('Lock: finished')


print('Power off your phone, then press and hold Power + Volume Up to enter Fastboot mode')
input('If your phone is already in Fastboot, press Enter to continue:')
print('Available Operations:\n1: Unlock\n2: Lock')

phone, interface, in_end, out_end = init_phone()
op = input('Select an operation:')

try:
    if op == '1':
        clear_halt()
        unlock_vivo()
    elif op == '2':
        clear_halt()
        lock_vivo()
    else:
        print('Invalid operation')
except:
    traceback.print_exc()
finally:
    usb.util.release_interface(phone, interface)
