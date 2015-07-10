#! /usr/bin/python2

import sys
import threading, time, json, datetime
import OSC

class SaltoPlayer():
    def __init__(self, filename):
        self.filename = filename
        self.server_address = '172.16.9.80'
        self.server_port = 14040

        self.client = OSC.OSCClient()
        self.client.connect((self.server_address, self.server_port))

    def run(self):
        print('Replaying recording ...')
        with open(self.filename, 'r') as thefile:
            for line in thefile:
                msg = json.loads(line)
                oscmessage = OSC.OSCMessage('/salto2/sensor')
                oscmessage.append(msg)
                self.client.send(oscmessage)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please supply filename')
    else:
        filename = sys.argv[1]
        sp = SaltoPlayer(filename)
        sp.run()
