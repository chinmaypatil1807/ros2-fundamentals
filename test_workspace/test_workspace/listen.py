import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listen(Node):
	def __init__(self):
		super().__init__('listen')
		self.get_logger().info("Listener started and waiting on /chat ...")
		self.sub=self.create_subscription(String,'chat',self.cb,10)
	def cb(self,msg):
		self.get_logger().info(f'I heard:"{msg.data}"')
def main(args=None):
	rclpy.init(args=args)
	node =Listen()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
