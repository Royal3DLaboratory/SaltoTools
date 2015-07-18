#! /usr/bin/python2

import sys
import argparse
import threading, time, json, datetime
import OSC

class SaltoPlayer():
    ''' Play Salto recordings and send the OSC data to a listening
        server.
    '''

    def __init__(self, filename, server_address, server_port):
        self.filename = filename
        self.server_address = server_address
        self.server_port = server_port

        self.client = OSC.OSCClient()
        self.client.connect((self.server_address, self.server_port))


    def run_thread(self):
        with open(self.filename, 'r') as thefile:
            for line in thefile:
                timedelta, msg = json.loads(line)
                oscmessage = OSC.OSCMessage('/salto2/sensor')
                oscmessage.append(msg)

                #Sleep a little sleep
                time.sleep(timedelta)
                self.client.send(oscmessage)


    def run(self):
        print('Replaying recording ...')
        self.st = threading.Thread( target = self.run_thread )
        self.st.start()


    def close(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='filename', type=str, 
        help='File to be replayed')
    parser.add_argument('address', default='127.0.0.1', help='IP of server to send to')
    parser.add_argument('port', default=14040, help='Port number of server to send to')

    args = parser.parse_args()
    print(args)

    '''
    if len(sys.argv) < 2:
        print('Please supply filename')
    else:
        filename = sys.argv[1]
        sp = SaltoPlayer(filename)
        sp.run()
    '''
