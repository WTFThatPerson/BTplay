# BTplay
Bluetooth audio output switching for Kodi 18 on Linux
Switches audio output between current device and bluealsa.

PREREQUISITES
1. Bluealsa up and running
2. Bluetooth device connected to system (obviously, it has to be trusted to connect automatically)
3. "Allow remote control via HTTP" in Kodi settings turned on

It stores current audio device before switch to Bluealsa and restores it after bluealsa switched off.

USING
- Input Your port number and credincials from Kodi's "Web server" settings page (Settings -> Control -> Web server)
- If port number isn't inputted, addon falls back to standard HTTP port 80 which is probably not what You want
- If username or password isn't inputted, addon omits authorization, so minimalistic setting is port number only; 
  one should use username/password fields only if it used in Kodi itself.
- If You select Bluetooth play multiple times by mistake, it doesn't lead to errors - right non-BT device will be restored anyway

P.S. I can't remember where I found icon for that addon, so my apologies to that person in copyright meaning.
