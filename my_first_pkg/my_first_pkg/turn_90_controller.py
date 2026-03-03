import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def normalize_angle(a: float) -> float:
    """Normalize angle to [-pi, pi]."""
    return math.atan2(math.sin(a), math.cos(a))

class Turn90Controller(Node):
    def __init__(self):
        super().__init__('turn_90_controller')

        # Publish velocity to turtlesim
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Subscribe to pose for feedback (theta)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)

        self.current_theta = None
        self.start_theta = None
        self.target_theta = None
        self.done = False

        # Control loop at 20 Hz
        self.timer = self.create_timer(0.05, self.control_loop)

        # Proportional gain (tuneable)
        self.kp = 2.0
        self.max_w = 1.0  # rad/s

        self.get_logger().info("Turn90Controller started. Waiting for pose...")

    def pose_cb(self, msg: Pose):
        self.current_theta = msg.theta
        if self.start_theta is None:
            self.start_theta = msg.theta
            self.target_theta = normalize_angle(self.start_theta + math.pi / 2.0)
            self.get_logger().info(
                f"Start theta: {self.start_theta:.3f} rad | Target theta: {self.target_theta:.3f} rad"
            )

    def control_loop(self):
        if self.current_theta is None or self.done:
            return

        # Angle error to target
        err = normalize_angle(self.target_theta - self.current_theta)
        self.get_logger().info(f"Current: {self.current_theta:.3f} | Error: {err:.3f}")
        # If close enough, stop
        if abs(err) < 0.03:  # ~1.1 degrees tolerance
            self.stop_robot()
            self.done = True
            self.get_logger().info("✅ Turn complete (within tolerance).")
            return

        # P-controller
        w = self.kp * err

        # Clamp angular velocity
        w = max(-self.max_w, min(self.max_w, w))

        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = w
        self.cmd_pub.publish(cmd)

    def stop_robot(self):
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = Turn90Controller()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
