#!/usr/bin/env python

import roslib; roslib.load_manifest('hubomsg')
import rospy
import alsaaudio
import sys
import time
import audioop
from hubomsg.msg import PythonMessage

if __name__ == '__main__':
    #Initialize and set the properties of PCM object
    card = 'default'
    audioInput = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    audioInput.setchannels(2)
    audioInput.setrate(44100)
    audioInput.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    audioInput.setperiodsize(160)
    #Initialize ros node and get a publisher from it
    #rospy.init_node("Noise_listener")
    #pub = rospy.Publisher("Maestro/Control", PythonMessage)
    try:
        #Start an infite loop that gets and analyzes audio data
        while True:
            l, data = audioInput.read()
            if l:
                lchan = audioop.tomono(data, 2, 1, 0)
                rchan = audioop.tomono(data, 2, 0, 1)
                print "L: " + str(audioop.max(lchan, 2))
                print "R: " + str(audioop.max(rchan, 2))
                time.sleep(.001) #audio refresh rate
    except KeyboardInterrupt :
        sys.exit() #TODO make it actually exit
            
