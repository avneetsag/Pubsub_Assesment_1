# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import rclpy
from rclpy.node import Node
import pyowm
import datetime
from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            '/weather/request',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variablea warning
                     
    def listener_callback(self, msg):
        self.get_logger().info("Location : %s" % msg.data )
        owm = pyowm.OWM('52d28a21a20009d150703b9237314905')
        mng = owm.weather_manager()
        obs = mng.weather_at_place(msg.data).weather.temperature('celius')
        location = 'weather/%s'%msg.data
        self.create_publisher(String,'weather/%s'%location,10)
        self.publisher_.publish(msg.data)
        self.get_logger().info("Weather : %s" % obs )

        
        
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
