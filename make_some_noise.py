""" Module Description

This file contains classes that describe sound waves, instruments that play
these sounds and a function that plays multiple instruments simultaneously.

As discussed in the handout, you may not change any of the public behaviour
(attributes, methods) given in the starter code, but you can definitely add
new attributes, functions, classes and methods to complete your work here.

"""
from __future__ import annotations
import typing
import csv
import numpy
from helpers import play_sound, play_sounds, make_sine_wave_array


class SimpleWave:
    """A SimpleWave is a wave with amplitude of 1.

    === Attributes ===
    _frequency: frequency of the wave in Hz.
    _duration: duration of the wave in seconds.
    _amplitude: amplitude of the wave. Max amplitude for a simple wave is 1.
    """
    # Attribute types

    _frequency: int
    _duration: float
    _amplitude: float

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes an instance of class SimpleWave.
        NOTE: If amplitude is greater than 1, it is stored as 1"""

        self._frequency = frequency
        self._duration = duration

        if not amplitude > 1:
            self._amplitude = amplitude
        else:
            self._amplitude = 1

    def __eq__(self, other: SimpleWave) -> bool:
        """ Returns true if two SimpleWaves are equal. False otherwise"""

        return (self._frequency == other._frequency and
                self._amplitude == other._amplitude and
                self._duration == other._duration)

    def __ne__(self, other: SimpleWave) -> bool:
        """ Returns true if two SimpleWaves are not equal. False otherwise """

        return not self.__eq__(other)

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Returns a ComplexWave containing this SimpleWave and
        the waves of other """

        if isinstance(other, SimpleWave):
            return ComplexWave([self, other])
        else:
            return ComplexWave([self] + other.get_waves())

    def get_duration(self) -> float:
        """ Returns the duration of the SimpleWave """
        return self._duration

    def _get_amplitude(self) -> float:
        """ Returns the amplitude of the SimpleWave """
        return self._amplitude

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array of the SimpleWave using a helper function.
        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """
        array = make_sine_wave_array(round(self._frequency), self._duration)
        array1 = numpy.absolute(array)

        if len(array1) == 0:
            abs_max = 0
        else:
            abs_max = array1.max()

        if abs_max != 0:
            return array * (self._get_amplitude() / abs_max)
        else:
            return array * 0


class ComplexWave:
    """ A ComplexWave is a wave consisting of multiple SimpleWaves

    === Attributes ===
    _waves: A list of simple waves which make up the complex wave
    _amplitude: Max amplitude of the individual waves
    _duration: Duration of the ComplexWave
    """
    # Attribute Types
    _waves: typing.List[SimpleWave]
    _amplitude: float
    _duration: float

    def __init__(self, waves: typing.List[SimpleWave]) -> None:
        """ Initializes an instance of class ComplexWave
        NOTE: If amplitude of individual waves is greater than 1,
        it is stored as 1"""

        self._waves = waves
        duration, amplitude = 0, 0

        for wave in self._waves:
            d = wave.get_duration()
            a = abs(wave._get_amplitude())
            if d > duration:
                duration = d
            if a > amplitude:
                amplitude = a

        if amplitude > 1:
            self._amplitude = 1
        else:
            self._amplitude = amplitude

        self._duration = duration

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Returns a ComplexWave containing the waves of this ComplexWave and
        the waves of other wave"""

        if isinstance(other, SimpleWave):
            return ComplexWave(self.get_waves() + [other])
        else:
            return ComplexWave(self.get_waves() + other.get_waves())

    def complexity(self) -> int:
        """ Returns the complexity, which is equal to the number of SimpleWaves
        that make up of the ComplexWave """

        return len(self._waves)

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array of the ComplexWave which combines all
        the SimpleWaves that make up the ComplexWave

        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """

        sum_array = numpy.array([])
        for array in self._waves:
            array = array.play()
            if len(array) > len(sum_array):
                sum_array = array[:len(sum_array)] + sum_array
                sum_array = numpy.append(sum_array, array[len(sum_array):])
            elif len(array) < len(sum_array):
                array = sum_array[:len(array)] + array
                array = numpy.append(array, sum_array[len(array):])
                sum_array = array
            else:
                sum_array = sum_array + array

        array = numpy.absolute(sum_array)
        amplitude = self._get_amplitude()

        if len(array) == 0:
            abs_max = 0
        else:
            abs_max = array.max()

        if abs_max != 0:
            return sum_array * (amplitude / abs_max)
        else:
            return sum_array

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Returns the list of SimpleWaves that makes up this ComplexWave"""

        return self._waves

    def get_duration(self) -> float:
        """ Returns the duration of the SimpleWave from self._waves
        with the maximum duration"""

        return self._duration

    def _get_amplitude(self) -> float:
        """ Returns the amplitude of this ComplexWave """

        return self._amplitude

    def simplify(self) -> None:
        """ TODO: write a docstring for this method
            REMEMBER: this is not a required part of the assignment
        """
        pass  # TODO: finish this method body


