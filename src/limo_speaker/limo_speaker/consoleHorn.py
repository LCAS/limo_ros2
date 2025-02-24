import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class LimoSpeakerConsoleHorn(Node):
    def __init__(self):
        super().__init__('limo_speaker_console_horn_publisher')
        self.publisher_ = self.create_publisher(String, '/speaker/play', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        user_input = input("> ").strip().replace('"', "'").replace("!,", "")
        
        if user_input.__len__() <= 1:
            # catch empty lines
            if user_input == "":
                user_input = "car"
            elif user_input == "1":
                user_input = "car"
            elif user_input == "2":
                user_input = "truck"
            elif user_input == "3":
                user_input = "clown"
            elif user_input == "4":
                user_input = "train"
            # default catch!
            else:
                user_input = "car"
            
        msg = String()
        msg.data = user_input
        self.publisher_.publish(msg)
        # Print the command to teach users how to do it manually
        print(f"ros2 topic pub -1 /speaker/play std_msgs/msg/String \"data: '{user_input}'\"\n")

def main(args=None):
    rclpy.init(args=args)
    horn_pub = LimoSpeakerConsoleHorn()
    rclpy.spin(horn_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    horn_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    print("\033[1mLimo Horn Publisher\n\033[0mWhich horn would you like to honk?")
    print("*"*16)
    print(" 1) Car Horn\n 2) Truck Horn \n 3) Clown Horn \n 4) Train Horn")
    print("*"*16, "\n")
    main()