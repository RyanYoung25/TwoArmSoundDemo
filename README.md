****************************************************
**************       INTRODUCTION      *************
****************************************************

This repository contains a ROS package that runs a two arm sound demo for hubo through MAESTRO. The demo listens to raw pcm audio from two channels and raises and lowers hubo's arms relative to the volume of noise heard on each channel. 

****************************************************
**************       REQUIREMENTS      *************
****************************************************

- Ubuntu 12.04 LTS
- ROS Fuerte
- MAESTRO (ROS stack)
- pyalsaaudio (http://pyalsaaudio.sourceforge.net/)

****************************************************
**************       INSTALLATION      *************
****************************************************
Add a line in your ros package path pointing to this package. If you don't know how to do this,
add a line like this to your .bashrc :

export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$HOME/path/to/this/package 

Once added to the Ros path, run a rosmake.

****************************************************
*******************    RUN    **********************
****************************************************

This package can be launched through a roslaunch:

roslaunch TwoArmSoundDemo demo.launch

It can also be run like any other python script. 

****************************************************
*******************    STOP   **********************
****************************************************

The demo stops with ctrl-c, the sigint signal.  



