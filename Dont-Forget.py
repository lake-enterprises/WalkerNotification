from firebase import firebase
from google.cloud import storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pygame
import time
from bt_proximity import BluetoothRSSI

BT_ADDR = '64:a2:f9:3c:ee:2e'  # You can put your Bluetooth address here
THRESHOLD = 15  # Threshold value under which the device will send a warning
BIN_SIZE = 10  # Number of measurements in running average
TIME_DELAY = 1  # Time between measurements in seconds
TX_POWER = 31  # Transmission power of Raspberry Pi Zero W in dBm
rssiList = []
pygame.mixer.init()


def main():
    
    database = firebase.FirebaseApplication('https://dont-forget-lake.firebaseio.com/', None)
    client = storage.Client()
    bucket = client.get_bucket('dont-forget-lake.appspot.com')
    blob = bucket.blob('./Audio/storage/emulated/0')
    blob.download_to_filename('./download.3gpp')
    pygame.mixer_music.load('./download.3gpp')
                       
    
    if BT_ADDR:
        addr = BT_ADDR
    else:
        print('No Bluetooth Address Found')  # Check whether address can be found
        return
    btrssi = BluetoothRSSI(addr=addr)
    rssiList = [btrssi.request_rssi() for _ in range(BIN_SIZE)]
    
    while True:  # Performs continual updates at an interval of TIME_DELAY
        rssi = btrssi.request_rssi()  # Get current RSSI
        rssiList.insert(0, rssi)  # Add RSSI to list
        rssiList.pop()  # Pop last element off list
        database.put('/pi', 'data', get_average(rssiList))

        if get_average(rssiList) < THRESHOLD:  # Check if average is below THRESHOLD - if yes, turn on output
            pygame.mixer_music.play(1)
            print('ALARM')

        time.sleep(TIME_DELAY)
        
def get_average(list):
    return sum(i[0] for i in list) / len(list)

if __name__ == "__main__":
    main()