class Note:
    """ A Note is a wave made up of different waves  played in order,
    one after another

    === Attributes ===
    _waves: A list of simple waves which make up the Note
    amplitude: Amplitude of the notes. Initially 1.
    _max_a: Max amplitude of the Note
    _duration: Total duration of note
    """
    # Attribute Types
    _waves: typing.List[ANYWAVE]
    amplitude: float
    _duration: float

    def __init__(self, waves: typing.List[ANYWAVE]) -> None:
        """ Initializes an instance of class Note
        NOTE: Amplitude is originally set to 1"""

        self._waves = waves
        self.amplitude = 1
        duration = 0

        for wave in self._waves:
            duration += wave.get_duration()

        self._duration = duration

    def __add__(self, other: Note) -> Note:
        """ Returns a Note in which this note is followed by the other.
        NOTE: Amplitude of result max amplitude between this and other Note"""

        note = Note(self._waves + other._waves)
        note.amplitude = max(self.amplitude, other.amplitude)

        return note

    def get_waves(self) -> typing.List[ANYWAVE]:
        """ Returns the list of Waves that makes up this Note"""

        return self._waves

    def get_duration(self) -> float:
        """ Returns the time in seconds that this Note will play """

        return self._duration

    def _get_amplitude(self) -> float:
        """ Returns the amplitude of this Note """

        return self.amplitude

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array in which each of the Note's component waves
        are played in order.

        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """

        n = numpy.array([])

        for wave in self._waves:
            n = numpy.append(n, wave.play())

        array = numpy.absolute(n)

        if len(array) == 0:
            abs_max = 0
        else:
            abs_max = array.max()

        if abs_max != 0:
            return n * (self._get_amplitude() / abs_max)
        else:
            return n


class SawtoothWave(ComplexWave):
    """ A  SawtoothWave is wave composed of an
    infinite number of components which follow a pattern.

    === Attributes ===
    _frequency: frequency of the wave in Hz.
    _duration: duration of the wave in seconds.
    _amplitude: amplitude of the wave.
    _waves: A list of simple waves which make up the SawtoothWave wave

    === Representation Invariants ==
    NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
    """
    # Attribute types

    _frequency: int
    _duration: float
    _amplitude: float
    _waves: typing.List[SimpleWave]

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes an instance of class SawtoothWave
        NOTE: If amplitude is greater than 1, it is stored as 1"""

        waves, components = [], 10

        if amplitude > 1:
            amplitude = 1

        for component in range(1, components + 1):
            waves.append(SimpleWave(((2 * component) - 1) * frequency,
                                    duration,
                                    amplitude / ((2 * component) - 1)))

        ComplexWave.__init__(self, waves)
        self._frequency = frequency
        self._amplitude = amplitude


class SquareWave(ComplexWave):
    """ A  SquareWave is wave composed of an
    infinite number of components which follow a pattern.

    === Attributes ===
    _frequency: frequency of the wave in Hz.
    _duration: duration of the wave in seconds.
    _amplitude: amplitude of the wave.
    _waves: A list of simple waves which make up the SquareWave wave

    === Representation Invariants ==
    NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
    """
    # Attribute types

    _frequency: int
    _duration: float
    _amplitude: float
    _waves: typing.List[SimpleWave]

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """Initializes an instance of class SquareWave
        NOTE: If amplitude is greater than 1, it is stored as 1"""

        waves, components = [], 10

        if amplitude > 1:
            amplitude = 1

        for component in range(1, components + 1):
            waves.append(SimpleWave(component * frequency,
                                    duration,
                                    amplitude / component))

        ComplexWave.__init__(self, waves)
        self._frequency = frequency
        self._amplitude = amplitude


