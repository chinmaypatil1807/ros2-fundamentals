import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talk(Node):
	def __init__(self):
		super().__init__('talker')
		self.pub= self.create_publisher(String,'chat',10)
		self.timer=self.create_timer(0.5,self.publish_msg)
		self.i=0
	def publish_msg(self):
		msg=String()
		msg.data = f'Hello world : {self.i}'
		self.pub.publish(msg)
		self.get_logger().info(f'Publishing:"{msg.data}"')
		self.i+=1

def main():
	rclpy.init()
	node =Talk()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()
