#!/opt/local/bin/python

import sys
from pydub import AudioSegment # requires pydub

# function to convert mm:ss to milliseconds
def time_to_ms (str_to_convert):
    minutes, seconds = str_to_convert.split(':')
    minutes = int(minutes)
    seconds = int(seconds)
    return (minutes * 60 + seconds) * 1000

if len(sys.argv) < 3:
    print("Usage: generate_ph.py <input-csv> <output-mp3> <transition-mp3>")
    print("\tAll audio files must be in a directory 'songs' in the current directory")
    quit()

infile = open(sys.argv[1], 'rU')

outfile = open(sys.argv[2], 'wb')

transition = AudioSegment.from_mp3("songs/" + sys.argv[3])

infile.readline()   # ignore the first line

# get the first song and use it

name, filename, time = infile.readline()[:-1].split(',')
time = time_to_ms(time)
result = AudioSegment.from_mp3("songs/" + filename)[time:time+(60*1000)]

# get every line in the input csv file
for line in infile:

    # grab the name, filename, and time to start at
    name, filename, time = line.split(',')
    time = time_to_ms(time)
    next_song = AudioSegment.from_mp3("songs/" + filename)[time:time+(60*1000)]

    # manually crossfade in from the transition sound clip
    cf_amt = int(1.0 * 1000)

    next_result = AudioSegment.silent(duration=(len(transition) + len(next_song) - cf_amt))

    next_result = next_result.overlay(transition) # get the transition first
    next_result = next_result.overlay(next_song.fade_in(cf_amt), position=(len(transition) - cf_amt))

    result = result.append(next_result, crossfade=(0 * 1000))

# save the final file
result.export(outfile, format="flac")
