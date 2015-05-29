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
MAX_POS = -2.95 #MAX POSITION IS NEGATIVE! This is very important, the arms go forward with negative radians

'''
Function to show how to call the set properties service using ros python service calls
'''
def setProps(names, properties, values):
    try:
        rospy.wait_for_service('setProperties')
        service = rospy.ServiceProxy('setProperties', setProperties)
        service(names, properties, values)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

'''
Signal handling so the demo finishes smoothly
'''
def exitDemo(signal, frame):
    setProps("RSP LSP", "position position", "0 0")
    sys.exit()

if __name__ == '__main__':
    #Initialize and set the properties of PCM object, this is how we capture sound using ALSA
    card = 'default'
    audioInput = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    audioInput.setchannels(2)
    audioInput.setrate(44100)
    audioInput.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    audioInput.setperiodsize(160)
    oldL = 1 #Variable for the old left value
    oldR = 1 #Variable for the old right value
    #Wait for the service setProperties to become available before continuing. 
    rospy.wait_for_service("setProperties")

    #Set up the signal handler
    signal.signal(signal.SIGINT, exitDemo) 

    #The demo
    try:
        #Start an infite loop that gets and analyzes audio data
        count = 0
        while True:
            l, data = audioInput.read() #Read a sample of audio
            if l:  #If successful
                #Split the data into two channels, a left one and right one
                lchan = audioop.tomono(data, 2, 1, 0)
                rchan = audioop.tomono(data, 2, 0, 1)
                #Find the maximum intensity for each of the channels and store it 
                lmax = audioop.max(lchan, 2)
                rmax = audioop.max(rchan, 2)
                #These are the positions that we will set the shoulder pitch to
                #Possible TODO During workshop: Change the way that we set the position to an incremental system, 
                #   where if we are above the threshold move up a little and below move down a little 
                rposition = 0
                lposition = 0
                #Start the threshold checks
                # check rmax vs two thresholds 
                if rmax > 500: #If above the 500 unit threshold calculate a position 
                    rposition =float('%.3f'%(MAX_POS * rmax/1000.0))
                    if(rposition < MAX_POS):
                        rposition = MAX_POS
                elif rmax < 70:
                    rposition = 0
                # check lmax vs two thresholds
                if lmax > 500: 
                    lposition =float('%.3f'%(MAX_POS * lmax/1000.0))
                    if(lposition < MAX_POS):
                        lposition = MAX_POS
                elif lmax < 70:
                    lposition = 0
                # if the position changed then call the service, this is to prevent rapidly calling unnecssarily 
                if oldR != rposition or oldL != lposition:
                    setProps("RSP LSP", "position position", str(rposition) + " " + str(lposition))  #Our helper function
                oldR = rposition #update to the new position values
                oldL = lposition #update to the new position values


                time.sleep(.001) #audio refresh rate
    except KeyboardInterrupt :
        pass
            
