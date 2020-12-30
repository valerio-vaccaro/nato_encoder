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

# Need ffmpeg
# If you have problem with pocketsphinx check https://github.com/bambocher/pocketsphinx-python/issues/28

import sys
import json
import argparse
from os import path
from pydub import AudioSegment
from pydub.playback import play, _play_with_ffplay
import speech_recognition as sr

VERSION = '0.0.2'

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

def main():
    parser = argparse.ArgumentParser(description='NATO alphabet encoder/decoder.')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_encode = subparsers.add_parser('encode')
    parser_encode.add_argument('-f', '--filename', help='Audio output filename (.wav)', required=False)
    parser_encode.add_argument('-s', '--speaker', help='Audio output on speakers', action='store_true')
    parser_encode.add_argument('-A', '--ascii-message', help='Message', required=False)
    parser_encode.add_argument('-H', '--hex-message', help='Message', required=False)

    parser_decode = subparsers.add_parser('decode')
    parser_decode.add_argument('-f', '--filename', help='Audio input filename (.wav) - Hic sunt leones!', required=False)
    parser_decode.add_argument('-m', '--mic', help='Audio input from microphone - Hic sunt leones!', required=False)
    parser_decode.add_argument('-M', '--message', help='Message', required=False)

    parser_map = subparsers.add_parser('map')

    parser_version = subparsers.add_parser('version')

    args = parser.parse_args()

    if args.command == 'encode':

        if args.ascii_message is not None or args.hex_message is not None:

            if args.ascii_message is not None:
                fingerprint = args.ascii_message.encode('ascii').hex().lower().replace(' ', '')

            elif args.hex_message is not None:
                fingerprint = args.hex_message.lower().replace(' ', '')

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

            if args.filename is not None:
                result_sound.export(args.filename, format='wav')
            if args.speaker:
                _play_with_ffplay(result_sound)

        else:
            print('Missing ascii or hex message parameter')

    elif args.command == 'decode':

        if args.filename is not None or args.mic is not None or args.message is not None:

            if args.mic is not None:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print('Say something!')
                    audio = r.listen(source)
                try:
                    # words = r.recognize_sphinx(audio).lower()
                    words = r.recognize_google(audio).lower() # better performace, less privacy
                except sr.UnknownValueError:
                    print('Could not understand audio')
                except sr.RequestError as e:
                    print('Error; {0}'.format(e))

            if args.filename is not None:
                r = sr.Recognizer()
                with sr.AudioFile(path.join(path.dirname(path.realpath(__file__)), args.filename)) as source:
                    audio = r.record(source)
                try:
                    # words = r.recognize_sphinx(audio).lower()
                    words = r.recognize_google(audio).lower() # better performace, less privacy
                except sr.UnknownValueError:
                    print('Could not understand audio')
                except sr.RequestError as e:
                    print('Error; {0}'.format(e))

            elif args.message is not None:
                words = args.message.lower()

            # correct well known mistakes
            words = words.replace('0', 'zero ')
            words = words.replace('1', 'one ')
            words = words.replace('2', 'two ')
            words = words.replace('3', 'three ')
            words = words.replace('4', 'four ')
            words = words.replace('5', 'five ')
            words = words.replace('6', 'six ')
            words = words.replace('8', 'seven ')
            words = words.replace('8', 'eight ')
            words = words.replace('9', 'nine ')
            words = words.replace('alpha', 'alfa')
            words = words.replace('to extract', 'foxtrot')
            words = words.replace('for', 'four')
            words = words.replace('to', 'two')
            words = words.replace('unifourm', 'uniform')
            words = words.replace('juliet', 'juliett')
            words = words.replace('victwor', 'victor')
            words = words.replace('x-ray', 'xray')
            words = words.replace('is', '')
            words = words.replace('dell ten', 'delta')
            words = words.replace('stocks tracts', 'foxtrot')
            words = words.replace('stwocks tracts', 'foxtrot')
            words = words.replace('indiana', 'india')
            words = words.replace('might be', 'mike')
            words = words.replace('x. ray', 'xray')
            words = words.replace('soon', 'zulu')
            words = words.replace('whkey', 'whiskey')
            words = words.replace('   ', ' ')
            words = words.replace('  ', ' ')
            words = ' '.join(words.split())
            print(words)

            words = words.split(' ')
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

        else:
            print('Missing filename or message parameter')

    elif args.command == 'map':
        print(json.dumps(conv, sort_keys=True, indent=4))

    elif args.command == 'version':
        print('NATO encoder - Version {}'.format(VERSION))
        print('GNU GENERAL PUBLIC LICENSE, Version 3')
        print('')
        print('')
        print('GREETINGS PROFESSOR FALKEN')
        print('')
        print('HELLO')
        print('')
        print('A STRANGE GAME.')
        print('THE ONLY WINNING MOVE IS')
        print('NOT TO PLAY.')


if __name__ == '__main__':
    main()
