import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelPublisher(Node):

    def __init__(self):
        super().__init__('cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        msg = Twist()

        if self.counter < 5:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info("Moving Forward")
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info("Rotating")

        self.publisher_.publish(msg)
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
