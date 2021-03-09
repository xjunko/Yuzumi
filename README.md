<h2 align="center">
	osu!droid Server
</h2>

<h4 align="center">
	meme server
</h4>

<p align="center">
	<img height=300 src="https://files.catbox.moe/1jhzz0.jpg" alt="anime girl doing anime stuff">
</p>


## Features
* _Fully-working_ osu!droid server
* PP System (osu!std pp system)
* Insert more :)

## Todo
* MySQL Support

## Requirements
* [ConEmu](https://conemu.github.io/) FOSS windows terminal emulator, (you can use your os default console, this is just for aesthetic if anything).
* [Python 3.8+](https://www.python.org/downloads/release/python-386/) (Recommended: Python 3.8.6)
* [Notepad++](https://notepad-plus-plus.org/downloads/)
* Python and general-programming knowledge.
* An Domain or IP address

## Setting up (server)
* Install the necessary python packages with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`
* Copy `config.sample.py` and name it `config.py`
* Edit `config.py`, [osu!api](https://old.ppy.sh/p/api) (optional unless you're using pp system)
* That's it. You can setup nginx and those web stuff if you want.
* To run you can use `python3.8 main.py` (Development) or `hypercorn main.py` (Production)

## Setting up (client)
There's two way of doing this, hosts and modified .apk. <br/>
Hosts method is better since you can change between servers without downloading apks.

### Hosts
* Install [Hosts Go](https://play.google.com/store/apps/details?id=dns.hosts.server.change&hl=en&gl=US) from Google Play or other site
* Add `ops.dgsrz.com` with your server ip address.
* That's it

### Apk
There's also two way of doing this, build from sources and modified .apk.<br/>
Since I don't commit java, we're going with the latter.

You need java installed for this (the same one that you need for Minecraft :>)

Update: There's a script for this now, you can use that if you're retarded or lazy like me <br/>
[[Script]](https://github.com/FireRedz/osudroid-patch) <br/>
[[Manual]](https://github.com/FireRedz/osudroid-patch/blob/master/old.md)



## Disclaimer
This is my first time working with this kind of stuff so if I do stupid stuff please say so :)

