#!/usr/bin/python2
from gi.repository import Gtk

from SaltoRecorder import SaltoRecorder

from SaltoPlayer import SaltoPlayer


class MyWindow(Gtk.Window):
    def __init__(self):
        self.saltoRecorder = SaltoRecorder()

        self.is_recording = False
        self.is_playing = False

        Gtk.Window.__init__(self, title="SaltoTools Replay")

        self.set_border_width(20)

        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        self.recordImage = Gtk.Image()
        self.recordImage.set_from_file('Assets/record.png')

        self.playImage = Gtk.Image()
        self.playImage.set_from_file('Assets/play.png')

        self.stopImage = Gtk.Image()
        self.stopImage.set_from_file('Assets/stop.png')

        self.recordButton = Gtk.Button(image=self.recordImage)
        self.recordButton.connect("clicked", self.record)
        self.recordButton.show()
        self.box.pack_start(self.recordButton, True, True, 0)

        self.playButton = Gtk.Button(label="Play")
        self.playButton = Gtk.Button(image=self.playImage)
        self.playButton.connect("clicked", self.play)
        self.box.pack_start(self.playButton, True, True, 0)


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

            self.saltoPlayer = SaltoPlayer(filename, '192.168.0.10', 14040)
            self.saltoPlayer.run()

        else : 
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

        return filename


win = MyWindow()
win.connect("delete-event", win.quit)
win.show_all()
Gtk.main()
