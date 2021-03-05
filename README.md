## I'm gonna do a rewrite, just wait for 2 years
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
* Custom avatar server (need .apk modification to work)
* PP System (osu!std pp system)
* _Fully-working_ osu!droid server
* Insert more :)

## Todo
* Sign Parameter
* Apis [Partially added]
* MySql Support

## Requirements
* [ConEmu](https://conemu.github.io/) FOSS windows terminal emulator.
* [Python 3.8+](https://www.python.org/downloads/release/python-386/)
* [Notepad++](https://notepad-plus-plus.org/downloads/)
* Python and general-programming knowledge.
* An Domain or IP address

## Setting up (server)
* Install the necessary python packages with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`
* Copy `config.sample.py` and name it `config.py`
* Edit `config.py`, [osu!api](https://old.ppy.sh/) (optional unless you're using pp system)
* That's it. You can setup nginx and those web stuff if you want.

## Setting up (client)
There's two way of doing this, hosts and modified .apk.
If you only want to use Yuzumi as a score server and nothing else then go with hosts

### Hosts
* Install [Hosts Go](https://play.google.com/store/apps/details?id=dns.hosts.server.change&hl=en&gl=US) from Google Play or other site
* Add `ops.dgsrz.com` with your server ip address.
* That's it

### Apk (Recommended)
There's also two way of doing this, build from sources or modified .apk.<br/>
Since I don't commit java, we're going with the latter.

You need java installed for this (the same one that you need for Minecraft :>)

Update: There's a script for this now, you can use that if you're retarded or lazy like me <br/>
[[Script]](https://github.com/FireRedz/osudroid-patch) <br/>
[[Manual]](https://github.com/FireRedz/osudroid-patch/blob/master/old.md)



## Disclaimer
This is my first time working with this kind of stuff so if I do stupid stuff please say so :)
