# Velociraptor-Bot
A discord bot for managing servers.

## Description
A multi-purpose discord bot to be used on a private server with my friends. 
This bot provides basic security for our server with an easily customizable verification system. 
Important e-learnig and virtual learning commands that can reply with my school’s schedule and per class zoom links. 
The bot can also join voice channels and play different sound effects stored as .mp3 files.

## Primary Dependencies
- discord.py
  - The python library to access the discord api. This allows a user to access the "control system" for their discord bot, perform actions as a bot, and gather data as a bot. 
  - This project demonstrates a strong understanding of how to use this library, as well as follow the suggested abstraction procedures (use of COGS)
- json
  - This library allows a dictionary to be easily stored as a .json file, as well as read a .json file into a dictionary
  - This project utilizes this to keep some data persistant, such as server and user preferences, along with custom calender data.
  - Some issues I had to overcome when working with saving data was *when* to do so - opening, saving, and closing a file every 
  time a change was made proved to be extremely inefficient and sometimes led to the file corrupting. 
  I solved this by setting up a timed async loop that saves the data every 5 minutes.
  
## Features and implementations
- List Comprehension
  - Something I'm quite proud of in this project, is my use of list comprehension - this is a powerful shorthand to generate lists in python. 
  Overall, they can help to shorten/cleanup code and often times are more efficient
  - An example from this project:
    - `counter = [m for m in velo.members if m.status in [discord.Status.online, discord.Status.do_not_disturb] and m.name not in bots]`
