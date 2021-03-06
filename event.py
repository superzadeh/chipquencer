import sequencer
import midi


class Event(object):
    def __init__(self, timestamp, function, params):
        # Using __dict__ directly to override __setattr__
        self.__dict__['timestamp'] = timestamp
        self.__dict__['function'] = function
        self.__dict__['params'] = params

    def type(self):
        return self.function.__name__

    def call(self, part):
        self.function(part, *self.params)

    def __repr__(self):
        return 'Event({}, {}, {})'.format(self.timestamp,
                                          self.type(),
                                          self.params)

    def __getattr__(self, name):
        # Checks if attribute is in self.params
        for i, n in enumerate(self.function.__code__.co_varnames[1:]):
            if n == name:
                return self.params[i]
        error = "'{}' event has no '{}' attribute".format(self.type(), name)
        raise AttributeError(error)

    def __setattr__(self, name, value):
        # Checks if attribute is in self.params
        for i, n in enumerate(self.function.__code__.co_varnames[1:]):
            if n == name:
                self.params[i] = value
                return

        object.__setattr__(self, name, value)

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __gt__(self, other):
        return self.timestamp > other.timestamp

    def __le__(self, other):
        return self.timestamp <= other.timestamp

    def __ge__(self, other):
        return self.timestamp >= other.timestamp

    def __ne__(self, other):
        return self.timestamp != other.timestamp


def note_off(part, note):
    midi.out.write_short(midi.NOTE_ON + part.channel, note, 0)


def note_on(part, note, velocity, length):
    midi.out.write_short(midi.NOTE_ON + part.channel, note, velocity)
    # Remove future note off events with same pitch
    part.future_events = [e for e in part.future_events
                          if not (e.type() == 'note_off' and
                                  e.note == note)]
    part.append_future(Event(sequencer.running_time + length,
                             note_off, [note]))


def cc(part, cc, data):
    midi.out.write_short(midi.CC + part.channel, cc, data)
