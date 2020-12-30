# Nato Encoder

Encode hexadecimal string using the nato alphabet/numbers.

```
python3 nato_encoder.py encode -M "deadbeef" -f "result.wav"

zero zero one four uniform two whiskey four three six
```

The file `result.wav` contain an audio version of the result phrase (created locally).

You can decode the nato string in the same manner.

```
python3 nato_encoder.py decode -M "zero zero one four uniform two whiskey four three six"

deadbeef
```

The `-h` argument can help you understanding how this program is working.

```
usage: nato_encoder.py [-h] {encode,decode,map,version} ...

NATO alphabet encoder/decoder.

positional arguments:
  {encode,decode,map,version}

optional arguments:
  -h, --help            show this help message and exit
```

## Protocol

The protocol uses a starting code (2 chars of start type) followed by the message encoding.
The encoding is realized char by char with a different conversion table for even and odd characters, this technique allows to recognize easily if a char is missing in the sequence.

### Even chars

Fist nibble of the byte is encoded with a set of nato chars:

- `0`: alpha
- `1`: charlie
- `2`: echo
- `3`: golf
- `4`: india
- `5`: kilo
- `6`: mike
- `7`: oscar
- `8`: quebec
- `9`: sierra
- `a`: uniform
- `b`: whiskey
- `c`: yankee
- `d`: one
- `e`: three
- `f`: five

### Odd chars

Second nibble of the byte is encoded with a different set of nato chars:

- `0`: bravo
- `1`: delta
- `2`: foxtrot
- `3`: hotel
- `4`: juliett
- `5`: lima
- `6`: november
- `7`: papa
- `8`: romeo
- `9`: tango
- `a`: victor
- `b`: xray
- `c`: zulu
- `d`: two
- `e`: four
- `f`: six

### Special chars

- `start`: zero - used two time as starting sequence,
- `silence`: char not printed but used as separator between words (in audio).

### Dependencies

- `pydub` used for create an unique wav file,
- `speech_recognition` used for STT conversion.

## License

               GNU GENERAL PUBLIC LICENSE, Version 3
Based on pgp-words.py Copyright (C) 2015 Joe Ruether jrruethe@gmail.com
