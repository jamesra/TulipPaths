#! /bin/bash

# Obtain a list of TulipPath plugin files
FILES=./*.py

HOME_DIR=$(eval echo '~')
TARGET_DIR="${HOME_DIR}/.Tulip-4.8/plugins/python"

# Make sure a directory exists for python plugins
if [ ! -d $TARGET_DIR ]; then
    mkdir "${HOME_DIR}/.Tulip-4.8/"
    mkdir "${HOME_DIR}/.Tulip-4.8/plugins/"
    mkdir "${HOME_DIR}/.Tulip-4.8/plugins/python/"
fi

# Copy each plugin script to the python plugin directory
for file in $FILES
do
    # Erase any existing compiled version of this plugin in the target
    # directory
    if [ -e "${TARGET_DIR}/${file}o" ]; then
        rm "${TARGET_DIR}/${file}o"
    fi

    cp $file "${TARGET_DIR}/"
done
