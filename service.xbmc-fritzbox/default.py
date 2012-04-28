# Open Source Initiative OSI - The MIT License (MIT):Licensing
#[OSI Approved License]
#The MIT License (MIT)

#Copyright (c) 2011 N.K.

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# ################################################################################
# author: nk
#
# ################################################################################

# Script constants
__addon__       = "XBMC Fritzbox Addon"
__addon_id__    = "service.xbmc-fritzbox"
__author__      = "N.K."
__url__         = "http://code.google.com/p/xbmc-pbx-addon/"
__version__     = "0.9.1"

import xbmc, xbmcaddon
import socket
import os


# [1]
#Default Fehler
def errorMsg(aList):
    text = "Unhandled State"
    xbmc.log(text)

#AusgehendeAnrufe
def handleOutgoingCall(aList):
    #datum;CALL;ConnectionID;Nebenstelle;GenutzteNummer;AngerufeneNummer;
    #[192.168.178.1] 03.01.12 22:09:56;CALL;0;0;123456;017500000;SIP1;
    datum, funktion, connectionID, Nebenstelle, GenutzteNummer, AngerufeneNummer, sip,  leer = aList
    text = ('Ausgehender Anruf an %s von Nr: %s, am %s' % (AngerufeneNummer, GenutzteNummer, datum))
    #print text
    xbmc.log(text)
    xbmc.executebuiltin("Notification(XBMC-Fritzbox,"+text+",5000,"+DEFAULT_IMG+")")


#EingehendeAnrufe:
def handleIncomingCall(aList):
    #datum;RING;ConnectionID;Anrufer-Nr;Angerufene-Nummer;sip;
    #[192.168.178.1] 03.01.12 21:52:21;RING;0;017100000;012345;SIP2;
    datum, funktion, connectionID, anruferNR, angerufeneNR, sip, leer = aList
    text = ('Eingehender Anruf von %s auf Apparat %s' % (aList[3], aList[4]))
    #print text
    xbmc.log(text)
    xbmc.executebuiltin("Notification(XBMC-Fritzbox,"+text+",5000,"+DEFAULT_IMG+")")

#Zustandegekommene Verbindung:
def handleConnected(aList):
    #datum;CONNECT;ConnectionID;Nebenstelle;Nummer;
    datum, funktion, connectionID, nebenstelle, nummer, leer = aList
    text = ('Verbunden mit %s' % (nummer))
    #print text
    xbmc.log(text)
    xbmc.executebuiltin("Notification(XBMC-Fritzbox,"+text+",5000,"+DEFAULT_IMG+")")

#Ende der Verbindung:
def handleDisconnected(aList):
    #datum;DISCONNECT;ConnectionID;dauerInSekunden;
    #[192.168.178.1] 03.01.12 22:12:56;DISCONNECT;0;0;
    datum, funktion, connectionID, dauer,  leer = aList
    text = ('Disconnected. Your call duration was %s seconds' % (dauer))
    #print text
    xbmc.log(text)
    xbmc.executebuiltin("Notification(XBMC-Fritzbox,"+text+",5000,"+DEFAULT_IMG+")")

#run the program
xbmc.log("xbmc-fritzbox ShowCallerInfo-Service starting...")
DEFAULT_IMG = xbmc.translatePath(os.path.join( "special://home/", "addons", "service.xbmc-fritzbox", "media","default.png"))
Addon = xbmcaddon.Addon(id='service.xbmc-fritzbox')
ip = "192.168.178.1"
parameterstring = "Fritzbox: Ip Adresse definiert als %s" % ( ip)
xbmc.log(parameterstring)
fncDict = {'CALL': handleOutgoingCall, 'RING': handleIncomingCall, 'CONNECT': handleConnected, 'DISCONNECT': handleDisconnected}

while(not xbmc.abortRequested):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.connect((ip, 1012))
        while True:
            xbmc.log('connected to fritzbox callmonitor')
            antwort = s.recv(1024) 
            log= "[%s] %s" % (ip,antwort)
            xbmc.log(log)
            items = antwort.split(';')
            fncDict.get(items[1], errorMsg)(items)
        s.close()
    except IndexError:
        text = 'ERROR: Something is wrong with the message from the fritzbox'
        #print text
        xbmc.log(text)
    except socket.error, msg:
        text = 'ERROR: Could not connect fritz.box on port 1012'
        xbmc.log(text)
    finally:
        s.close()

