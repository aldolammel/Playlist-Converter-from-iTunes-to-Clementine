# Playlist Converter: from iTunes to Clementine
>*Author: @aldolammel*

>*Public repository: https://github.com/aldolammel/Playlist-Converter-from-iTunes-to-Clementine*

This simple app converts your iTunes playlists from .xml to .xspf files used by Clementine's playlists. 

__

## APP FEATURES

- It converts .xml to .xspf for Clementine format;
- You can customize your music folder path for each OS (Windows or Linux);
- Latin-based and Cyrillic-based words are supported on files path;
- Free to use, copy, modify etc.

**Known bugs:**
- If you store exported playlists (.xspf) on online repositories like GitHub, don't download them directly by browser because it destroys .xspf encoding some how, including in each file many junk-html-lines, breaking the file.

__

## HOW TO INSTALL

Video demo: soon

1) Download this repository;
2) Make sure you have installed Python v3.12+;
3) Go to the repository folder;
4) On your iTunes, export each playlist (using .xml format) you wanna use in Clementine;
5) Move all playlists to the "to_converted" folder in your local repository folder;
6) On terminal, go to the root of your local repository folder;
7) Run the command: python3 converter.py
8) The converted playlists (.xspf) are in "converted" folder in the local repository folder;

;)

__

## IDEA AND FIX?

aldolammel@gmail.com

__

## CHANGELOG

**Jun, 4th 2025 | v0.1**
- Hello world.