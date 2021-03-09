# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from JackMCS import MCS
from JackMCS.backend import jackserver
from JackMCS.util import *

import jack

from time import sleep
def test():
    midi_backend = jackserver()
    midi_backend.verbose = False
    mcs = MCS(midi_backend)
    mcs.verbose = True


    with mcs.backend.client:
        mcs.backend.inport.connect('system_midi:capture_2')
        mcs.backend.outport.connect('system_midi:playback_3')

        mcs.initialize()

        alpha_display = mcs.alphanumeric_display('Corndogs', 0, 0)
        alpha_display.send()

        timecode_display = mcs.timecode_display()
        timecode_display.send()

        timeA = mcs.backend.client.transport_query()[1]['frame']

        while True:
            print(mcs.backend.last_recv)

            sleep(0.005)

            timecode_display.timecode = frames_to_timecode(mcs.backend.client.transport_query()[1]['frame'], mcs.backend.client.samplerate)

            if mcs.backend.last_recv == [240, 21, 37, 66, 59, 1, 247] and mcs.backend.client.transport_state != jack.ROLLING:
                mcs.backend.client.transport_start()
            elif mcs.backend.last_recv == [240, 21, 37, 66, 58, 1, 247] and mcs.backend.client.transport_state == jack.ROLLING:
                mcs.backend.client.transport_stop()
                timecode_display.send()
            elif mcs.backend.client.transport_state == jack.ROLLING:
                timecode_display.send()

        input()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

#last msg received: [240, 21, 37, 69, 0, 126, 64, 247]
#last msg received: [240, 21, 37, 69, 1, 127, 64, 247]
#last msg received: [240, 21, 37, 69, 2, 127, 0, 247]

#last msg received: [240, 21, 37, 65, 0, 1, 247]
#last msg received: [240, 21, 37, 65, 1, 1, 247]