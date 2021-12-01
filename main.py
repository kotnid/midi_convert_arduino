from mido import MidiFile , tick2second
from time import sleep 
from os import path , remove 
from math import ceil

if path.exists("test2.txt"):
    remove("test2.txt")

if path.exists("test.txt"):
    remove("test.txt")

cv1 = MidiFile('song.mid',clip=True)

number = 0
for track in cv1.tracks:
    print(f"track {number} : {track}")    
    number += 1

ans = input(f"track (0~{number}) to convert : ")

while int(ans) > number  :
    print("\n wrong input ! pls re enter \n")
    sleep(3)
    ans = input(f"track (0~{number}) to convert : ")

def get_tempo():
    for track in cv1.tracks[0]:
        if track.type == 'set_tempo':
            return track.tempo
    return 500000   


pin = input("pin : ")
tempo = get_tempo()

for track in cv1.tracks[int(ans)]:
    msg = str(track).split(' ')
    with open('test2.txt','a') as f:
        f.write(str(msg))
        f.write('\n')
    if msg[0] == "note_off":
        hz = str(ceil((400/32)*(2**((int(msg[2][5:])-9)/12))))
        time = tick2second(int(msg[4][5:]),cv1.ticks_per_beat , tempo)*1000
        with open('test.txt', 'a') as f:
            f.write(f"tone({pin},{hz},{time});")
            f.write('\n')
            f.write(f"delay({time});")
            f.write('\n')
    elif msg[0] == "note_on":
        hz = str(ceil((400/32)*(2**((int(msg[2][5:])-9)/12))))
        time = tick2second(int(msg[4][5:]) ,cv1.ticks_per_beat*4 , tempo)*1000
        if time != 0:
            with open('test.txt', 'a') as f:
                f.write(f"delay({time});")
                f.write('\n')

