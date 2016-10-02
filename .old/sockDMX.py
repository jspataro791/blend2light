import socket
import sys
import platform
print("\n[CLIENT INIT]") 

if platform.system() == 'Windows':
    print("INFO: Importing WinTk")
    from tkinter import *
if platform.system() == 'Linux':
    print("INFO: Importing LinTk")
    from Tkinter import *

# Lamp class
class Lamp:

    def __init__(self,chan,intens,color):
        self.chan = chan
        self.intens = intens
        self.color = color

    def __hash__(self):
        return self.chan

    def __eq__(self,other):
        try:
            return (self.chan == other.chan)
        except AttributeError:
            return NotImplemented

# SET UP UDP PORT LISTEN
print("Opening UDP port...")

UDP_IP = 'localhost'
UDP_PORT = 8081

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(0)
    sock.bind((UDP_IP, UDP_PORT))
except:
    print("ERR: Unable to open UDP socket.")
    exit

   
# Light widget (tombstone)
class LightWidget:

    def __init__(self,chanel,parent):
        frame = Frame(master=parent)
        frame.config(relief = RIDGE, bd=3)
        self.frame = frame
        
        self.chanel = chanel
        self.intensity = 0
        self.color = '#000000'
        
        self.createWidgets()
        
    def createWidgets(self):
        # channel 
        self.nametag = Label(self.frame, text = "CH: " + str(self.chanel))
        self.nametag.config(bd=1, relief=SUNKEN, bg="white")
        self.nametag.grid(row=0,column=0,columnspan=2)

        # intensity
        self.inttag = Label(self.frame, text = "Int")
        self.inttag.grid(row=1,column=0)
        self.intlabel = Label(self.frame,text = str(self.intensity))
        self.intlabel.grid(row=1,column=1)

        # color
        self.colortag = Label(self.frame, text = "Color")
        self.colortag.grid(row=2,column=0)
        self.color = Label(self.frame,text="      ")
        self.color.config(relief=RIDGE,bd=1,bg="white")
        self.color.grid(row=2,column=1)

    def setColor(self,color):
        self.color.config(bg=color)

    def setChan(self,channel):
        self.nametag.config(text="CH: %i" % channel)

    def setIntens(self,intens):
        self.intlabel.config(text=("%i" % intens).zfill(3))

# light monitor
class LightMonitor:

    def __init__(self,parent):
        frame = Frame(master=parent)
        frame.pack()

        self.parent = parent     
        self.lights = []
        self.frame = frame

        self.socket = sock

        self.lamplist = []

        parent.title("Light Monitor")
        self.dataAquire()


    def remAllLights(self):
        self.lights = []
               
    def addLight(self,channel):
        newLight = LightWidget("%i" % channel,self.frame)
        self.lights.append(newLight)

        i = 0
        j = 0
        for l in self.lights:
            l.frame.grid(row=j,column=i)
            i = i+1

            if i % 5 is 0:
                j = j + 1
                i = 0

    def updateLight(self,channel,ncol,nintens):
        for l in self.lights:
            if l.chanel == str(channel):
                l.setColor(ncol)
                l.setIntens(int(nintens))
        
    def exitprog(self):
        self.frame.master.quit()
        sys.exit

    def dataAquire(self):
        
        # get the lamp data
        lampstemp = data_get(self.socket)

        # see if we've got nothing
        if lampstemp != [-1]:
            
            # see if we have new lamps
            if set(lampstemp) != set(self.lamplist):
                print("Received a lamp update")

                # delete old lamps
                self.remAllLights()
                            
                # put new lamps in UI
                for l in lampstemp:
                    self.addLight(l.chan)
                         
            # update the lamplist
            self.lamplist = lampstemp

            # update the UI
            for l in self.lamplist:
                self.updateLight(l.chan,l.color,l.intens)
        
        # call later
        self.parent.after(1,self.dataAquire)

# Data getter
def data_get(socket):
  
    # receive data
    try:
        data, addr = socket.recvfrom(1024)
    except:
        return [-1]
    
    data_in = data.decode()

    # split to list of lamp data
    lampDat = data_in.split(";")
    lampDat.remove('')
 
    # create a new lamp list
    lamps = []
    for d in lampDat:
        newLampDat = d.split(":")
        
        newLampChan = int(newLampDat[0])
        newLampIntens = float(newLampDat[1])
        newLampColor = newLampDat[2].split(",")

        newLamp = Lamp(newLampChan, newLampIntens, newLampColor)

        lamps.append(newLamp)
   
    return lamps

## MAIN ##

def main():

    print("Listening...")

    root = Tk()
    lm = LightMonitor(root)

    root.mainloop()
            
        
if __name__=='__main__':
    main()

    
