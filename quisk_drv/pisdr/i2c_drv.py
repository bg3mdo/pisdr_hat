# This is a testing only Python script by Yuan Wang (BG3MDO)
# The script adding supports to Quisk for PISDR HAT
# 5 April 2021, email: bg3mdo@gmail.com
# Further optimisation is needed

import smbus


class I2CDrv(object):

    @staticmethod
    def get_pi_revision():
        # "Gets the version number of the Raspberry Pi board"
        # Courtesy quick2wire-python-api
        # https://github.com/quick2wire/quick2wire-python-api
        # Updated revision info from: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('Revision'):
                        return 1 if line.rstrip()[-1] in ['2', '3'] else 2
        except:
            return 0

    @staticmethod
    def get_pi_i2c_bus_number():
        # Gets the I2C bus number /dev/i2c#
        return 1 if I2CDrv.get_pi_revision() > 1 else 0

    def __init__(self, address, bus_num=-1, debug=False):
        self.address = address
        # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
        # Alternatively, you can hard-code the bus version below:
        # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)
        # self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's)
        self.bus = smbus.SMBus(bus_num if bus_num >= 0 else I2CDrv.get_pi_i2c_bus_number())
        self.debug = debug

    @staticmethod
    def reverse_byte_order(self, data):
        # "Reverses the byte order of an int (16-bit) or long (32-bit) value"
        byte_count = len(hex(data)[2:].replace('L', '')[::2])
        val = 0
        for i in range(byte_count):
            val = (val << 8) | (data & 0xff)
            data >>= 8
        return val

    def err_msg(self):
        print('Error accessing 0x%02X: Check your I2C address' % self.address)
        return -1

    def write8(self, reg, value):
        # "Writes an 8-bit value to the specified register/address"
        try:
            self.bus.write_byte_data(self.address, reg, value)
            if self.debug:
                print('I2C: Wrote 0x%02X to register 0x%02X' % (value, reg))
        except IOError:
            return self.err_msg()

    def write16(self, reg, value):
        # "Writes a 16-bit value to the specified register/address pair"
        try:
            self.bus.write_word_data(self.address, reg, value)
            if self.debug:
                print('I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X' %
                      (value, reg, reg + 1))
        except IOError:
            return self.err_msg()

    def write_raw8(self, value):
        # "Writes an 8-bit value on the bus"
        try:
            self.bus.write_byte(self.address, value)
            if self.debug:
                print('I2C: Wrote 0x%02X' % value)
        except IOError:
            return self.err_msg()

    def write_list(self, reg, a_list):
        # "Writes an array of bytes using I2C format"
        try:
            if self.debug:
                print('I2C: Writing list to register 0x%02X:' % reg)
                print(a_list)
            self.bus.write_i2c_block_data(self.address, reg, a_list)
        except IOError:
            return self.err_msg()

    def read_list(self, reg, length):
        # "Read a list of bytes from the I2C device"
        try:
            results = self.bus.read_i2c_block_data(self.address, reg, length)
            if self.debug:
                print('I2C: Device 0x%02X returned the following from reg 0x%02X' %
                      (self.address, reg))
                print(results)
            return results
        except IOError:
            return self.err_msg()

    def read_u8(self, reg):
        # "Read an unsigned byte from the I2C device"
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if self.debug:
                print('I2C: Device 0x%02X returned 0x%02X from reg 0x%02X' %
                      (self.address, result & 0xFF, reg))
            return result
        except IOError:
            return self.err_msg()

    def read_s8(self, reg):
        # "Reads a signed byte from the I2C device"
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if result > 127:
                result -= 256
            if self.debug:
                print('I2C: Device 0x%02X returned 0x%02X from reg 0x%02X' %
                      (self.address, result & 0xFF, reg))
            return result
        except IOError:
            return self.err_msg()

    def read_u16(self, reg, little_endian=True):
        # "Reads an unsigned 16-bit value from the I2C device"
        try:
            result = self.bus.read_word_data(self.address, reg)
            # Swap bytes if using big endian because read_word_data assumes little
            # endian on ARM (little endian) systems.
            if not little_endian:
                result = ((result << 8) & 0xFF00) + (result >> 8)
            if self.debug:
                print('I2C: Device 0x%02X returned 0x%04X from reg 0x%02X' % (self.address, result & 0xFFFF, reg))
            return result
        except IOError:
            return self.err_msg()

    def read_s16(self, reg, little_endian=True):
        # "Reads a signed 16-bit value from the I2C device"
        try:
            result = self.read_u16(reg, little_endian)
            if result > 32767:
                result -= 65536
            return result
        except IOError:
            return self.err_msg()


if __name__ == '__main__':
    try:
        bus = I2CDrv(address=0x00)
        print('Default I2C bus is accessible')
    except:
        print('Error accessing default I2C bus')