class Rest(ComplexWave):
    """ A Rest is a wave which models a wave in with no sound

    === Attributes ===
    _frequency: frequency of the wave in Hz.
    _duration: duration of the wave in seconds.
    _complexity: the complexity of rest. 1 by default.

    === Representation Invariants ==
    Amplitude and frequency of Rest class is always 0
    """
    # Attribute Types
    _frequency: int
    _duration: float
    _complexity: int

    def __init__(self, duration: float) -> None:
        """Initializes an instance of class Rest """

        ComplexWave.__init__(self, [SimpleWave(0, duration, 0)])
        self._frequency = 0

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Adds Rest with any other wave"""

        if isinstance(other, SimpleWave):
            return ComplexWave([self, other])
        else:
            return ComplexWave([self] + other.get_waves())

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array modeling this rest period """

        return make_sine_wave_array(round(self._frequency), self._duration) * 0


class StutterNote(Note):
    """ A StutterNote is a note which alternates between Rest and SawtoothWave

    === Attributes ===
    _waves: A list of simple waves which make up the StutterNote
    amplitude: Amplitude of the StutterNote.
    _duration: Total duration of StutterNote
    _frequency: Initial frequency of StutterNote

    === Representation Invariants ==
    NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
     """

    _waves: typing.List[ANYWAVE]
    amplitude: float
    _duration: float
    _frequency: int

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes an instance of class StutterNote """

        cur, i, waves = 0, 0, []

        while (0.025 + cur) <= duration:
            if i % 2 == 1:
                waves.append(SawtoothWave(frequency, 0.025, amplitude))
            else:
                waves.append(Rest(0.025))

            i += 1
            cur += 0.025

        if cur < duration and i % 2 == 1 and duration - cur > 0.0001:
            waves.append(SawtoothWave(frequency, duration - cur, amplitude))
        elif cur < duration and i % 2 == 0 and duration - cur > 0.0001:
            waves.append(Rest(duration - cur))

        Note.__init__(self, waves)
        self._frequency = frequency
        self.amplitude = amplitude


class Baliset:
    """ A Baliset is an instrument

    === Attributes ===
    _frequency: fundamental frequency of the instrument in Hz.
    _duration: duration of the wave in seconds.
    _waves: A list of SawtoothWave which make up the sound of this instrument
    _amplitude: Amplitude of the instrument
    _next_notes: Stores the next notes for the instrument. Originally empty
     """

    _frequency: int
    _duration: float
    _waves: typing.List[typing.Union[SawtoothWave, Rest]]
    _amplitude: float
    _next_notes: typing.List[typing.Tuple[str, float, float]]

    def __init__(self) -> None:
        """ Initializes an instance of class Baliset
        NOTE: self._amplitude is originally set to 1"""

        self._duration = 0
        self._frequency = 196
        self._waves = []
        self._amplitude = 1
        self._next_notes = []

    def get_duration(self) -> float:
        """ Duration of this Baliset """

        d = 0
        for wave in self._waves:
            d += wave.get_duration()
        self._duration = d

        return d

    def _get_amplitude(self) -> float:
        """ Max amplitude of this Baliset """

        a = 0
        for wave in self._waves:
            w_a = wave._get_amplitude()
            if w_a > a:
                a = w_a
        self._amplitude = a

        return a

    def _get_waves(self) -> typing.List[SimpleWave]:
        """Returns all the Simple waves that make up instrument"""

        lst = []
        for wave in self._waves:
            lst.extend(wave.get_waves())
        return lst

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ Stores the next notes for this Baliset.
        NOTE: If duration of notes is less than 1, it only stores up to the
        given duration and doesn't add rest. If duration is greater than 1, it
        will partially store the wave that makes it have duration of greater
        than 1
        """

        self._waves, i, d, duration, n_i, n_f = [], 0, 0, None, note_info, 0

        if len(n_i) >= 1:
            duration = n_i[i][2]

        while duration and i < len(n_i) and d + duration <= 1:
            ratio = list(n_i[i][0].strip().split(':'))
            ratio[0], ratio[1] = ratio[0].strip(), ratio[1].strip()

            if int(ratio[0]) != 0 and int(ratio[1]) != 0:
                n_f = int(int(ratio[0]) / int(ratio[1]) * self._frequency)
                self._waves.append(SawtoothWave(n_f, n_i[i][2], n_i[i][1]))
            else:
                self._waves.append(SawtoothWave(0, n_i[i][2], 0))

            d += duration
            i += 1
            if i < len(n_i):
                duration = n_i[i][2]

        if not duration:
            self._waves.append(Rest(1))

        elif d < 1 and i < len(n_i):
            a, d = n_i[i][1], 1 - d
            self._waves.append(SawtoothWave(n_f, d, a))

        self._duration = self.get_duration()
        self._next_notes = note_info

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array in which each of the Note's component waves
        are played in order.

        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """

        n = numpy.array([])

        for wave in self._waves:
            n = numpy.append(n, wave.play())

        array = numpy.absolute(n)

        if len(array) == 0:
            abs_max = 0
        else:
            abs_max = array.max()

        if abs_max != 0:
            return n * (self._get_amplitude() / abs_max)
        else:
            return n


class Holophonor:
    """ A Holophonor is an instrument

    === Attributes ===
    _frequency: fundamental frequency of the instrument in Hz.
    _duration: duration of the wave in seconds.
    _waves: A list of StutterNote which make up the sound of this instrument
    _amplitude: Amplitude of the instrument
    _next_notes: Stores the next notes for the instrument. Originally empty
    """

    _frequency: int
    _duration: float
    _waves: typing.List[typing.Union[StutterNote, Rest]]
    _amplitude: float
    _next_notes: typing.List[typing.Tuple[str, float, float]]

    def __init__(self) -> None:
        """ Initializes an instance of class Holophonor """
        self._duration = 0
        self._frequency = 65
        self._waves = []
        self._amplitude = 1
        self._next_notes = []

    def get_duration(self) -> float:
        """ Duration of this Baliset """

        d = 0
        for wave in self._waves:
            d += wave.get_duration()
        self._duration = d

        return d

    def _get_amplitude(self) -> float:
        """ Max amplitude of this Holophonor """

        a = 0
        for wave in self._waves:
            w_a = wave._get_amplitude()
            if w_a > a:
                a = w_a
        self._amplitude = a

        return a

    def _get_waves(self) -> typing.List[SimpleWave]:
        """Returns all the Simple waves that make up self._waves"""
        lst = []
        for wave in self._waves:
            lst.extend(wave.get_waves())
        return lst

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ Stores the next notes for this Holophonor
        NOTE: If duration of notes is less than 1, it only stores up to the
        given duration and doesn't add rest. If duration is greater than 1, it
        will partially store the wave that makes it have duration of greater
        than 1"""

        self._waves, i, d, duration, n_i, n_f = [], 0, 0, None, note_info, 0

        if len( n_i) >= 1:
            duration = n_i[i][2]

        while duration and i < len(n_i) and d + duration <= 1:
            ratio = list(n_i[i][0].strip().split(':'))
            ratio[0], ratio[1] = ratio[0].strip(), ratio[1].strip()

            if int(ratio[0]) != 0 and int(ratio[1]) != 0:
                n_f = int(int(ratio[0]) / int(ratio[1]) * self._frequency)
                self._waves.append(StutterNote(n_f, n_i[i][2], n_i[i][1]))
            else:
                self._waves.append(StutterNote(0, n_i[i][2], 0))

            d += duration
            i += 1
            if i < len(n_i):
                duration = n_i[i][2]

        if not duration:
            self._waves.append(Rest(1))

        elif d < 1 and i < len(n_i):
            a, d = n_i[i][1], 1 - d
            self._waves.append(StutterNote(n_f, d, a))

        self._duration = self.get_duration()
        self._next_notes = note_info

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array in which each of the Note's component waves
        are played in order.

        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """

        n = numpy.array([])

        for wave in self._waves:
            n = numpy.append(n, wave.play())

        array = numpy.absolute(n)

        if len(array) == 0:
            abs_max = 0
        else:
            abs_max = array.max()

        if abs_max != 0:
            return n * (self._get_amplitude() / abs_max)
        else:
            return n


class Gaffophone:
    """ A Gaffophone is an instrument

    === Attributes ===
    _frequency: fundamental frequency of the instrument in Hz.
    _duration: duration of the wave in seconds.
    _waves: A list of SquareWave which make up the sound of this instrument
    _amplitude: Amplitude of the instrument
    _next_notes: Stores the next notes for the instrument. Originally empty
    """

    _frequency: int
    _duration: float
    _waves: typing.List[typing.Union[SquareWave, Rest]]
    _amplitude: float
    _next_notes: typing.Tuple[str, float, float]

    def __init__(self) -> None:
        """ Initializes an instance of class Gaffophone """

        self._duration = 0
        self._frequency = 131
        self._waves = []
        self._amplitude = 1
        self._next_notes = []

    def get_duration(self) -> float:
        """ Duration of this Baliset """

        d = 0
        for wave in self._waves:
            d += wave.get_duration()
        self._duration = d

        return d

    def _get_amplitude(self) -> float:
        """ Max amplitude of this Holophonor """

        a = 0
        for wave in self._waves:
            w_a = wave._get_amplitude()
            if w_a > a:
                a = w_a
        self._amplitude = a

        return a

    def _get_waves(self) -> typing.List[SimpleWave]:
        """Returns all the Simple waves that make up self._waves"""
        lst = []
        for wave in self._waves:
            lst.extend(wave.get_waves())
        return lst

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ Stores the next notes for this Gaffophone.
        NOTE: If duration of notes is less than 1, it only stores up to the
        given duration and doesn't add rest. If duration is greater than 1, it
        will partially store the wave that makes it have duration of greater
        than 1"""

        self._waves, i, d, duration, n_i, n_f = [], 0, 0, None, note_info, 0

        if len(n_i) >= 1:
            duration = n_i[i][2]

        while duration and i < len(n_i) and d + duration <= 1:
            ratio = list(n_i[i][0].strip().split(':'))
            ratio[0], ratio[1] = ratio[0].strip(), ratio[1].strip()

            if int(ratio[0]) != 0 and int(ratio[1]) != 0:
                n_f = int(int(ratio[0]) / int(ratio[1]) * self._frequency)
                self._waves.append(SquareWave(n_f, n_i[i][2], n_i[i][1]) +
                                   SquareWave(int(n_f * (3 / 2)), n_i[i][2],
                                              n_i[i][1]))
            else:
                self._waves.append(SquareWave(0, n_i[i][2], 0))

            d += duration
            i += 1
            if i < len(n_i):
                duration = n_i[i][2]

        if not duration:
            self._waves.append(Rest(1))

        elif d < 1 and i < len(n_i):
            a, d = n_i[i][1], 1 - d
            self._waves.append(SquareWave(n_f, d, a) +
                               SquareWave(int(n_f * (3 / 2)), d, a))

        self._duration = self.get_duration()
        self._next_notes = note_info

    def play(self) -> numpy.ndarray:
        """ Returns a numpy array in which each of the Note's component waves
        are played in order.

        NOTE: Amplitude of the numpy array is scaled down to
        self._get_amplitude() value in order to preserve original amplitude.
        """

        n = numpy.array([])

        for wave in self._waves:
            n = numpy.append(n, wave.play())

        array = numpy.absolute(n)

        if len(array) == 0:
            abs_max = 0
        else:
            abs_max = array.max()

        if abs_max != 0:
            return n * (self._get_amplitude() / abs_max)
        else:
            return n


