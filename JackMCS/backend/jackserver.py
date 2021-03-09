import jack
from time import sleep
import binascii

from JackMCS.sysex import *

class jackserver(object):
    def __init__(self, client_name='JackMCS', inport_name='input', outport_name='output', verbose=False):
        self.verbose = verbose

        self.verbosity('Starting JackMCS client as {}...'.format(client_name))
        self.client_name = client_name
        self.client = jack.Client(client_name)

        self.verbosity('Registering ports...')
        self.outport_name = outport_name
        self.outport = self.client.midi_outports.register(outport_name)

        self.inport_name = inport_name
        self.inport = self.client.midi_inports.register(inport_name)

        self._last_recv = None
        self._realtime_recv = None

        self._msg = None
        self._ch = 0

        self.time_code_display = Timecode_Display('', self, self.verbose)

        self.verbosity('Activating JackMCS...')
        @self.client.set_process_callback
        def process(frames):
            self.outport.clear_buffer()
            a = self.client.frame_time
            if self.inport.incoming_midi_events():
                self.rx()
            if self._msg:
                self.tx()


        self.verbosity('Successfully started JackMCS.')

    @property
    def last_recv(self):
        recv = self._last_recv
        if recv:
            self.verbosity('last msg received: {}'.format(recv))
        return recv

    @property
    def realtime_recv(self):
        recv = self._realtime_recv
        if recv:
            self.verbosity('msg received: {}'.format(recv))
        self._realtime_recv = None
        return recv

    def tx(self,):
        self.outport.write_midi_event(self._ch, self._msg)
        self.verbosity('msg sent: {}, ch.{}'.format([hex(_) for _ in self._msg], self._ch))
        self._msg = None
        self._ch = 0

    def rx(self):
        for offset, data in self.inport.incoming_midi_events():
            if data:
                line = binascii.hexlify(data).decode()
                self._last_recv = [int('0x'+(line[i:i+2]), 16) for i in range(0, len(line), 2)]
                self._realtime_recv = self.last_recv

    def send(self, msg, ch):
        self._ch = ch
        self._msg = msg

    def verbosity(self, status):
        if not self.verbose:
            return False
        else:
            print(status)