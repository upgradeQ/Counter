# Obscounter
Python implementation of hotkey counter in OBS studio.  
- ![prevew](counter.gif)
- ![ui](https://i.imgur.com/UobLYdS.png)
- ![hotkeys](https://i.imgur.com/dEC2Y6M.png)
# Installation 
- Download [source code](https://github.com/upgradeQ/Obscounter/archive/master.zip), unpack/unzip.
- Add `hotkey_counter.py` to OBS Studio via Tools > Scripts > "+" button
# Setup
For windows install [python3.6](https://www.python.org/downloads/release/python-368/) 64 or 32 bit depending on your OBS 
- Create text source
- Open `Tools>Scripts` 
- Make sure Python path is not empty
- Add and select this script
- Set settings for it
- Set hotkeys in `File>Settings`
If you need additional COUNTERS , copy paste `hotkey_counter.py` , and add it again
# See also
There is [`Lua alternative`](https://gist.github.com/tid-kijyun/477c723ea42d22903ebe6b6cee3f77a1) with helpful blogpost(JP)
on how to install and setup those kinds of scripts in OBS.
Lua support in OBS Studio is built-in , so you don't need install anything extra.
# Contribute 
Contributions are welcome
