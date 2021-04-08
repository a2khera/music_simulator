from make_some_noise import *
from helpers import *


def play_song_csv():
    b1, b2 = Baliset(), Baliset()
    h1, h2 = Holophonor(), Holophonor()
    g1, g2 = Gaffophone(), Gaffophone()

    b1.next_notes([("5:4", 1, 0.5), ("1:1", 0, 0.5)])
    h1.next_notes([("3:2", 0.5, 0.5), ("3:1", 0.5, 0.5)])
    g1.next_notes([("1:1", 0, 1.0)])

    b2.next_notes([("1:1", 0, 1.0)])
    h2.next_notes([("1:1", 0, 1.0)])
    g2.next_notes([("1:1", 0, 0.5), ("1:1", 1, 0.5)])

    play_sounds([b1, h1, g1])
    play_sounds([b2, h2, g2])


def play_swan_lake_csv():
    b1, b2, b3, b4 = Baliset(), Baliset(), Baliset(), Baliset()
    h1, h2, h3, h4  = Holophonor(), Holophonor(), Holophonor(), Holophonor()
    g1, g2, g3, g4 = Gaffophone(), Gaffophone(), Gaffophone(), Gaffophone()

    b1.next_notes([("277:98", 0.5, 0.8), ("185:98", 0.5, 0.2)])
    h1.next_notes([("1:1", 0, 1)])
    g1.next_notes([("93:131", 0.9, 0.8), ("185:131", 0.9, 0.2)])

    b2.next_notes([("415:196", 0.5, 0.2), ("110:49", 0.5, 0.2),
                   ("247:98", 0.5, 0.2), ("277:98", 0.5, 0.4)])
    h2.next_notes([("1:1", 0, 1)])
    g2.next_notes([("185:131", 0.9, 0.6), ("93:131", 0.9, 0.4)])

    b3.next_notes([("277:98", 0.5, 0.2), ("110:49", 0.5, 0.2),
                   ("277:98", 0.5, 0.6)])
    h3.next_notes([("1:1", 0, 1)])
    g3.next_notes([("93:131", 0.9, 0.4), ("1:1", 0, 0.6)])

    b4.next_notes([("110:49", 0.5, 0.2), ("277:98", 0.5, 0.6),
                   ("185:98", 0.5, 0.2)])
    h4.next_notes([("1:1", 0, 1)])
    g4.next_notes([("1:1", 0, 0.2), ("93:131", 0.2, 0.8)])

    play_sounds([b1, h1, g1])
    play_sounds([b2, h2, g2])
    play_sounds([b3, h3, g3])
    play_sounds([b4, h4, g4])


def play_spanish_violin_csv():
    b1, b2, b3, b4 = Baliset(), Baliset(), Baliset(), Baliset()
    h1, h2, h3, h4  = Holophonor(), Holophonor(), Holophonor(), Holophonor()
    g1, g2, g3, g4 = Gaffophone(), Gaffophone(), Gaffophone(), Gaffophone()

    b1.next_notes([("277:98", 0.5, 0.8), ("185:98", 0.5, 0.2)])
    h1.next_notes([("1:1", 0, 1)])
    g1.next_notes([("93:131", 0.9, 0.8), ("185:131", 0.9, 0.2)])

    b2.next_notes([("415:196", 0.5, 0.2), ("110:49", 0.5, 0.2),
                   ("247:98", 0.5, 0.2), ("277:98", 0.5, 0.4)])
    h2.next_notes([("1:1", 0, 1)])
    g2.next_notes([("185:131", 0.9, 0.6), ("93:131", 0.9, 0.4)])

    b3.next_notes([("277:98", 0.5, 0.2), ("110:49", 0.5, 0.2),
                   ("277:98", 0.5, 0.6)])
    h3.next_notes([("1:1", 0, 1)])
    g3.next_notes([("93:131", 0.9, 0.4), ("1:1", 0, 0.6)])

    b4.next_notes([("110:49", 0.5, 0.2), ("277:98", 0.5, 0.6),
                   ("185:98", 0.5, 0.2)])
    h4.next_notes([("1:1", 0, 1)])
    g4.next_notes([("1:1", 0, 0.2), ("93:131", 0.2, 0.8)])

    play_sounds([b1, h1, g1])
    play_sounds([b2, h2, g2])
    play_sounds([b3, h3, g3])
    play_sounds([b4, h4, g4])


def test_sounds():
    play_sound(SimpleWave(440, 1, 1))
    play_sound(Rest(1))
    play_sound(SimpleWave(550, 1, 1))
    play_sound(Rest(1))
    c1 = ComplexWave([SimpleWave(440, 1, 1), SimpleWave(550, 1, 1)])
    c2 = ComplexWave([SimpleWave(100, 1, 1), SimpleWave(200, 1, 1)])
    play_sound(c1)
    play_sound(Rest(1))
    play_sound(c2)
    play_sound(Rest(1))
    play_sound(Note([c1, c2]))
    play_sound(Rest(1))
    play_sound(SquareWave(440, 1, 1))
    play_sound(Rest(1))
    play_sound(SawtoothWave(440, 1, 1))
    play_song('song.csv', 0.5)
    play_song('swan_lake.csv', 0.2)
    play_song('spanish_violin.csv', 0.2)
    play_song('base_songs\line_1_d_equal_1.csv', 1.0)
    play_song('base_songs\line_1_d_greater_1.csv', 1.0)
    play_song('base_songs\line_1_d_less_1.csv', 1.0)
    play_song('base_songs\line_2_d_equal_1.csv', 1.0)
    play_song('base_songs\line_2_d_greater_1.csv', 1.0)
    play_song('base_songs\line_2_d_less_1.csv', 1.0)


if __name__ == '__main__':
    # play_song_csv()
    # play_swan_lake_csv()
    # play_spanish_violin_csv()
    test_sounds()

