## PiFrameArtGen

This repository contains code I use to mathematically generate artwork to display on one of my photo frames! 

So far this just uses uniform destributions and the samila library to create math based artwork, but long term plan is to include multiple different mathematical ways to generate and render artwork throughout the day.

As of right now, the script in this repository generates a new artwork every 10 minutes and refreshes the eInk display.

## Frame Build
I used a waveshare eInk display, an old raspberry-Pi 3B, and a woodern frame off amazon build this. 

![](https://i.imgur.com/oQURlDj.jpg)

Links to parts below:

- [Display](https://www.waveshare.com/7.5inch-e-paper-hat.htm)
- [Frame](https://www.amazon.com/dp/B0BPS8GKX1)

## Start art generation at boot
To make the pi to automatically start rendering when booted up, I added the following to /etc/rc.local

```sudo -H -u {user} bash -c 'cd /home/pi/mathart && /usr/bin/python3 main.py'```