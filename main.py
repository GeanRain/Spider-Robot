# _*_ coding: utf_8 _*_
# main.py __ put your code here!
import time
from machine import I2C, Pin
from PS2_lib import PS2Gamepad
from servo import Servos


def gamepad_init(pad):
    pad.setConfig()
    pad.setVibMode(vibration=True)
    pad.setAnalogMode(red=True, lock=True)
    pad.setConfig()


def main():
    time.sleep_ms(1000)
    # 'X1':  MISO=DAT(DI)
    # 'X2':  MOSI=CMD(DO)
    # 'X3':  CS=CS
    # 'X4':  CLK=CLK
    ps2 = PS2Gamepad(freq=250000, dat='X1', cmd='X2', cs='X3', clk='X4')
    gamepad_init(ps2)
    scl_pin = Pin('Y9')
    sda_pin = Pin('Y10')
    i2c = I2C(scl=scl_pin, sda=sda_pin, freq=10000)
    i2c.scan()
    servos = Servos(i2c, address=0x40)
    while(True):
        pass


if __name__ == "__main__":
    main()

