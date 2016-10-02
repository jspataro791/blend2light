# -*- coding: utf-8 -*-

# Custom Import
from src import patchconfig
from src import dmxserver
from patchconfig import PatchConfig
from dmxserver import DMXServer

# Library Import
import time

# Setup
version = "1.0"
PATCH_CONFIG_PATH = "../configs/patchconfig.dat"
TEST_TIME_WAIT = 1
pconf = PatchConfig(PATCH_CONFIG_PATH)
DMXServ = DMXServer(pconf)


# Defs
def printUsage():
    print("Invalid input.")
    #sys.exit(0)


def printChanUsage():
    print("Usage: chan <channel> @ <level>")
    print("       chan <ch1> thru <ch2> @ <level>")
    print("       Valid Levels: 1-100, full, out")


def printTstUsage():
    print("Usage: tst chan <channel> <repeats>")

# Main Loop
running = True
while(running):

    # get input

    inp = raw_input("> ")

    inp = inp.lower()

    args = inp.split(" ")

    # CHAN
    if args[0] == "chan":

        value = None
        channel1 = None
        channel2 = None

        try:
            channel1 = int(args[1])

            if args[2] == "thru":

                channel2 = int(args[3])

                if args[4] == "@" or args[4] == "at":

                    if args[5] == "out":
                        value = 0
                    elif args[5] == "full":
                        value = 100
                    else:
                        value = int(args[5])

                    for x in range(channel1, channel2 + 1):
                        DMXServ.setChan(x, value)
                else:
                    printChanUsage()

            elif args[2] == "@" or args[2] == "at":

                if args[3] == "out":
                    value = 0
                elif args[3] == "full":
                    value = 100
                else:
                    value = int(args[3])

                DMXServ.setChan(channel1, value)

            else:
                printChanUsage()

        except ValueError:
            "Invalid channel or level"
        except IndexError:
            printChanUsage()

    # EXIT
    elif args[0] == "exit" or args[0] == "quit":
        break

    # PATCH
    elif args[0] == "patch":

        if len(args) < 3:
            print("Usage: patch <address> <channel>")

        else:
            try:
                address = int(args[1])
                channel = int(args[2])
                confirm = raw_input("Patch Address %i -> Ch %i? (y/n) "
                                            % (address, channel))
                if confirm == "y":
                    pconf.patch(address, channel)

            except ValueError:  # catch if the user puts in something weird
                print("Invalid address or channel.")

    # LIST PATCHES
    elif args[0] == "list":
        pconf.printPatches()

    # UNPATCH
    elif args[0] == "unpatch":
        try:
            address = int(args[1])
            pconf.removePatch(address)
        except ValueError:
            print("Invalid address.")

    # PURGE
    elif args[0] == "purge":
        confirm = raw_input("Confirm purge patch config? (y/n) ")
        if confirm == "y":
            pconf.purge()

    # PRINT BUFFER
    elif args[0] == "printbuf":
        DMXServ.printCurData()

    # ALL OUT
    elif args[0] == "out":
        DMXServ.out()

    # ALL FULL
    elif args[0] == "full":
        confirm = raw_input("All channels at full? (y/n) ")
        if confirm == "y":
            DMXServ.full()

    # TST
    elif args[0] == "tst":
        try:
            if args[1] == "chan":
                channel = int(args[2])
                repeats = int(args[3])

                for x in range(repeats):
		    time.sleep(TEST_TIME_WAIT)
                    DMXServ.setChan(channel, 100)
                    time.sleep(TEST_TIME_WAIT)
                    DMXServ.setChan(channel, 0)

            else:
                printTstUsage()
        except ValueError:
            print("Invalid input number.")

    # PRINT USAGE
    else:
        printUsage()









