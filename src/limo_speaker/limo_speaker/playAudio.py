import rclpy
from rclpy.node import Node
import sounddevice as sd
import numpy as np
import wave
from std_msgs.msg import String

class LimoSpeakerPlayAudio(Node):
    def __init__(self):
        super().__init__('limo_speaker_play_audio')
        self.subscription = self.create_subscription(
            String,
            '/speaker/play',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Trying to play sound: "%s"' % msg.data)
        self.play_wav(msg.data)

    # Plays a WAV file on the specified sound device.
    def play_wav(self, sound, device_name="USB PnP Audio Device"):
        device_index = self.get_speaker_by_name(device_name)
        if device_index is None:
            self.get_logger().warning(f"No sound device found with name containing '{device_name}'")
            return

        ## This puts it in the limo_platform/configs/sounds folder in the repo!
        file_path = f"/home/ros/robot_home/limo_platform/configs/sounds/{sound}.wav"

        try:
            with wave.open(file_path, 'rb') as wf:
                samplerate = wf.getframerate()
                frames = wf.readframes(wf.getnframes())

                # Convert bytes to NumPy array
                data = np.frombuffer(frames, dtype=np.int16)

                # Reshape if stereo
                channels = wf.getnchannels()
                if channels > 1:
                    data = data.reshape(-1, channels)

                self.get_logger().info(f"Playing {sound} sound on device {device_index} - {device_name}")

                sd.play(data, samplerate=samplerate, device=device_index)
                sd.wait()
        except:
            self.get_logger().warning(f"Couldn't play file {file_path}, does the file exist?")

    # Finds the first audio device containing the given name.
    def get_speaker_by_name(self, name_contains):
        devices = sd.query_devices()
        for idx, device in enumerate(devices):
            if name_contains.lower() in device['name'].lower():
                return idx  # Return the device index
        return None  # Return None if not found

def main(args=None):
    rclpy.init(args=args)

    playAudio = LimoSpeakerPlayAudio()

    rclpy.spin(playAudio)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    playAudio.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()