def _make_vertical_lst(o_lst: list, beat: float, first: list) -> list:
    """ Returns vertical list """

    n_lst, i, v = [], 0, 0
    while i < len(first):
        temp_lst = []
        while v < len(o_lst):
            ele = o_lst[v][i].replace(' ', '').lower().strip()
            if 'rest' in ele:
                temp_lst.append([("1:1", 0.0, round(float(ele[5:]) * beat, 5))])
            elif len(ele) != 0:
                semi_c = [e for e in range(len(ele)) if ele[e] == ':']
                f = ele[:semi_c[1]]
                a = round(float(ele[semi_c[1] + 1: semi_c[2]]), 5)
                d = round(float(ele[semi_c[2] + 1:]) * beat, 5)
                temp_lst.append([(f, a, d)])
            v += 1
        n_lst.append(temp_lst)
        v = 0
        i += 1

    return n_lst


def _less_than_1(v_lst: list, v: int, d: float) -> None:
    """ Case less than 1 duration """

    t = v + 1

    while d < 1 and t < len(v_lst):
        n_d = v_lst[t][0][2]
        if d + n_d <= 1:
            d += n_d
            d = round(d, 5)
            v_lst[v].extend(v_lst.pop(t))
        else:
            f_t, a_t = v_lst[t][0][0], v_lst[t][0][1]
            v_lst[v].append((f_t, a_t, round(float(1.0 - d), 5)))
            v_lst[t][0] = (f_t, a_t, round(float(d + n_d - 1), 5))
            d = 1.0


