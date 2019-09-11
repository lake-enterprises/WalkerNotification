from bt_rssi import BluetoothRSSI
from gpiozero import LED
from time import sleep
from firebase import firebase
import time
import sys

BT_ADDR = '7:EB:B1:A2:E0'   # You can put your Bluetooth address here 
THRESHOLD = -15             # Threshold value under which the device will send a warning
BIN_SIZE = 10               # Number of measurements in running average
TIME_DELAY = 1              # Time between measurements in seconds
TX_POWER = 31                                   # The tranmission power of the Raspberry Pi in use



def main():
    firebase = firebase.FirebaseApplication('https://dont-forget-lake.firebaseio.com', None)
    btrssi = BluetoothRSSI(addr=BT_ADDR)
    rssiList = [btrssi.get_rssi() for _ in range(BIN_SIZE)] # Populate initial list up to BIN_SIZE
    
    while True:                                    # Performs continual updates at an interval of TIME_DELAY
        rssi = btrssi.get_rssi()                    # Get current RSSI
        rssiList.insert(0, rssi)                     # Add RSSI to list
        rssiList.pop()                            # Pop last element off list
        distance = firebase.put('/pi',{'disance':'test'})
        
        #if(getAverage(rssiList) < THRESHOLD):       # Check if average is below THRESHOLD - if yes, turn on output
           # print('ALARM')
        
        time.sleep(1)


def get_average(l):                               # Return average of current list of RSSI values
    average = sum(l) / len(l)
    return average

def get_distance(rssi, txpower):
    ratio = rssi / txpower
    if ratio < 1:
        return ratio**10
    else:
        return 0.89976 * (ratio**7.7095) + 0.111

if __name__ == "__main__":
    main()



