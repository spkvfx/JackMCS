from time import sleep
from .sysex import *

class MCS(object):
    def __init__(self, midi_backend, verbose=False):
        self._verbose = verbose
        self._backend = midi_backend

    #mutable properties
    @property
    def verbose(self):
        return self._verbose
    @verbose.setter
    def verbose(self, v):
        if isinstance(v, bool):
            self._verbose = v
        else:
            raise TypeError('Expected {0} but got {1}'.format(type(bool()), type(v)))

    @property
    def backend(self):
        return self._backend

    def initialize(self):
        _HANDSHAKE = [240, 21, 37, 3, 1, 43, 2, 0, 0, 0, 247]
        mcs_exit = self.mcs_exit()
        mcs_exit.send()
        sleep(0.25)
        reset = self.mcs_reset()
        reset.send()
        sleep(0.25)
        request = self.mcs_request()
        request.send()
        i=0
        while True:
            if self.backend.last_recv == _HANDSHAKE:
                break
            else:
                if self.verbose:
                    print('MCS Did not respond after {} out of {} attempts'.format(i, 100))

                mcs_exit.send()
                sleep(0.25)
                reset.send()
                sleep(0.25)
                request.send()
                sleep(0.25)
                i += 1

                if i > 100:
                    print('MCS Did not Respond after 100 attempts.')
                    exit()

        print('MCS was Initialized Successfully')
        sleep(1)

        return True

    def status(self):
        return Status(self.backend, self.verbose)

    def alphanumeric_display(self, text='', line=0, position=0):
        return Alpha(self.backend, self.verbose, text, line, position)

    def mcs_exit(self):
        return MCS_Exit(self.backend, self.verbose)

    def mcs_reset(self):
        return MCS_Reset(self.backend, self.verbose)

    def mcs_request(self):
        return MCS_Request(self.backend, self.verbose)

    def timecode_display(self, timecode = ''):
        return Timecode_Display(timecode, self.backend, self.verbose)