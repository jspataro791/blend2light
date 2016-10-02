# -*- coding: utf-8 -*-

import array
from ola.ClientWrapper import ClientWrapper

# This object talks to the Open Lighting Architecture library

class DMX():

    def __init__(self, universe):
        self.mUniverse = universe
        self.mWrapper = ClientWrapper()
        self.mClient = self.mWrapper.Client()

    def DmxSent(self, state):
        self.mWrapper.Stop()

    def sendSingleFrame(self, dataArray):

        if len(dataArray) > 512:
            print("WARNING: Data array length exceeds 512.")
        for x in dataArray:
            if x > 255:
                print("WARNING: Data array contains value exceeding 255")

        self.mClient.SendDmx(self.mUniverse, dataArray, self.DmxSent)

        self.mWrapper.Run()

