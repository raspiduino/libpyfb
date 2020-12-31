# libpyfb
Python library for controling raw framebuffer. Written in pure Python.

## What is this?
libpyfb is a low-level framebuffer control library written in Python. This work on all Linux devices, include x86, x86_64 and ARM.

## Why made this?
Currently, there is no low-level Python module for direct writing to framebuffer. Pygame still require SDL and other C libraries. Their is also <a href="https://gist.github.com/FredEckert/3425429">a gist</a> in C about this and also a Go script <a href="https://github.com/kaey/framebuffer">here</a>
<br>So I made this small library for doing that. Have fun!

## How this work?
Linux Framebuffer can be easily accessed in /dev/fb0. Like any other file, this can be read and write to (if the user in video group). So this library will open fb0, map it to memory and control the screen from that. Each pixel is 4 bytes (32 bit) or 2 bytes (16 bit). These bytes are B, G, R and one transparency bytes.

## Todo
- Add graphical drawing
- Add mouse and keyboard support

## License
Under MIT license.

And one last thing...
Enjoy your 2021!
