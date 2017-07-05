#pd-extended -inchannels 1 -r 48000 -nogui -audiooutdev 6 bakamod.pd
echo 1 > /sys/class/leds/red_led/brightness
#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

if pgrep -x "pd-extended" > /dev/null
then
    echo "Running"
else
    echo "Stopped"
#    python /root/Adafruit_Python_PCA9685/examples/simpletest.py&
#    pd-extended -rt -oss -r 48000 -nogui -nomidi bakamod.pd&
fi
#pd-extended -rt -oss -r 48000 -nogui -nomidi bakamod.pd
#pd-extended -listdev -nogui
