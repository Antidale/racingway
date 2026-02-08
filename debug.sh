#make sure things are set up correctly
source ./ENV/bin/activate
pip install -e .

# Start the bot setting it to run vs a local rt.gg instance and to not enforce https
racingway ff4fe --host localhost:8000 --insecure $Local_RTGG_Client_ID $Local_RTGG_Client_Secret