def _greater_than_1(v_lst: list, v: int, d: float) -> None:
    """ Case greater than 1 duration """

    f_v, a_v, t = v_lst[v][0][0], v_lst[v][0][1], v + 1

    while d > 1:
        if d - 1 < 1:
            v_lst[v][-1] = (f_v, a_v, 1.0)
            v_lst.insert(t, [(f_v, a_v, round(float(d - 1.0), 5))])
            d -= 1.0
            d = round(d, 5)
        elif d - 1.0 > 1:
            v_lst[v][-1] = (f_v, a_v, round(float(d - 1.0), 5))
            v_lst.insert(t, [(f_v, a_v, 1.0)])
            d -= 1.0
            d = round(d, 5)
        else:
            v_lst[v][-1] = (f_v, a_v, 1.0)
            v_lst.insert(t, v_lst[v])
            d = 1.0


def _playables_list(v_lst: list, instrument: str) -> list:
    """ Returns a playable list """

    if instrument == 'baliset':
        lst_note = []
        for note in v_lst:
            b = Baliset()
            b.next_notes(note)
            lst_note.append(b)
    elif instrument == 'holophonor':
        lst_note = []
        for note in v_lst:
            h = Holophonor()
            h.next_notes(note)
            lst_note.append(h)
    else:
        lst_note = []
        for note in v_lst:
            g = Gaffophone()
            g.next_notes(note)
            lst_note.append(g)

    return lst_note


