from time import sleep

import mido

def list_ports():
    print("Available MIDI input ports:")
    print(mido.get_input_names())

    print("\nAvailable MIDI output ports:")
    print(mido.get_output_names())

class Matribox:
    # Port MIDI
    input_port_name = "Matribox II PRO MIDI 0"  # Remplace par le nom du port d'entrée
    output_port_name = "Matribox II PRO MIDI 1"  # Remplace par le nom du port de sortie

    def __init__(self):
        # Ouvrir le port MIDI d'entrée et de sortie
        self.input_port = mido.open_input(Matribox.input_port_name)
        self.output_port = mido.open_output(Matribox.output_port_name)

    def __del__(self):
        try:
            self.input_port.close()
            self.output_port.close()
        except Exception as e:
            print(f"Error closing port: {e}")

    def send_sysex_message(self, sysex_data):
        # Créer un message SYSEX
        sysex_message = mido.Message('sysex', data=sysex_data)
        self.output_port.send(sysex_message)  # Utiliser le port de sortie
        print(f"Sent SYSEX message: {sysex_data}")

    def decode_sysex(self, message):
        if message.type == 'sysex':
            # Décoder les données SYSEX
            sysex_data = message.data
            print(f"Received SYSEX: {sysex_data}")

    def monitor_matribox_midi(self):
        print(f"Listening on '{Matribox.input_port_name}'...")
        for message in self.input_port:
            self.decode_sysex(message)

    def send_display_screen_drum(self, display: bool):
        """
        Looper on/off:
        0-63: Off
        64-127: On
        :return:
        """
        if display:
            message = mido.Message('control_change', channel=0, control=92, value=120)
        else:
            message = mido.Message('control_change', channel=0, control=92, value=60)
        self.output_port.send(message)

    def send_display_screen_looper(self, display: bool):
        """
        Looper on/off:
        0-63: Off
        64-127: On
        :return:
        """
        if display:
            message = mido.Message('control_change', channel=0, control=59, value=120)
        else:
            message = mido.Message('control_change', channel=0, control=59, value=60)
        self.output_port.send(message)

    def send_display_tuner(self, display: bool):
        """
        ???
        """
        if display:
            message = mido.Message('control_change', channel=0, control=58, value=120)
        else:
            message = mido.Message('control_change', channel=0, control=58, value=60)
        self.output_port.send(message)

    def send_knob(self, knob_id: int, value: int):
        """
        updates the value of the quick adjustment knob
        :param value: 0-100
        :param knob_id: 1-3
        :return:
        """
        if value < 0 or value > 100:
            raise ValueError("value must be [0-100]")

        if knob_id == 1:
            message = mido.Message('control_change', channel=0, control=16, value=value)
        if knob_id == 2:
            message = mido.Message('control_change', channel=0, control=18, value=value)
        if knob_id == 3:
            message = mido.Message('control_change', channel=0, control=20, value=value)
        else:
            raise ValueError("knob_id must be [1-3]")
        self.output_port.send(message)

    def send_looper_play(self):
        """
        Looper Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=62, value=120)
        self.output_port.send(message)

    def send_looper_undo_redo(self):
        """
        :return:
        """
        message = mido.Message('control_change', channel=0, control=63, value=0)
        self.output_port.send(message)

    def send_looper_record(self):
        """
        :return:
        """
        message = mido.Message('control_change', channel=0, control=60, value=0)
        self.output_port.send(message)

    def send_looper_auto_record(self):
        """
        :return:
        """
        message = mido.Message('control_change', channel=0, control=61, value=0)
        self.output_port.send(message)

    def send_looper_delete(self):
        """
        :return:
        """
        message = mido.Message('control_change', channel=0, control=64, value=0)
        self.output_port.send(message)

    def send_looper_playback_volume(self, volume: int):
        """
        :volume: 0-100
        :return:
        """
        if volume < 0 or volume > 100:
            raise ValueError("volume must be [0-100]")

        message = mido.Message('control_change', channel=0, control=66, value=volume)
        self.output_port.send(message)

    def send_looper_recording_volume(self, volume: int):
        """
        :volume: 0-100
        :return:
        """
        if volume < 0 or volume > 100:
            raise ValueError("volume must be [0-100]")

        message = mido.Message('control_change', channel=0, control=65, value=volume)
        self.output_port.send(message)

    def send_looper_placement(self, before_multieffects: bool):
        """
        :before_multieffects:
        :return:
        """
        if before_multieffects:
            message = mido.Message('control_change', channel=0, control=67, value=120)
        else:
            message = mido.Message('control_change', channel=0, control=67, value=60)
        self.output_port.send(message)

    def send_looper_stop(self):
        """
        Looper Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=62, value=60)
        self.output_port.send(message)

    def send_footswitch_stomp_mode(self):
        """
        Footswitch Modes:
        0-63: Preset Mode
        64-127: Stomp Mode
        :return:
        """
        message = mido.Message('control_change', channel=0, control=29, value=120)
        self.output_port.send(message)

    def send_footswitch_preset_mode(self):
        """
        Footswitch Modes:
        0-63: Preset Mode
        64-127: Stomp Mode
        :return:
        """
        message = mido.Message('control_change', channel=0, control=29, value=60)
        self.output_port.send(message)

    def send_drum_start(self):
        """
        Drum Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=93, value=120)
        self.output_port.send(message)

    def send_drum_stop(self):
        """
        Drum Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=93, value=60)
        self.output_port.send(message)

    def send_drum_rythm(self, rythm: int):
        """
        :rythm: 0: "Rock-Rock 1" / 1: "Rock-Rock 2" / ... / 99: "Metronome-9/8"
        :return:
        """
        if rythm < 0 or rythm > 99:
            raise ValueError("rythm must be [0-99]")

        message = mido.Message('control_change', channel=0, control=94, value=rythm)
        self.output_port.send(message)

    def send_drum_volume(self, volume: int):
        """
        :volume: 0-100
        :return:
        """
        if volume < 0 or volume > 100:
            raise ValueError("volume must be [0-100]")

        message = mido.Message('control_change', channel=0, control=95, value=volume)
        self.output_port.send(message)

    def send_drum_bpm(self, bpm: int):
        """
        :bpm: 40-300
        :return:
        """
        if 40 <= bpm <= 127:
            message = mido.Message('control_change', channel=0, control=68, value=0)
            self.output_port.send(message)
            message = mido.Message('control_change', channel=0, control=69, value=bpm)
            self.output_port.send(message)
        elif 128 <= bpm <= 255:
            message = mido.Message('control_change', channel=0, control=68, value=1)
            self.output_port.send(message)
            message = mido.Message('control_change', channel=0, control=69, value=bpm - 128)
            self.output_port.send(message)
        elif 256 <= bpm <= 300:
            message = mido.Message('control_change', channel=0, control=68, value=2)
            self.output_port.send(message)
            message = mido.Message('control_change', channel=0, control=69, value=bpm - 256)
            self.output_port.send(message)
        else:
            raise ValueError("volume must be [40-300]")


    def send_drum_tap(self):
        """
        ???
        """
        message = mido.Message('control_change', channel=0, control=70, value=0)
        self.output_port.send(message)

    def send_ctrl(self, ctrl: int, value: int):
        """
        ???
        :ctrl: 1-4
        :value: 0-127
        :return:
        """
        if ctrl < 1 or ctrl > 4:
            raise ValueError("ctrl must be [1-4]")

        if value < 0 or value > 127:
            raise ValueError("value must be [0-100]")

        message = mido.Message('control_change', channel=0, control=70 + ctrl, value=value)
        self.output_port.send(message)

if __name__ == '__main__':
    list_ports()
    m = Matribox()

    # m.monitor_matribox_midi()

    m.send_display_tuner(True)
    # m.send_display_screen_drum(True)
    # m.send_drum_tap(40)
    # m.send_footswitch_stomp_mode()
    # m.send_display_screen_looper(True)
    # m.send_looper_auto_record()
    # m.send_looper_recording_volume(50)
    # m.send_looper_playback_volume(50)
    # m.send_looper_placement(True)
    # sleep(5)
    # m.send_looper_placement(False)
    # m.send_looper_record()
    # m.send_drum_start()
    # m.send_looper_play()
    # sleep(5)
    # m.send_looper_stop()
    # m.send_display_screen_looper(False)
    # m.send_drum_stop()
