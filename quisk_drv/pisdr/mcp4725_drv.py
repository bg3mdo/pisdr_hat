from i2c_drv import I2CDrv

MCP4752_I_CH_I2C_ADDRESS_DEFAULT = 0x66
MCP4752_Q_CH_I2C_ADDRESS_DEFAULT = 0x67
# Register values:
WRITEDAC = 0x40
WRITEDACEEPROM = 0x60


class MCP4725(object):
    def __init__(self, address=MCP4752_I_CH_I2C_ADDRESS_DEFAULT, bus_num=-1):
        self.i2c = I2CDrv(address=address, bus_num=bus_num)

    def set_voltage(self, value, persist=False):
        # Vout = (5V * value) / 4096

        if value > 4095:
            value = 4095
        if value < 0:
            value = 0

        reg_data = [(value >> 4) & 0xFF, (value << 4) & 0xFF]
        if persist:
            self.i2c.write_list(WRITEDACEEPROM, reg_data)
        else:
            self.i2c.write_list(WRITEDAC, reg_data)


if __name__ == '__main__':
    mcp4725_i = MCP4725(MCP4752_I_CH_I2C_ADDRESS_DEFAULT)
    mcp4725_i.set_voltage(2000)
    mcp4725_q = MCP4725(MCP4752_Q_CH_I2C_ADDRESS_DEFAULT)
    mcp4725_q.set_voltage(2000)
