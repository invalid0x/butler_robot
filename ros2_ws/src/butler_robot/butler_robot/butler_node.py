import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep

class ButlerRobot(Node):
    def __init__(self):
        super().__init__('butler_robot')
        self.subscription = self.create_subscription(
            String,
            'order',
            self.order_callback,
            10)
        self.state = 'home'

    def order_callback(self, msg):
        self.get_logger().info('Received order: "%s"' % msg.data)
        self.handle_order(msg.data)

    def handle_order(self, table):
        self.move_to('kitchen')
        if self.confirm('kitchen'):
            self.move_to(table)
            if self.confirm(table):
                self.get_logger().info('Delivered food to %s' % table)
                self.move_to('home')
            else:
                self.move_to('kitchen')
                self.move_to('home')
        else:
            self.move_to('home')

    def move_to(self, location):
        self.get_logger().info('Moving to %s' % location)
        self.state = location
        sleep(2)

    def confirm(self, location):
        self.get_logger().info('Waiting for confirmation at %s' % location)
        sleep(2)
        return True

def main(args=None):
    rclpy.init(args=args)
    butler_robot = ButlerRobot()
    rclpy.spin(butler_robot)
    butler_robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
