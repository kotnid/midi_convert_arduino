import os 
from mido import MidiFile , tick2second
from math import ceil


def get_tempo(tracks):
    for track in tracks:
        if track.type == 'set_tempo':
            return track.tempo
    return 500000   

if os.path.exists("test.txt"):
    os.remove("test.txt")

cv1 = MidiFile('badapple.mid' , clip=True)

pin = 9
tempo = get_tempo(cv1.tracks[1])
for track in cv1.tracks[1]:
    msg = str(track).split(' ')
    if msg[0] == "note_off":
        hz = str(ceil((400/32)*(2**((int(msg[2][5:])-9)/12))))
        time = tick2second(int(msg[4][5:]),cv1.ticks_per_beat , get_tempo(cv1.tracks[1]))*1000
        with open('test.txt', 'a') as f:
            f.write(f"tone({pin},{hz},{time})")
            f.write('\n')
            f.write(f"delay({time})")
            f.write('\n')
    elif msg[0] == "note_on":
        hz = str(ceil((400/32)*(2**((int(msg[2][5:])-9)/12))))
        time = tick2second(int(msg[4][5:]) ,cv1.ticks_per_beat*4 , get_tempo(cv1.tracks[1]))*1000

        if time != 0:
            with open('test.txt', 'a') as f:
                f.write(f"delay({time})")
                f.write('\n')

