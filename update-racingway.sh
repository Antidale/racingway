#!/bin/bash

# kill current process, move current bot to backup, clear old log file
kill $(ps aux | grep '[r]acingway' | awk '{print $2}')
cd ~/src/racingway
git pull

#make sure things are set up correctly
source ./ENV/bin/activate
pip install -e .

nohup racingway ff4fe $Racetime_Client_Id $Racetime_Client_Secret -v >> nohup.out 2>&1 &

# Give the bot some startup time and write out the current log file contents
sleep 3 
cat nohup.out