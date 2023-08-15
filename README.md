# KiriKiri .XP3 archive repacking and extraction tool COMMAND LINE! You can use it in GitHub Actions!

Based on original script by Edward Keyes, ed-at-insani-dot-org, 2006-07-08, http://www.insani.org/tools/  
and SmilingWolf, https://bitbucket.org/SmilingWolf/xp3tools-updated

Based on Python 3 rewrite, Awakening

Enhanced by Kiriha!

[中文](README_zh.md)

## Introduction

Extracts an .XP3 archive to a directory of files, and
packs a directory of files into an .XP3 archive, including any
subdirectory structure.

Uses Numpy (if available) to speed up decryption/encryption.

## Features

Adapt multiple encryption schemes, you can add your own encryption scheme easily!

Please see game_list.py for more information.
