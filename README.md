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
* PP System (not recommended to use as the implementation of it is retarded)
* Fully-working osu!droid server
* Insert more :)

## Todo
* Everytime a player sends a request they send an sign parameter, idk what to do with it yet.

## Requirements
* [ConEmu](https://conemu.github.io/) FOSS windows terminal emulator.
* [Python 3.8+](https://www.python.org/downloads/release/python-386/)
* [Notepad++](https://notepad-plus-plus.org/downloads/)
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

* Download [Apktool](https://ibotpeaches.github.io/Apktool/), [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer) and osu!droid.apk from it's website
* Create an folder somewhere in your pc and copy all of the file there
* Do `java -jar apktool.jar d droid.apk` and wait till the thing completes
* Open the folder and go to `smali\ru\nsu\ccfit\zuev\osu` and open Notepad++
* Ctrl+F into Notepad++ and go to `Find in Files` tab and do as below. Note that the directory may be different from the screenshot.</br>
![ss](https://yuzumi.please-end.me/IDI8p4.png)
* You will get something like this 
![ss](https://yuzumi.please-end.me/pxYs30.png)
* If you did then put your domain/ip into the `Replace with` box, if not then try again till you find it.
![ss](https://yuzumi.please-end.me/EgdG4F.png)
* After that, search for `secure.gravatar.com` and replace it with your domain
* Okay, we're almost there.
* Go back to the folder that you created and do `java -jar apktool.jar b droid` and the apk should be in `droid\dist` after it completes.
* Do `java -jar signer.jar -a droid\dist\droid.apk --out droid_sign` and there should be `droid-aligned-debugSigned.apk` in the `droid_sign folder`
* and... That's it holy shit thats alot of steps.
* You can now use the modified .apk to connect to the server without doing the Hosts stuff.



## Disclaimer
This is my first time working with this kind of stuff so if I do stupid stuff please say so :)
