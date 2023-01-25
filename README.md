# Obscounter

Python implementation of hotkey counter in OBS studio.

![prevew](counter.gif)

# Requirements

For windows install [python3.6](https://www.python.org/downloads/release/python-368/) 64 or 32 bit depending on your OBS 

# Installation 

1. Download [source code](https://github.com/upgradeQ/Obscounter/archive/master.zip).
2. Unzip the file to be able to access `hotkey_counter.py`. Remember the file location because you will need this later.

# Usage

1. On OBS, under Sources, click + to create a new text source (below, you will see Text GDI+). You may leave it blank.

![image](https://user-images.githubusercontent.com/2420577/214267000-44e091a0-eadb-43a2-ac68-d8763b172320.png)

2. On the OBS menu, click `Tools > Scripts`

![image](https://user-images.githubusercontent.com/2420577/214267186-562deac4-ee82-46df-8ebc-5278f9429f64.png)

3. Under the `Python Settings` tab, make sure the Python path is configured.

![image](https://user-images.githubusercontent.com/2420577/214267353-7155c08d-f9eb-4053-a17f-34ada6af86f5.png)

4. Under the `Scripts` tab, click the + sign to add this script.

![image](https://user-images.githubusercontent.com/2420577/214267447-cb5de6cc-5b98-44d6-bb5f-cccff76be836.png)

5. Close the scripts window, and return to your OBS window and configure OBS settings by clicking `File > Settings`.

6. Configure the hotkeys.

![ui](https://i.imgur.com/UobLYdS.png)

![hotkeys](https://i.imgur.com/dEC2Y6M.png)

## How do I use more counters?

If you need additional counters, duplicate the `hotkey_counter.py` file and save it with a new filename (e.g. `hotkey_counter2.py`), and repeat the process.

# Potential issues

OBS sometimes does not want to play nicely with Python, and [sometimes requires a specific Python version e.g. 3.6.4](https://obsproject.com/forum/threads/cant-seem-to-get-the-obs-python-library-to-work-correctly-help-pls.101339/). 

# Alternatives

There is a [`LUA alternative`](https://gist.github.com/tid-kijyun/477c723ea42d22903ebe6b6cee3f77a1) with helpful blogpost (JP)
on how to install and setup those kinds of scripts in OBS. Lua support in OBS Studio is built-in , so you don't need install anything extra.

# Contribute 

Contributions are welcome.
