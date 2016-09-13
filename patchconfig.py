# -*- coding: utf-8 -*-

MAX_ADDRESS = 511


class Patch():

    def __init__(self, channel, addresses):
        self.mChannel = channel
        self.mAddresses = addresses
        self.mAddresses.sort()

    def getAddresses(self):
        return self.mAddresses

    def appendAddress(self, address):
        if self.mAddresses.count(address):
            return
        else:
            self.mAddresses.append(address)
            self.mAddresses.sort()

    def removeAddress(self, address):
        if address in self.mAddresses:
            self.mAddresses.remove(address)
            print("Removed address %i from channel %i"
                        % (address, self.mChannel))
            return True
        else:
            return False

    def getChannel(self):
        return self.mChannel

    def rawStr(self):
        strr = "%i" % self.mChannel
        for x in self.mAddresses:
            strr += ","
            strr += "%i" % x

        return strr

    def __repr__(self):

        strr = "Ch%i <- " % self.mChannel
        for x in self.mAddresses:
            strr += "%i, " % x

        return strr

    def __lt__(self, other):
        return self.mChannel < other.mChannel


class PatchConfig():

    def __init__(self, configfilepath):

        self.cfp = configfilepath
        self.readConfigFile()

    def __del__(self):
        self.writeConfigFile()

    def readConfigFile(self):

        self.data = []

        fp = open(self.cfp, "r")

        for line in fp:
            if len(line) < 1:
                print("ERR: Empty patch config.")
                return

            val = line.replace("\n", '').split(',')

            nChan = int(val[0])
            nAddresses = map(int, val[1:])
            newPatch = Patch(nChan, nAddresses)

            self.data.append(newPatch)

        self.data.sort()
        fp.close()

    def writeConfigFile(self):

        fp = open(self.cfp, "w")

        for x in self.data:
            fp.write(x.rawStr() + "\n")

        fp.close()

    def patch(self, address, channel):

        skipPatch = False

        if address > MAX_ADDRESS:
            print("ERR: Address larger than 512.")
            return

        if self.contains(address, channel):
            print("Patch already exists!")
            return

        if self.patchCheck(address):
            print("Address patched to another channel.")
            confirm = raw_input("Overwrite? (y/n) ")
            if confirm == "y":
                chan = self.getChannelWithAddress(address)
                self.removePatch(address)

                print("Removed address %i from channel %i"
                            % (address, chan))
            else:
                skipPatch = True

        if not skipPatch:
            found = False
            for x in self.data:
                if x.getChannel() == channel:
                    x.appendAddress(address)
                    found = True
                    break
            if not found:
                newPatch = Patch(channel, [address])
                self.data.append(newPatch)
                self.data.sort()

            print("Patched!")

        self.writeConfigFile()

    def contains(self, address, channel):
        for x in self.data:
            if x.getChannel() == channel:
                if address in x.getAddresses():
                    return True
        return False

    def patchCheck(self, address):
        for patch in self.data:
            if address in patch.getAddresses():
                return True
        return False

    def removePatch(self, address):
        for patch in self.data:
            tst = patch.removeAddress(address)

        if not tst:
            print("Address is not patched to any channel.")

        self.writeConfigFile()

    def getChannelWithAddress(self, address):
        for patch in self.data:
            if address in patch.getAddresses():
                return patch.getChannel()

    def hasPatchData(self, channel):
        for patch in self.data:
            if patch.getChannel() == channel:
                if len(patch.getAddresses()) > 0:
                    return True
        return False

    def getPatchConfig(self):
        return self.data

    def purge(self):
        self.data = []
        self.writeConfigFile()
        print("Purged patch configuration.")

    def printPatches(self):
        for x in self.data:
            if len(x.getAddresses()) > 0:
                print(x)

