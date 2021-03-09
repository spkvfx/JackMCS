_JLCOOPER = 0x15, 0x25
_REALTIME = 0x7F
_HANDSHAKE = [240, 21, 37, 3, 1, 43, 2, 0, 0, 0, 247]

class _SysEx(object):
    def __init__(self, backend, verbose):
        self.backend = backend
        self.verbose = verbose

        self._group = 0x00
        self._parameter = 0x00
        self._value = 0x00

        self._id = _REALTIME
        self._group = None
        self._parameter = None
        self._value = None

    @property
    def id(self):
        return self._id

    @property
    def group(self):
        return self._group

    @property
    def parameter(self):
        return self._parameter

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, v):
        self._value = v

    @property
    def message(self):
        msg = []
        contents = [0xF0, self.id, self.group, self.parameter, self.value, 0xF7]
        for item in contents:
            if item is not None:
                try:
                    msg.extend(item)
                except TypeError:
                    msg.append(item)

        return tuple(msg)


    def send(self, msg=None, channel=0):
        msg = msg if msg else self.message
        self.backend.send(msg, channel)


class Status(_SysEx):
    def __init__(self, backend, verbose):
        super().__init__(backend, verbose)
        self._value = [0xFE]

class Alpha(_SysEx):
    def __init__(self, backend, verbose, text='', line=0, position=0):
        super().__init__(backend, verbose)

        self._text = text
        self._line = line
        self._position = position

        self._id = _JLCOOPER
        self._group = 0x43

    @property
    def text(self):
        if self._text:
            return self._text
        else:
            self.clear()
            return self._text
    @text.setter
    def text(self, v):
        self._text = v

    @property
    def line(self):
        return self._line
    @line.setter
    def line(self, v):
        self._line = v

    @property
    def position(self):
        return self._position
    @position.setter
    def position(self, v):
        self._position = v

    @property
    def length(self):
        return len(self.text)

    @property
    def parameter(self):
        return [self.position + (64 * self.line)]

    @property
    def value(self):
        return [self.length] + [ord(_) for _ in self.text]

    def _clear(self, l, s, e):
        original_text = self.text
        original_line = self.line
        original_position = self.position

        self.line = l
        self.position = s
        self.text = [' ']*e
        self.send()

        self.position = original_position
        self.line = original_line
        self.text = original_text


    def clear(self):
        self._clear(self.line, self.position, self.length)

    def clear_line(self):
        self._clear(self.line, 0, 40)

    def clear_all(self):
        self._clear(0, 0, 80)

class MCS_Exit(_SysEx):
    def __init__(self, backend, verbose):
        super().__init__(backend, verbose)

        self._id = _JLCOOPER
        self._value = 0x02, 0x00, 0x00, 0x00, 0x00

class MCS_Reset(_SysEx):
    def __init__(self, backend, verbose):
        super().__init__(backend, verbose)

        self._id = _JLCOOPER
        self._value = 0x03

class MCS_Request(_SysEx):
    def __init__(self, backend, verbose):
        super().__init__(backend, verbose)

        self._id = _JLCOOPER
        self._value = 0x02, 0x02, 0x02, 0x00, 0x00

class Timecode_Display(_SysEx):
    def __init__(self, timecode, backend, verbose):
        super().__init__(backend, verbose)

        self._timecode = timecode
        self._id = _JLCOOPER
        self._parameter = [0x49]
        self._value = [0] * 8
        self.parse()

    @property
    def timecode(self):
        return self._timecode
    @timecode.setter
    def timecode(self, v):
        self._timecode = v
        self.parse()

    @property
    def mask(self):
        return [0b1111101,
                0b0101000,
                0b0110111,
                0b0101111,
                0b1101010,
                0b1001111,
                0b1011111,
                0b0101001,
                0b1111111,
                0b1101011]

    def parse(self):
        for index, item in enumerate(self.timecode[::-1]):
            if item == ' ':
                self._value[index] = 0
            else:
                self._value[index] = self.mask[int(item)]