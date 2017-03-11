# POWER HOUR

This script generates a power hour playlist given a csv file of song names, filenames, and times to begin each song.

## Requirements
- [pydub](http://pydub.com/)

## Usage
`python generate_ph.py <input-csv> <output-mp3> <transition-mp3>`

All audio files must be in a directory 'songs' in the current directory.
The format of the input .csv file is as follows: 
> `[Name],[filename],[timestamp]`

The script takes the first minute of each song in `filename` starting at time `timestamp`.
