Matribox II Pro controller from Sonicake 
===

# Background

## SysEx
You may use Matribox II Pro Software V1.0.0 for Windows.zip to drive
your Matribox, but if you use [Wireshark](https://www.wireshark.org/) to scan USB messages,
you will see SYSEX messages

> **SysEx** : *System Exclusive Messages* are messages send information about a synthesizer's functions, 
> rather than performance data such as which notes are being played and how loud.
> Because they can include functionality beyond what the MIDI standard provides, they are a major reason 
> for the flexibility and longevity of the MIDI standard. Manufacturers use them to create proprietary messages
> that control their equipment more thoroughly than the limitations of standard MIDI messages.
> The MIDI Manufacturers Association issues a unique identification number to MIDI companies.
> These are included in SysEx messages, to ensure that only the specifically addressed device responds to the message, 
> while all others know to ignore it. Many instruments also include a SysEx ID setting, so a controller 
> can address two devices of the same model independently.

> SYSEX message example when "DRUM" button is activated
> ````
> 0000   1b 00 10 f0 98 4a 09 ae ff ff 00 00 00 00 09 00
> 0010   01 02 00 0f 00 83 03 48 00 00 00 04 f0 21 25 04
> 0020   4d 50 00 04 00 7b 00 04 14 00 00 04 00 00 01 04
> 0030   00 00 00 04 00 01 01 04 00 0c 00 04 00 00 00 04
> 0040   00 00 01 04 09 00 00 04 08 01 00 04 00 00 00 04
> 0050   00 00 00 04 00 00 00 04 00 00 01 04 01 00 00 07
> 0060   00 00 f7
> ````

SysEx messages start with (hexadecimal) `F0` and end with `F7`.
Universal Real Time SysEx messages start with `F0`, followed by `7F`, then include other fields before the terminating `F7`.

The following shows Universal Real Time SysEx message format (all numbers hexadecimal):

> `F0 7F` <Device-ID> <Sub-ID#1> [<Sub-ID#2> [\<parameters\>]] `F7`

where `Device-ID` (aka "*MMC device's ID*" or "*channel number*") is a value ranging from `00` to `7F` (`7F` = all devices)

> **MMC** : *MIDI Machine Control* is a subset of the MIDI specification.
> It provides specific commands for controlling recording equipment 
> such as multi-track recorders. 
> MMC messages can be sent along a standard MIDI cable for remote control 
> of such functions as Play, Fast Forward, Rewind, Stop, Pause, and Record. 
> These are "System Exclusive" ([SysEx](https://en.wikipedia.org/wiki/MIDI#System_Exclusive_messages)) messages, 
> specifically Real Time Universal SysEx messages. 


and `Sub-ID#1:` is one of the following values. The bolded values are MIDI Machine Control related:
* 01 = Long Form MTC
* 02 = MIDI Show Control
* 03 = Notation Information
* 04 = Device Control
* 05 = Real Time MTC Cueing
* 06 = **MIDI Machine Control Command**
* 07 = **MIDI Machine Control Response**
* 08 = Single Note Retune 

### Analysis
Knowing this, the sample provided above seems to embed a couple of extra data

* there is an `FO` at byte 0003 and another one at byte  001C with only one `F7` at the end :
> 0000   1b 00 10 f0 98 4a 09 ae ff ff 00 00 00 00 09 00 <br>
> 0010   01 02 00 0f 00 83 03 48 00 00 00 04 **f0** 21 25 04 <br>
> 0020   4d 50 00 04 00 7b 00 04 14 00 00 04 00 00 01 04 <br>
> 0030   00 00 00 04 00 01 01 04 00 0c 00 04 00 00 00 04 <br>
> 0040   00 00 01 04 09 00 00 04 08 01 00 04 00 00 00 04 <br>
> 0050   00 00 00 04 00 00 00 04 00 00 01 04 01 00 00 07 <br>
> 0060   00 00 **f7** <br>
* according to the standard, the Matribox ID should be 0x21 (33) and the sub ID 0x25 (37)
   > the decode_sysex() method provides a sequence that starts with `[0x21, 0x25, 0x4D, 0x50, 0x00, 0x00, ...]` (i.e. `[33, 37, 77, 80, 0, 0, ...]`) 
* there are `0x04` values that are inserted at columns 3, 7, 11, 15 (counting from 0) 
* since the mido lib expects values < 127, it means that headers (F0) and tails (F7) should not be included in messages

### Attempts
So far, this direction lead to nowhere since the sent messages don't have any effect (e.g. 
`f0 21 25 04 4d 50 00 04 00 7b 00 04 14 00 00 04 00 00 01 04 00 00 00 04 00 01 01 04 00 0c 00 04 00 00 00 04 00 00 01 04 09 00 00 04 05 02 00 04 00 00 00 04 00 00 00 04 00 00 00 04 00 00 01 04 01 00 00 07 00 00 f7`
is supposed to start the drum module but nothing happens with `send_sysex_message()`)

# Message Control Changes
The user manual refers to a MIDI Control Information List.

Instead of using SysEx messages, "control_change" message types will be involved
````python
import mido

message = mido.Message('control_change', channel=0, control=59, value=60)
output_port = mido.open_output("Matribox II PRO MIDI 1")
output_port.send(message)
````

This way, controls and values are the one found in the list found in the manual.

# Ref
* SYSEX 101: https://www.youtube.com/watch?v=JKJMeHwydUQ
* https://midi.org
* Matribox user manual at page 55 ([French version of the user manual](https://cdn.shopify.com/s/files/1/0100/1950/4185/files/QME-200_Manual-FR.pdf?v=1728524183)), there is a "MIDI Control Information List"
* https://electronicmusic.fandom.com/wiki/System_exclusive
* https://en.wikipedia.org/wiki/MIDI_Machine_Control
* https://github.com/johnko/python-rtmidi/blob/master/examples/sendsysex.py