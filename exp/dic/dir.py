import os.path
import sys


def getFastPwdsDir():
    return os.path.join(sys.path[0], "FastPwds.txt")


def getMidPwdsDir():
    return os.path.join(sys.path[0], "LargePwds.txt")


def getLargePwdsDir():
    return os.path.join(sys.path[0], "MidPwds.txt")
#
#
# print(getMidPwdsDir())
# print(getFastPwdsDir())
# print(getLargePwdsDir())
