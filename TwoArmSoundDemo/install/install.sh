#!/bin/bash
if [[ `echo "$0" | grep "/" | wc -l` > 0 ]]; then
    cd ${0%/*}
fi
cd ..
PATH_TO_PACKAGE="$(pwd)"
NEW_ROS_LINE="export ROS_PACKAGE_PATH=\$ROS_PACKAGE_PATH:"$PATH_TO_PACKAGE
echo $NEW_ROS_LINE >> $HOME/.bashrc 
