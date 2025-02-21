import rclpy
from rclpy.node import Node
import sounddevice as sd
import numpy as np
import wave
import os
from std_msgs.msg import String
from time import sleep
from scipy.io import wavfile
from scipy.signal import resample

class LimoSpeakerPlayTTS(Node):
    def __init__(self):
        super().__init__('limo_speaker_play_tts')
        self.subscription = self.create_subscription(
            String,
            '/speaker/tts',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I am saying: "%s"' % msg.data)
        self.text_to_wav(msg.data) # save file to /tmp/tts.wav
        # sleep(30)
        self.play_wav() # play tts.wav

    def text_to_wav(self, text):
        process = os.system(f'espeak "{text}" -w /tmp/tts.wav')

    # Plays a WAV file on the specified sound device.
    def play_wav(self, device_name="USB PnP Audio Device"):
        device_index = self.get_speaker_by_name(device_name)
        if device_index is None:
            self.get_logger().warning(f"No sound device found with name containing '{device_name}'")
            return

        file_path = f"/tmp/tts.wav"

        try:
            with wave.open(file_path, 'rb') as wf:
                samplerate = wf.getframerate()
                frames = wf.readframes(wf.getnframes())

                # Convert bytes to NumPy array
                data = np.frombuffer(frames, dtype=np.int16)

                self.get_logger().info(f"Playing tts sound file on device {device_index} - {device_name}")

                # Get the supported sample rates for the device
                device_info = sd.query_devices(device_index, 'output')
                supported_samplerates = device_info['default_samplerate']

                # Resample if the file samplerate is not supported
                if samplerate != supported_samplerates:
                    self.get_logger().info(f"Resampling from {samplerate} to {supported_samplerates}")
                    data = resample(data, int(len(data) * supported_samplerates / samplerate))
                    data = np.asarray(data, dtype=np.int16)  # Ensure data is int16
                    samplerate = supported_samplerates

                sd.play(data, samplerate=samplerate, device=device_index)
                sd.wait()
        except Exception as e:
            self.get_logger().warning(f"Couldn't play file {file_path}, does the file exist? Error: {e}")

    # Finds the first audio device containing the given name.
    def get_speaker_by_name(self, name_contains):
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if name_contains.lower() in device['name'].lower():
                return idx  # Return the device index
        return None  # Return None if not found

def main(args=None):
    rclpy.init(args=args)
    playTTS = LimoSpeakerPlayTTS()
    rclpy.spin(playTTS)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    playTTS.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()