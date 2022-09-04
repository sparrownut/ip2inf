import argparse

parser = argparse.ArgumentParser(description='SERVERID')
parser.add_argument('-i', type=str, help='username')
parser.add_argument('-y', action='store_true', help='default switch yes')
parser.add_argument('-v', action='store_true', help='output details if switch this argument')
parser.add_argument('-f', type=str, help='input hosts file')
parser.add_argument('-lip', type=str, help='lhost ip')
args = parser.parse_args()

details = False
threadcou = 10
