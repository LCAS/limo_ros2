import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LimoSpeakerConsoleTTS(Node):
    def __init__(self):
        super().__init__('limo_speaker_console_tts_publisher')
        self.publisher_ = self.create_publisher(String, '/speaker/tts', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        user_input = input("> ").strip().replace('"', "'").replace("!,", "")
        msg = String()
        msg.data = user_input
        self.publisher_.publish(msg)
        # Print the command to teach users how to do it manually
        print(f"ros2 topic pub -1 /speaker/tts std_msgs/msg/String \"data: '{user_input}'\"\n")

def main(args=None):
    rclpy.init(args=args)
    tts_pub = LimoSpeakerConsoleTTS()
    rclpy.spin(tts_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tts_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    print("What do you want me to say?\n\n")
    main()