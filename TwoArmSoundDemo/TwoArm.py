#!/usr/bin/env python

import roslib; roslib.load_manifest('TwoArmSoundDemo')
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
    rospy.init_node("Noise_listener")
    pub = rospy.Publisher("Maestro/Control", PythonMessage)
    print "Turning Interpolation On"
    time.sleep(.5);
    pub.publish("", "SetMode", "Interpolation", "true")
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
                    rposition =(-3.14 * rmax/1000.0)
                    if(rposition < -3.14):
                        rposition = -3.14
                elif rmax < 70:
                    rposition = 0

                if lmax > 500: 
                    lposition =(-3.14 * lmax/1000.0)
                    if(lposition < -3.14):
                        lposition = -3.14
                elif lmax < 70:
                    lposition = 0
                if count == 20:
                    pub.publish("RSP LSP", "position position", str(rposition) + " " + str(lposition), "")  
                    count = 0
                count = count + 1


                time.sleep(.001) #audio refresh rate
    except KeyboardInterrupt :
        sys.exit() #TODO make it actually exit
            
