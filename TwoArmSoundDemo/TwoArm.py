#!/usr/bin/env python

import roslib; roslib.load_manifest('TwoArmSoundDemo')
import rospy
import alsaaudio
import sys
import time
import audioop
import signal
from maestor.srv import *

ID_NUM = 4
MAX_POS = -2.95 #MAX POSITION IS NEGATIVE! This is very important 

def setProps(names, properties, values):
    try:
        rospy.wait_for_service('setProperties')
        service = rospy.ServiceProxy('setProperties', setProperties)
        service(names, properties, values)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def exitDemo(signal, frame):
    setProps("RSP LSP", "position position", "0 0")
    sys.exit()

if __name__ == '__main__':
    #Initialize and set the properties of PCM object
    card = 'default'
    audioInput = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    audioInput.setchannels(2)
    audioInput.setrate(44100)
    audioInput.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    audioInput.setperiodsize(160)
    oldL = 1
    oldR = 1
    #Initialize ros node and get a publisher from it
    #rospy.init_node("Noise_listener")
    rospy.wait_for_service("setProperties")

    #Set up the signal handler
    signal.signal(signal.SIGINT, exitDemo) 

    #The demo
    try:
        #Start an infite loop that gets and analyzes audio data
        count = 0
        while True:
            l, data = audioInput.read()
            if l:
                lchan = audioop.tomono(data, 2, 1, 0)
                rchan = audioop.tomono(data, 2, 0, 1)
                lmax = audioop.max(lchan, 2)
                rmax = audioop.max(rchan, 2)
                rposition = 0
                lposition = 0
                #Start the threshold checks
                # check rmax vs two thresholds 
                if rmax > 500: 
                    rposition =float('%.3f'%(MAX_POS * rmax/1000.0))
                    if(rposition < MAX_POS):
                        rposition = MAX_POS
                elif rmax < 70:
                    rposition = 0

                if lmax > 500: 
                    lposition =float('%.3f'%(MAX_POS * lmax/1000.0))
                    if(lposition < MAX_POS):
                        lposition = MAX_POS
                elif lmax < 70:
                    lposition = 0
                if oldR != rposition or oldL != lposition:
                    setProps("RSP LSP", "position position", str(rposition) + " " + str(lposition))  
                oldR = rposition
                oldL = lposition


                time.sleep(.001) #audio refresh rate
    except KeyboardInterrupt :
        pass
            