def _process_song(song_file: str, beat: float) -> tuple:
    """ Processes the song and returns a tuple containing a playable list,
     max_len of list and len instruments"""

    with open(song_file) as song:
        reader = csv.reader(song, skipinitialspace=True)
        first = song.readline().split(',')
        first = [x.strip().lower().replace(' ', '') for x in first]
        o_lst = ([x for x in reader if x])
    song.close()

    v_lst = _make_vertical_lst(o_lst, beat, first)

    for instrument in range(len(first)):
        v = 0
        while v < len(v_lst[instrument]):
            d = v_lst[instrument][v][0][2]
            if d < 1 and v == len(v_lst[instrument]) - 1:
                v_lst[instrument][v].append(('1:1', 0.0,
                                             round(float(1.0 - d), 5)))
            elif d < 1:
                _less_than_1(v_lst[instrument], v, d)
            elif d > 1:
                _greater_than_1(v_lst[instrument], v, d)
            v += 1

    max_len = max([len(x) for x in v_lst])

    for instr_f in v_lst:
        while len(instr_f) < max_len:
            instr_f.append([('1:1', 0, 1)])

    for instr_i in range(len(first)):
        v_lst[instr_i] = _playables_list(v_lst[instr_i], first[instr_i])

    return max_len, first, v_lst


def play_song(song_file: str, beat: float) -> None:
    """ Plays the given song pieces at a given beat.
    NOTE: The duration of the passed ins song_file is rounded to 5 decimal
    places"""

    max_len, first, v_lst = _process_song(song_file, beat)
    lst_notes = []
    for column in range(max_len):
        lst_note = []
        for instr_i in range(len(first)):
            lst_note.append(v_lst[instr_i][column])
        lst_notes.append(lst_note)

    for note in lst_notes:
        play_sounds(note)

# This is a custom type for type annotations that
# refers to any of the following classes (do not
# change this code)


ANYWAVE = typing.TypeVar('ANYWAVE',
                         SimpleWave,
                         ComplexWave,
                         SawtoothWave,
                         SquareWave,
                         Rest)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['helpers',
                                                  'typing',
                                                  'csv',
                                                  'numpy'],
                                'disable':  ['E9997', 'E9998', 'W0611']})
