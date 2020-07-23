#!/usr/bin/python3
import requests
import json
import sys
import struct
import socket
import colorama
from colorama import Fore

indent = "  "


def ip2bin(ip):  # Credit to converter
    binary = bin(struct.unpack('!I', socket.inet_aton(ip))[0])
    return binary


def arg_length():
    return len(sys.argv)


def print_help():
    print("Commands:")
    print("** ipl -i <ip> - Gets information from an IP address")
    print("** ipl -h - Displays this page.")


def lookup(ip):
    print("Looking up IP address \"" + str(ip) + "\"..")

    re = requests.get("https://ipinfo.io/" + str(ip) + "/json")

    j = json.loads(re.content)

    postal = ''
    loc = ''
    hostname = ''

    print("IP Information:")

    for key, value in j.items():
        maininfo = True
        if str(key) == "error":
            print("Error: Invalid IP address")
            exit(0)
        if str(key) != "readme":
            if key == "postal":
                postal = value
                maininfo = False
            if key == "loc":
                loc = value
                maininfo = False
            if key == 'hostname':
                loc = value
                maininfo = False
            if maininfo:
                print(indent + key, "-", Fore.BLUE + value + Fore.WHITE)

    binary = ip2bin(ip).replace('0b', '')

    ipClass = 'Class '

    if binary.startswith("0"):
        ipClass += 'A'

    elif binary.startswith('10'):
        ipClass += 'B'

    elif binary.startswith('110'):
        ipClass += 'C'

    elif binary.startswith('1110'):
        ipClass += 'D'

    elif binary.startswith('1111'):
        ipClass += 'E'

    print("Additional Information:")
    print(indent + "IP Class: " + Fore.BLUE + ipClass + Fore.WHITE)
    print(indent + "Postal Code: " + Fore.BLUE + postal + Fore.WHITE)
    print(indent + "Long/Lat: " + Fore.BLUE + loc + Fore.WHITE)
    if not hostname == '':
        print("Hostname: " + hostname)


if arg_length() == 1 or arg_length() == 2:
    print_help()
if arg_length() == 3:
    if str(sys.argv[1]) == "-i":
        lookup(str(sys.argv[2]))
    else:
        print_help()
