import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

esp32_hostname = "camerarobot.local"

class StreamGetter(Node):
    def __init__(self):
        super().__init__('stream_getter')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.cap = cv2.VideoCapture("http://" + esp32_hostname + ":81/stream")
        self.bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing video frame on /camera/image_raw')

def main(args=None):
    rclpy.init(args=args)
    stream_getter = StreamGetter()
    rclpy.spin(stream_getter)
    stream_getter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
