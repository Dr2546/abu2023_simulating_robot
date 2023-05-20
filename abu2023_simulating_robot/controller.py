import rclpy
from rclpy.node import Node
from rclpy.qos import QoSReliabilityPolicy
from geometry_msgs.msg import Twist
import serial
import math
from gazebo_msgs.srv import GetEntityState

class Controller(Node):

    def __init__(self):
        super().__init__('controller')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_RELIABLE)
        self.serial_ = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
        self.state = 'idle'
        self.client = self.create_client(GetEntityState, "/gazebo/get_entity_state")
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("/gazebo/get_entity_state service is not available")
            exit(1)
        self.client2 = self.create_client(GetEntityState, "/gazebo/get_entity_state")
        if not self.client2.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("/gazebo/get_entity_state service is not available")
            exit(1)
        

    def run(self):
        while rclpy.ok():
            #print(self.serial_.in_waiting)
            if self.serial_.in_waiting > 0:
                data = self.serial_.readline().strip()
                l = str(data).split()
                try :
                    x = int(l[0][2:])
                    y = int(l[1])
                    r = int(l[2])
                    s = int(l[4][:-1])
                except Exception as e:
                    print(e)
                else:
                    msg = Twist()
                    msg.linear.z = 0.0
                    msg.angular.x = 0.0
                    msg.angular.y = 0.0
                    if y > 3000:
                        msg.linear.x = -1.0
                    elif y < 1200:
                        msg.linear.x = 1.0
                    else:
                        msg.linear.x = 0.0
                    
                    if x > 3000:
                        msg.linear.y = -1.0
                    elif x < 1200:
                        msg.linear.y = 1.0
                    else:
                        msg.linear.y = 0.0

                    if r > 3000:
                        msg.angular.z = 4.0
                    elif r < 1200:
                        msg.angular.z = -4.0
                    else:
                        msg.angular.z = 0.0

                    self.publisher_.publish(msg)

                    if s != 0 and self.state == 'idle':
                        self.state = 'shoot'
                        myreq = GetEntityState.Request()
                        myreq.name = "my_bot"
                        myreq.reference_frame = "world"

                        future = self.client.call_async(myreq)
                        rclpy.spin_until_future_complete(self, future)
                        if future.result() is None:
                            self.get_logger().error("Service call failed")
                            exit(1)

                        # Print the result
                        response = future.result()

                        myposx = response.state.pose.position.x
                        myposy = response.state.pose.position.y
                        myposz = response.state.pose.position.z

                        # Create a request to get the state of the "my_bot" entity relative to the "world" frame
                        request = GetEntityState.Request()
                        pole = ['abu_pole_small_3','abu_pole_small_4','abu_pole_small_5','abu_pole_small_2','abu_pole_small_1','abu_pole_big','abu_pole_small_0','abu_pole_small','abu_pole_small_6','abu_pole_small_8','abu_pole_small_7']
                        request.name = pole[s+1]
                        request.reference_frame = "world"
                        # Call the service and wait for the response
                        future = self.client2.call_async(request)
                        rclpy.spin_until_future_complete(self, future)
                        if future.result() is None:
                            self.get_logger().error("Service call failed")
                            exit(1)

                        # Print the result
                        response = future.result()

                        objposx = response.state.pose.position.x
                        objposy = response.state.pose.position.y
                        objposz = response.state.pose.position.z

                        distance = math.sqrt( (objposx-myposx)**2 + (objposy-myposy)**2 + (objposz-myposz)**2 )

                        print("Distance between {0} and my_bot is {1}".format(request.name,distance))
                    
                    if s == 0 and self.state == 'shoot':
                        self.state = 'idle'



    def stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def goforward(self):
        msg = Twist()
        msg.linear.x = -0.6
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def gobackward(self):
        msg = Twist()
        msg.linear.x = 0.6
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def goright(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = -0.6
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)

    def goleft(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.6
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    controller = Controller()

    #rclpy.spin(controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.run()
    
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()