import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.qos import QoSReliabilityPolicy

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

class JoyConverter(Node):

    def __init__(self):
        super().__init__('joyconverter')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            qos_profile_sensor_data) #QoS value must be same as Publisher
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(
            Twist,
            'cmd_vel',
            QoSReliabilityPolicy.RELIABLE
		)

    def listener_callback(self, msg):
        header = msg.header
        axes = msg.axes
        buttons = msg.buttons
        twstmsg = Twist()
        y, x, z = axes[0], axes[1], axes[2]
        twstmsg.linear.x, twstmsg.linear.y, twstmsg.linear.z, twstmsg.angular.x, twstmsg.angular.y, twstmsg.angular.z = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if x < -0.5:
            twstmsg.linear.x = 1.0
        elif x > 0.5:
            twstmsg.linear.x = -1.0
        if y < -0.5:
            twstmsg.linear.y = 1.0
        elif y > 0.5:
            twstmsg.linear.y = -1.0
        if z < -0.5:
            twstmsg.angular.z = -3.0
        elif z > 0.5:
            twstmsg.angular.z = 3.0
        self.publisher_.publish(twstmsg)
        

def main(args=None):
    rclpy.init(args=args)

    joyconverter = JoyConverter()

    rclpy.spin(joyconverter)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
