import rclpy
from rclpy.node import Node
import sys
from gazebo_msgs.srv import GetEntityState
import math

class MyClientNode(Node):

    def __init__(self):
        super().__init__("my_client_node")

        myclient = self.create_client(GetEntityState, "/gazebo/get_entity_state")
        if not myclient.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("/gazebo/get_entity_state service is not available")
            exit(1)

        myreq = GetEntityState.Request()
        myreq.name = "my_bot"
        myreq.reference_frame = "world"

        future = myclient.call_async(myreq)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is None:
            self.get_logger().error("Service call failed")
            exit(1)

        # Print the result
        response = future.result()

        myposx = response.state.pose.position.x
        myposy = response.state.pose.position.y
        myposz = response.state.pose.position.z

        # Create a client for the "/gazebo/get_entity_state" service
        self.client = self.create_client(GetEntityState, "/gazebo/get_entity_state")

        # Wait for the service to become available
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error("/gazebo/get_entity_state service is not available")
            exit(1)

        # Create a request to get the state of the "my_bot" entity relative to the "world" frame
        request = GetEntityState.Request()
        request.name = sys.argv[1]
        request.reference_frame = "world"

        # Call the service and wait for the response
        future = self.client.call_async(request)
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

def main(args=None):
    rclpy.init(args=args)
    node = MyClientNode()
    rclpy.spin_once(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()