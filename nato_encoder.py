#!/usr/bin/env python3
#
# Copyright (C) 2020 Valerio Vaccaro nato_converter@valeriovaccaro.it
# Based on pgp-words.py Copyright (C) 2015 Joe Ruether jrruethe@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from pydub import AudioSegment

nato = [
    'alfa', 'bravo', 'charlie', 'delta',     #  0-3
    'echo', 'foxtrot', 'golf', 'hotel',      #  4-7
    'india', 'juliett', 'kilo', 'lima',      #  8-11
    'mike', 'november', 'oscar', 'papa',     # 12-15
    'quebec', 'romeo', 'sierra', 'tango',    # 16-19
    'uniform', 'victor', 'whiskey', 'xray',  # 20-23
    'yankee', 'zulu', 'one', 'two',          # 24-27
    'three', 'four', 'five', 'six',          # 28-31
    'seven', 'eight', 'nine', 'zero',        # 32-35
    ]

conv = {
 'even': {
    '0': nato[0],
    '1': nato[2],
    '2': nato[4],
    '3': nato[6],
    '4': nato[8],
    '5': nato[10],
    '6': nato[12],
    '7': nato[14],
    '8': nato[16],
    '9': nato[18],
    'a': nato[20],
    'b': nato[22],
    'c': nato[24],
    'd': nato[26],
    'e': nato[28],
    'f': nato[30],
 },
 'odd': {
    '0': nato[1],
    '1': nato[3],
    '2': nato[5],
    '3': nato[7],
    '4': nato[9],
    '5': nato[11],
    '6': nato[13],
    '7': nato[15],
    '8': nato[17],
    '9': nato[19],
    'a': nato[21],
    'b': nato[23],
    'c': nato[25],
    'd': nato[27],
    'e': nato[29],
    'f': nato[31],
 },
 'special': {
    'start': nato[35],
    'silence': 'silence',
 },
}

if len(sys.argv) == 2:
    fingerprint = sys.argv[1].lower().replace(' ', '')

    result = ''
    result_sound =  AudioSegment.from_wav(f"sounds/{conv['special']['silence']}.wav")

    result = f"{result}{conv['special']['start']} "
    result = f"{result}{conv['special']['start']} "
    result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['start']}.wav")
    result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['silence']}.wav")
    result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['start']}.wav")
    result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['silence']}.wav")

    for i in range(0, len(fingerprint)):
        if i % 2 == 0: # Even
            result = f"{result}{conv['even'][fingerprint[i]]} "
            result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['even'][fingerprint[i]]}.wav")
            result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['silence']}.wav")
        else: # Odd
            result = result + conv['odd'][fingerprint[i]] + ' '
            result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['odd'][fingerprint[i]]}.wav")
            result_sound = result_sound + AudioSegment.from_wav(f"sounds/{conv['special']['silence']}.wav")

    print(result)
    result_sound.export('result.wav', format='wav')
else:
    words = sys.argv[1:]
    even = True
    result = ''
    for i in words:
        if not i == conv['special']['start']:
            if even:
                even = False
                character = list(conv['even'].keys())[list(conv['even'].values()).index(i)]
                result = f'{result}{character}'
            else:
                even = True
                character = list(conv['odd'].keys())[list(conv['odd'].values()).index(i)]
                result = f'{result}{character}'

    print(result)
