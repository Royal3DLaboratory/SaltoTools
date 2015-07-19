#!/usr/bin/python2
from gi.repository import Gtk

from lib.SaltoRecorder import SaltoRecorder

from lib.SaltoPlayer import SaltoPlayer

from time import sleep


class MyWindow(Gtk.Window):
    def __init__(self):
        self.saltoRecorder = SaltoRecorder()

        self.is_recording = False
        self.is_playing = False

        Gtk.Window.__init__(self, title="SaltoTools Replay")
        self.set_resizable(False)

        self.set_border_width(20)

        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        self.table = Gtk.Table(3, 2, True)
        self.table.set_row_spacings(20)
        self.table.set_col_spacings(20)
        #self.add(self.table)

        self.box.pack_start(self.table, True, True, 0)

        self.countdown_label = Gtk.Label(label=':P')
        self.countdown_label.set_use_markup(True)
        self.countdown_label.set_markup('<span size="38000"> </span>')

        self.recordImage = Gtk.Image()
        self.recordImage.set_from_file('lib/Assets/record.png')

        self.playImage = Gtk.Image()
        self.playImage.set_from_file('lib/Assets/play.png')

        self.stopImage = Gtk.Image()
        self.stopImage.set_from_file('lib/Assets/stop.png')

        self.recordButton = Gtk.Button(image=self.recordImage)
        self.recordButton.connect("clicked", self.record)
        self.recordButton.set_size_request(170, 50)

        self.playButton = Gtk.Button(image=self.playImage)
        self.playButton.connect("clicked", self.play)
        self.playButton.set_size_request(170, 50)

        self.actionButton = Gtk.Button(label='Action!')
        self.actionButton.connect('clicked', self.action)
        self.actionButton.set_size_request(170, 50)

        self.check_passthrough = Gtk.CheckButton("Passthrough")
        self.check_passthrough.set_active(True)

        self.table.attach(self.countdown_label, 0, 2, 0, 1)
        self.table.attach(self.recordButton, 0, 1, 1, 2)
        self.table.attach(self.playButton, 1, 2, 1, 2)
        self.table.attach(self.check_passthrough, 0, 1, 2, 3)
        self.table.attach(self.actionButton, 1, 2, 2, 3)

        '''
        self.grid.add(self.countdown_label)
        self.grid.attach_next_to(self.recordButton, self.countdown_label, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.playButton, self.recordButton, Gtk.PositionType.RIGHT, 1, 2)
        self.grid.attach_next_to(self.check_passthrough, self.recordButton, Gtk.PositionType.BOTTOM, 1, 2)
        self.grid.attach_next_to(self.actionButton, self.playButton, Gtk.PositionType.BOTTOM, 1, 2)
        '''


    def countdown(self, time, callback=None, label=None, label_color=None):
        for sec in range(time*10):
            remaining = time - (sec / 10)

            sleep(0.1)
            self.countdown_label.set_markup('<span size="38000">' + str(remaining) + '</span>')
            while Gtk.events_pending():
                Gtk.main_iteration()

        if not label:
            label = 'Active'

        if not label_color:
            label_color = '#2a0'

        self.countdown_label.set_markup('<span size="38000" color="' + label_color + '">' + label + '</span>')

        if callback:
            callback()

        return True


    def action(self, widget):
        self.countdown(5, None)
        # Make a server and a client and pass the data through!
        self.action_client = SaltoPlayer('127.0.0.1', 14050)


    def record(self, widget):
        if not self.is_recording:
            self.recordButton.set_image(self.stopImage)
            self.saltoRecorder.run()
            self.is_recording = True
        else:
            self.recordButton.set_image(self.recordImage)
            self.saltoRecorder.close()
            self.is_recording = False


    def play(self, widget):
        if not self.is_playing:
            self.playButton.set_image(self.stopImage)
            self.is_playing = True

            filename = self.choose_file()

            self.saltoPlayer = SaltoPlayer('127.0.0.1', 14050)
            self.saltoPlayer.run(filename, self.rundoneCallback)

        else : 
            self.saltoPlayer.close()
            self.is_playing = False
            self.playButton.set_image(self.playImage)


    def rundoneCallback(self):
        self.saltoPlayer.close()
        self.is_playing = False
        self.playButton.set_image(self.playImage)


    def quit(self, widget, stuff):
        if self.is_recording:
            self.saltoRecorder.close()

        if self.is_playing:
            self.saltoPlayer.close()
        Gtk.main_quit()

    def choose_file(self):
        chooser_dialog = Gtk.FileChooserDialog(title="Open file"
        ,action=Gtk.FileChooserAction.OPEN
        ,buttons=["Open", Gtk.ResponseType.OK, "Cancel", Gtk.ResponseType.CANCEL]
        )
        chooser_dialog.set_modal(True)
        tfilter = Gtk.FileFilter()
        tfilter.add_mime_type('text/plain')
        tfilter.add_pattern('*.txt')
        tfilter.set_name('Salto Recordings')
        chooser_dialog.add_filter(tfilter)
        response = chooser_dialog.run()
        filename = chooser_dialog.get_filename()
        chooser_dialog.hide() #destroy()

        while Gtk.events_pending():
            Gtk.main_iteration()

        return filename.decode('utf8')


win = MyWindow()
win.connect("delete-event", win.quit)
win.show_all()
Gtk.main()
