# -*- coding: utf-8 -*-

from dmx import DMX

import array

MAX_ADDRESSES = 512
UNIVERSE = 1


class DMXServer():

    def __init__(self, PatchConfigOb):
        self.pconf = PatchConfigOb
        self.patchConf = self.pconf.getPatchConfig()
        self.dmxDev = DMX(UNIVERSE)
        self.data = [0] * MAX_ADDRESSES

        self.debug = True

    def setChan(self, channel, level):

        changed = True

        if level > 100 or level < 0:
            print("Level must be in range 0-100")
            return
        if channel > MAX_ADDRESSES - 1 or channel < 1:
            print("Channel must be between 1 and %i"
                        % (MAX_ADDRESSES - 1))
            return

        if not self.pconf.hasPatchData(channel):
            changed = False
            #print("Channel %i has no patched addresses." % channel)
            #return

        nLevel = self.levelConv(level)

        addList = []
        for patch in self.patchConf:
            if patch.getChannel() == channel:
                addList = patch.getAddresses()
                break

        for address in addList:
            self.data[address - 1] = nLevel

        self.sendData(self.data)

        if changed:
            if self.debug:
                print("Ch%i set to level %i" % (channel, level))

    def out(self):
        self.data = [0] * MAX_ADDRESSES
        self.sendData(self.data)
        print("All out!")

    def full(self):
        self.data = [255] * MAX_ADDRESSES
        self.sendData(self.data)
        print("All full!")

    def sendData(self, dataList):
        sendData = array.array('B', dataList)
        self.dmxDev.sendSingleFrame(sendData)

    def levelConv(self, level):
        return int((float(level) / 100) * float(255))

    def printCurData(self):
        print(self.data)

    def DebugToggle(self, TF):
        self.debug = TF