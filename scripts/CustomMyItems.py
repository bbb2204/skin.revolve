# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.

import sys
import xbmc

from xbmc_property import *

SCRIPT_NAME = 'Revolve/PopulateListFromHomeProperties'
TARGET_WINDOW = '1102'
TOTAL_ITEMS = 20

def logMessage(annotation):
    message = '%s: %s' % (SCRIPT_NAME, annotation.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def createNameProperty(originbase, destination):
    value = getValueFromHomeProperty(originbase + '.Title')
    value = replaceEmptyValueFromHomeProperty(originbase + '.EpisodeTitle', value)
    setValueToProperty(destination, value, TARGET_WINDOW)
    
def createSubtitleProperty(originbase, destination):
    value = joinLabels(
        getValueFromHomeProperty(originbase + '.ShowTitle'),
        getValueFromHomeProperty(originbase + '.TVShowTitle'),
        getValueFromHomeProperty(originbase + '.Studio'),
        getValueFromHomeProperty(originbase + '.Artist'),
        getValueFromHomeProperty(originbase + '.Author'),
        getValueFromHomeProperty(originbase + '.Album'),
        ignoreNumericZeroValue(getValueFromHomeProperty(originbase + '.Year')),
        ignoreNumericZeroValue(getValueFromHomeProperty(originbase + '.Version')))
    setValueToProperty(destination, value, TARGET_WINDOW)
    
def createIconProperty(originbase, destination):
    value = getValueFromHomeProperty(originbase + '.Art(poster)')
    value = replaceEmptyValueFromHomeProperty(originbase + '.Thumb', value)
    setValueToProperty(destination, value, TARGET_WINDOW)
    
def createBackgroundImageProperty(originbase, destination):
    value = getValueFromHomeProperty(originbase + '.Art(fanart)')
    value = replaceEmptyValueFromHomeProperty(originbase + '.Art(fanart_image)', value)
    value = replaceEmptyValueFromHomeProperty(originbase + '.Fanart', value)
    setValueToProperty(destination, value, TARGET_WINDOW)
    
def createActionProperty(originbase, destination):    
    value = getValueFromHomeProperty(originbase + '.Play')
    if value == '':
        value = addPrefixAndSuffixToLabel(getValueFromHomeProperty(originbase + '.Path'), 'PlayMedia("', '")')
        print(value)
    if value == '':
        value = getValueFromHomeProperty(originbase + '.LibraryPath')
    setValueToProperty(destination, value, TARGET_WINDOW)
    

def copyProperties(originmask):
    for index in range (1, TOTAL_ITEMS):
        originbase = originmask % (index)
        destinationbase = 'MyItems%02dOption' % (index)

        createNameProperty(originbase, destinationbase + '.Name')
        createSubtitleProperty(originbase, destinationbase + '.Subtitle')
        createIconProperty(originbase, destinationbase + '.Icon')
        createBackgroundImageProperty(originbase, destinationbase + '.BackgroundImage')
        createActionProperty(originbase, destinationbase + '.Action')


if len(sys.argv) >= 2:
    logMessage('Call to ' + SCRIPT_NAME + ' script with arguments: ' + str(sys.argv) + '.')	
    menuname = sys.argv[1]
    originmask = sys.argv[2]

    logMessage(SCRIPT_NAME + ' copies properties: ' + sys.argv[2] + ' to MyItems-properties')	
    copyProperties(originmask)
else:
    logMessage(SCRIPT_NAME + ' terminates: Missing argument(s) in call to script.')	
