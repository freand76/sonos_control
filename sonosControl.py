#!/usr/bin/python3

from meross_iot.manager import MerossManager
from meross_iot.cloud.devices.power_plugs import GenericPlug
from soco.discovery import by_name
import time
import sys

merossEMAIL = ""
merossPASSWORD = ""
verbose=False

def printVerbose(string):
    if verbose:
        print(string)
        
def getPlayState():
    device = by_name("Matrum")
    if device == None:
        return False
    playState=device.group.coordinator.get_current_transport_info()['current_transport_state']
    playBool=transportToState(playState)
    return playBool
    
def changePlugState(state):
    try:
        manager = MerossManager(meross_email=merossEMAIL, meross_password=merossPASSWORD)
    except:
        return;

    manager.start()
    plug = manager.get_device_by_name('Stereo')
    if plug == None:
        return
    
    if state:
        plug.turn_on()
    else:
        plug.turn_off()

def transportToState(transport):
    switcher = {
        'PLAYING': True,
        'TRANSITIONING': True,
        'PAUSED_PLAYBACK': False,
        'STOPPED': False,        
        }
    return switcher.get(transport)

## Here we GO!
playState = getPlayState()
ampState = False
ampTimeout = 0

if len(sys.argv) > 1:
    verbose=True
    printVerbose("Verbse Output")

credentialsFile='/opt/sonos_control/merossCred.txt'
credDict = {}
for line in open(credentialsFile).readlines():
    key, val = line.strip().split('=')  # Remove \n and split on =
    credDict[key.strip()] = val.strip()

merossEMAIL=credDict['EMAIL']
merossPASSWORD=credDict['PASSWORD']

if playState:
    changePlugState(True)
    ampState = True
    
while True:
    time.sleep(1)
    newPlayState = getPlayState()
    if newPlayState == playState:
        # Decrease timeout counter if 
        if ampState == True and playState == False:
            if ampTimeout > 0:
                ampTimeout = ampTimeout - 1
                printVerbose("Timeout: %d"%ampTimeout)
            elif ampTimeout == 0:
                printVerbose('Off')
                changePlugState(False)
                ampState = False
        continue

    playState = newPlayState
    if playState:
        # Just started playing
        printVerbose('On')
        changePlugState(True)
        ampState = True
    else:
        # Just stopped playing, set turn off timeout
        ampTimeout = (15*60)
