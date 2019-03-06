from pyb import Timer


class SpiderJoint:
    def __init__(self, No):
        self.__servoNo = No
        self.__degNow = 0
        self.__degSet = 0
        self.__degOffSet = 0

    def setDeg(self, deg):
        self.__degSet = deg + self.__degOffSet

    def setOffSet(self, offset):
        self.__degOffSet = offset

    def isInPlace(self):
        if self.__degNow is self.__degSet:
            return True
        elif self.__degNow - self.__degSet > 0:
            if (self.__degNow - self.__degSet) % 2 is 0:
                self.__degNow -= 2
            else:
                self.__degNow -= 1
        else:
            if (self.__degNow - self.__degSet) % 2 is 0:
                self.__degNow += 2
            else:
                self.__degNow += 1
        return False

    def inPlace(self):
        self.__degNow = self.__degSet


class SpiderLimbs:
    def __init__(self, turn, turnLength, led, ledLength, tibia, tibiaLength):
        pass
        # NumList = range(0, 15)
        # if turn in NumList and led in NumList and tibia in NumList:
        #     self.__turn = {"joins": SpiderJoint(turn), "length": turnLength}
        #     self.__led = {"joins": SpiderJoint(led), "length": ledLength}
        #     self.__tibia = {"joins": SpiderJoint(tibia), "length": tibiaLength}

    def limbsDebug(self):
        while True:
            pass
            # print("- 1 - turn")
            # print("- 2 - led")
            # print("- 3 - tibia")
            # limbs = input("select the option to modify:")
            # print("- 1 - setDeg(" + self.limbs[limbsOption[int(limbs)]]['deg_set'] + ")")
            # print("- 2 - offset(" + self.limbs[limbsOption[int(limbs)]]['offset'] + ")")
            # modify = input("select the option to modify:")
            # value = input("enter the value:")
            # if int(modify) is 1:
            #     self.setDeg(self.limbs[limbsOption[int(limbs)]], degSet=value)
            # else:
            #     self.setDeg(self.limbs[limbsOption[int(limbs)]], offset=value)
            # if input("do you want to exit(y/n):") is 'y':
            #     break

    def setPoint(self, x, y, height):
        pass
        # r = math.sqrt(x*x + y*y)
        # self.__turn["joins"].setDeg(self.__getdegrees(x, r, y))

    def __getdegrees(self, subtense, left, right):
        pass
        # return math.degrees(math.acos(
        #     (left*left + right*right - subtense*subtense) /
        #     (2*left*right)
        # ))


class SpiderAction:
    def __init__(self):
        # self.LFront = SpiderLimbs(0, 1, 2)
        # self.RFront = SpiderLimbs(4, 5, 6)
        # self.LRear = SpiderLimbs(8, 9, 10)
        # self.RRear = SpiderLimbs(12, 13, 14)
        self.ready()
        tim = Timer(1, freq=2)
        tim.callback(self.actionIRQ)

    def ready(self):
        pass

    def stand():
        pass
    
    def hallo():
        pass

    def walk():
        pass

    def actionIRQ(self):
        pass
