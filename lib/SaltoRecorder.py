#! /usr/bin/python2

import threading, time, json, datetime
import OSC

# Setup

class SaltoRecorder():
    def __init__(self):
        self.bind_address = '0.0.0.0'
        self.bind_port = 14040

        self.is_receiving = False

        self.previous_time = 0

        self.should_record = False


    def print_interface(self):
        print('**********************')
        print('*   Salto Recorder   *')
        print('**********************')
        print('')
        print('Listening on port %d' % (self.bind_port,))
        print('Waiting ...')

    def open_file(self):
        datestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.writeFile = open('Recordings/' + datestr + '.txt', 'w')


    def run(self):
        self.print_interface()
        self.open_file()
        self.setup_server()


    def close(self):
        self.server.close()
        self.writeFile.close()
        print('Closing server')


    def setup_server(self):
        self.server = OSC.OSCServer((self.bind_address, self.bind_port))
        self.server.addMsgHandler('/salto2/sensor', self.recorder_callback)
        self.st = threading.Thread( target = self.server.serve_forever )
        self.st.start()


    def set_passthrough_client(self, client):
        self.passthrough_client = 

    def recorder_callback(self, addr, tags, data, client_address):
        if not self.is_receiving:
            print('Server is receiving data')
            print('Recording ... (Press Ctrl+C to stop)')
            self.is_receiving = True


        if self.is_receiving:
            if self.should_record:
                time_now = time.time()
                if self.previous_time == 0:
                    time_delta = 0
                else:
                    time_delta = time_now - self.previous_time

                to_dump = (time_delta, data)
                self.writeFile.write(json.dumps(to_dump) + '\n')
                self.previous_time = time_now

            if self.passthrough:
                # Send the data on though the pipes
                pass



if __name__ == '__main__':
    suit = SaltoRecorder()
    suit.run()

    try :
        while 1 :
            time.sleep(1)

    except KeyboardInterrupt :
        print("\nClosing Salto Recorder.")
        suit.close()
        print("Done")
