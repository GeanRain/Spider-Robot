from machine import Pin
import time


class PS2Gamepad:
    def __init__(self, dat, cmd, cs, clk, freq=250000):
        self.__pinDAT = Pin(dat, Pin.IN, Pin.PULL_DOWN)
        self.__pinCMD = Pin(cmd, Pin.OUT)
        self.__pinCS = Pin(cs, Pin.OUT, Pin.PULL_UP)
        self.__pinCLK = Pin(clk, Pin.OUT)
        # This is the ID of the button
        # SELECT   = 1   L3        = 2   R3       = 3   START    = 4
        # PAD_UP   = 5   PAD_RIGHT = 6   PAD_DOWN = 7   PAD_LEFT = 8
        # L2       = 9   R2        = 10  L1       = 11  R1       = 12
        # TRIANGLE = 13  CIRCLE    = 14  CROSS    = 15  SQUARE   = 16
        self.__buttonMask = (
            "SELECT", "L3", "R3", "START",
            "PAD_UP", "PAD_RIGHT", "PAD_DOWN", "PAD_LEFT",
            "L2", "R2", "L1", "R1",
            "TRIANGLE", "CIRCLE", "CROSS", "SQUARE"
        )
        self.__sendBuf = [0x01, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.__dataBuf = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.__freq = int(1000000 / freq)
        self.redMode = False
        self.configMode = False
        self.vibMode = False
        self.__vibValue = [0x00, 0x00]
        self.setReady()

    def __ready2send(self):
        self.__pinCS.value(0)

    def __endOfsend(self):
        self.__pinCS.value(1)

    def __sendFrame(self, cmd=0):
        ret = 0
        for respBit in (1, 2, 4, 8, 16, 32, 64, 128):
            if(respBit & cmd):  # send cmd
                self.__pinCMD.value(1)
            else:
                self.__pinCMD.value(0)
            self.__pinCLK.value(1)
            time.sleep_us(self.__freq)
            self.__pinCLK.value(0)
            time.sleep_us(self.__freq)
            if(self.__pinDAT.value() == 1):  #get resp
                ret = respBit | ret
            self.__pinCLK.value(1)
        return ret
    
    def clearSendBuf(self):
        self.__sendBuf = [0x01, 0x42, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def clearDataBuf(self):
        for i in range(0, len(self.__dataBuf), 1):
            self.__dataBuf[i] = 0

    def setReady(self):
        self.__endOfsend()
        self.__pinCLK.value(1)
        self.__pinCMD.value(0)
        time.sleep_ms(10)

    def cmdWithPad(self):
        self.__ready2send()
        self.__sendFrame(self.__sendBuf[0])  # start Communicating
        self.redMode = self.__sendFrame(self.__sendBuf[1]) is not 0x41
        self.__sendFrame(self.__sendBuf[2])  # game pad start to send btn data
        for i in range(0, 6, 1):
            self.__dataBuf[i] = self.__sendFrame(self.__sendBuf[i + 3])
        self.__endOfsend()
        time.sleep_ms(10)

    def setConfig(self):
        self.clearSendBuf()
        self.clearDataBuf()
        self.__sendBuf[1] = 0x43
        if self.configMode is False:
            # start config
            self.__sendBuf[3] = 0x01
            self.configMode = True
        else:
            # save config
            for index in range(4, 9, 1):
                self.__sendBuf[index] = 0x5A
            self.configMode = False
        self.__ready2send()
        self.cmdWithPad()
        self.__endOfsend()
        time.sleep_ms(10)

    def setAnalogMode(self, red=False, lock=False):
        self.clearSendBuf()
        self.clearDataBuf()
        self.__sendBuf[1] = 0x44
        if red is False:
            self.__sendBuf[3] = 0x00  # disable red mode
        else:
            self.__sendBuf[3] = 0x01  # enable red mode
        if lock is False:
            # unlock the setting, you can use <mode> btn to change analog
            self.__sendBuf[4] = 0xEE
        else:
            # lock the setting, you can' use <mode> btn to change analog
            self.__sendBuf[4] = 0x03
        self.__ready2send()
        self.cmdWithPad()
        self.__endOfsend()
        time.sleep_ms(10)

    def setVibMode(self, vibration=False):
        self.clearSendBuf()
        self.clearDataBuf()
        self.__sendBuf[1] = 0x4D
        if vibration is False:
            # enable vibration
            self.__sendBuf[4] = 0X00
            self.vibMode = False
        else:
            # disable vibration
            self.__sendBuf[4] = 0X01
            self.vibMode = True
        self.__ready2send()
        self.cmdWithPad()
        self.__endOfsend()
        time.sleep_ms(10)

    # set vibration value
    def setVibValue(self, WW=-1, YY=-1):
        self.clearSendBuf()
        self.clearDataBuf()
        if 0x00 <= WW <= 0xFF:
            self.__vibValue[0] = WW
        if 0x40 <= YY <= 0xFF:
            self.__vibValue[1] = YY
        self.__ready2send()
        self.cmdWithPad()
        self.__endOfsend()
        time.sleep_ms(10)

    def getBtn(self):
        self.clearSendBuf()
        self.clearDataBuf()
        if self.vibMode is True:
            self.__dataBuf[3] = self.__vibValue[0]
            self.__dataBuf[4] = self.__vibValue[1]
        self.cmdWithPad()
        retList = []
        btn = (self.__dataBuf[1] << 8) | self.__dataBuf[0]
        for i in range(0, 16):
            if((btn & (1 << i)) == 0):
                retList.append(i + 1)
        return retList

    def getBtnName(self, button):
        if(1 <= button <= len(self.__buttonMask)):
            return self.__buttonMask[button - 1]
        else:
            return "None"

    def getAnologData(self, rocker='L'):
        ret = []
        if rocker is 'L':
            ret.append(self.__dataBuf[2] - 128)
            ret.append(127 - self.__dataBuf[3])
        else:
            ret.append(self.__dataBuf[4] - 128)
            ret.append(127 - self.__dataBuf[5])
        return ret


def main():
    time.sleep_ms(1000)
    # 'X1':  MISO=DAT(DI)
    # 'X2':  MOSI=CMD(DO)
    # 'X3':  CS=CS
    # 'X4':  CLK=CLK
    ps2 = PS2Gamepad(freq=1000000, dat='X1', cmd='X2', cs='X3', clk='X4')
    input("please enter to start debug")
    ps2.setConfig()
    ps2.setAnalogMode(red=True, lock=True)
    ps2.setVibMode(vibration=True)
    ps2.setConfig()
    ps2.setVibValue(0xFF, 0xFF)
    while(True):
        btn = ps2.getBtn()
        if btn:
            for i in range(0, len(btn)):
                btn[i] = ps2.getBtnName(btn[i])
            print("get button:" + str(btn))
        time.sleep_ms(100)


if __name__ == "__main__":
    main()
