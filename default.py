# -*- coding: utf-8 -*-

#/*
# *      Copyright (C) 2021 StrangeAlien
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, see
# *  <http://www.gnu.org/licenses/>.
# *
# */


import sys
import os
import xbmc
import xbmcvfs
import xbmcaddon
import xbmcgui
import requests
import json
import base64

ADDON      = xbmcaddon.Addon()
ADDONNAME  = ADDON.getAddonInfo('name')
ADDONID    = ADDON.getAddonInfo('id')
VERSION    = ADDON.getAddonInfo("version")

def log(txt):
    xbmc.log("##### [%s] - Version: %s: %s" % (ADDONNAME,VERSION,txt),level=xbmc.LOGDEBUG)

if __name__ == '__main__':

  log('Started')

  port = ADDON.getSetting('port')
  username = ADDON.getSetting('username')
  password = ADDON.getSetting('password')

  url = 'http://127.0.0.1:' + port + '/jsonrpc'

  if username == '' or password == '':
    headers={'content-type': 'application/json'}
  else:
    password = username + ':' + password
    password = base64.b64encode(password.encode('ascii'))
    password = 'Basic ' + password.decode('ascii')
    headers={'content-type': 'application/json', 'Authorization': password}  

  path = xbmc.translatePath('special://profile/addon_data/' + ADDONID + '/').decode('utf-8')
  pathdir = xbmc.validatePath(path)
  if not xbmcvfs.exists(pathdir):
      pathdir = xbmcvfs.mkdirs(pathdir)
  path = xbmc.validatePath(path +'current')
  if xbmcvfs.exists(path):
      log('Bluetooth device already switched on')
      with open(path, 'r') as fd:
        CurrentDevice = fd.read()
      log("Current audio device: %s" % CurrentDevice)
  else:
      r = requests.post(url,
          data='{"jsonrpc":"2.0","method":"Settings.GetSettingValue", "params":{"setting":"audiooutput.audiodevice"},"id":1}',
          headers=headers)
      CurrentDevice = r.json()['result']['value']
      with open(path, 'w') as fd:
        fd.write(CurrentDevice)
      log('Current audio device stored')

  sel = -1

  try:
    dialog = xbmcgui.Dialog()

    if len(sys.argv) == 1:
      sel = dialog.contextmenu(["Switch on Bluetooth play","Switch off Bluetooth play"])
    else:
      sel = ["Switch on Bluetooth play","Switch off Bluetooth play"].index(sys.argv[1])

    if sel == 0:
      r = requests.post(url,
          data='{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice", "value": "' + CurrentDevice +'"},"id":1}',
          headers=headers)
      r = requests.post(url,
          data='{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice", "value": "ALSA:bluealsa"},"id":1}',
          headers=headers)
    elif sel == 1:
      r = requests.post(url,
          data='{"jsonrpc":"2.0","method":"Settings.SetSettingValue", "params":{"setting":"audiooutput.audiodevice", "value": "' + CurrentDevice +'"},"id":1}',
          headers=headers)
      pathdir = xbmcvfs.delete(path)
  except:
    pass

sys.modules.clear()
