import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


def finite_min(values):
    vals = [v for v in values if math.isfinite(v)]
    return min(vals) if vals else float('inf')


class WallStop(Node):
    def __init__(self):
        super().__init__('wall_stop')

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_cb, 10)

        # Safer parameters to reduce collisions/physics weirdness
        self.forward_speed = 0.12
        self.turn_speed = 0.35
        self.back_speed = -0.08

        self.too_close = 0.35      # if anything is closer than this, back up + turn
        self.avoid_dist = 0.55     # start turning if front/side is closer than this
        self.clear_dist = 0.70     # go forward only when all sectors are clear

        self.front_min = float('inf')
        self.left_min = float('inf')
        self.right_min = float('inf')

        self.state = "FORWARD"
        self.last_state = None
        self.turn_dir = 1.0  # +1 left, -1 right
        self.back_ticks = 0  # small backup timer

        self.timer = self.create_timer(0.1, self.control_loop)  # 10 Hz
        self.get_logger().info("WallStop v2 started (front+side sectors, backup, turn-away).")

    def scan_cb(self, msg: LaserScan):
        front = []
        left = []
        right = []

        # Define angular sectors (radians)
        front_half = math.radians(20)      # ±20°
        left_min_a = math.radians(30)      # 30° to 90°
        left_max_a = math.radians(90)
        right_min_a = math.radians(-90)    # -90° to -30°
        right_max_a = math.radians(-30)

        for i, r in enumerate(msg.ranges):
            a = msg.angle_min + i * msg.angle_increment

            if -front_half <= a <= front_half:
                front.append(r)
            elif left_min_a <= a <= left_max_a:
                left.append(r)
            elif right_min_a <= a <= right_max_a:
                right.append(r)

        self.front_min = finite_min(front)
        self.left_min = finite_min(left)
        self.right_min = finite_min(right)

    def control_loop(self):
        # If we haven't received scan yet, do nothing
        if not math.isfinite(self.front_min):
            return

        # Decide turn direction: turn away from the closer side
        # If left is closer -> turn right (dir = -1), else turn left (dir = +1)
        if self.left_min < self.right_min:
            self.turn_dir = -1.0
        else:
            self.turn_dir = +1.0

        # Emergency: if anything is VERY close, back up for a short time
        min_any = min(self.front_min, self.left_min, self.right_min)
        if min_any < self.too_close and self.state != "BACKUP":
            self.state = "BACKUP"
            self.back_ticks = 8  # 8 ticks @10Hz = 0.8s

        # Normal state transitions
        if self.state == "FORWARD":
            if (self.front_min < self.avoid_dist) or (self.left_min < self.avoid_dist) or (self.right_min < self.avoid_dist):
                self.state = "TURN"

        elif self.state == "TURN":
            if (self.front_min > self.clear_dist) and (self.left_min > self.clear_dist) and (self.right_min > self.clear_dist):
                self.state = "FORWARD"

        elif self.state == "BACKUP":
            self.back_ticks -= 1
            if self.back_ticks <= 0:
                self.state = "TURN"

        # Log only on changes
        if self.state != self.last_state:
            self.get_logger().info(
                f"State -> {self.state} | front={self.front_min:.2f} left={self.left_min:.2f} right={self.right_min:.2f}"
            )
            self.last_state = self.state

        # Output commands
        cmd = Twist()
        if self.state == "FORWARD":
            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0
        elif self.state == "TURN":
            cmd.linear.x = 0.0
            cmd.angular.z = self.turn_speed * self.turn_dir
        else:  # BACKUP
            cmd.linear.x = self.back_speed
            cmd.angular.z = 0.0

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = WallStop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

