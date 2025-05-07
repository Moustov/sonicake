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

    def send_looper_screen_on_off(self, display: bool):
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

    def send_looper_play(self):
        """
        Looper Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=62, value=120)
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

    def send_start_drum(self):
        """
        Drum Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=93, value=120)
        self.output_port.send(message)

    def send_stop_drum(self):
        """
        Drum Play/Stop
        0-63: Stop
        64-127: Play
        :return:
        """
        message = mido.Message('control_change', channel=0, control=93, value=60)
        self.output_port.send(message)

if __name__ == '__main__':
    list_ports()
    m = Matribox()
    # m.monitor_matribox_midi()
    m.send_footswitch_stomp_mode()
    m.send_looper_screen_on_off(True)
    m.send_start_drum()
    m.send_looper_play()
    sleep(5)
    m.send_looper_stop()
    m.send_looper_screen_on_off(False)
    m.send_stop_drum()
