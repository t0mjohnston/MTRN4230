#!/usr/bin/env python
# BEGIN ALL
import rospy
from time import sleep
from std_msgs.msg import String
# import cv2, cv_bridge

class Publisher: 
    def __init__(self): 
        self.pub = rospy.Publisher("/comms/cam_ready", String, queue_size=1)
        self.camera_ready = "ready"

    def run(self): 
        self.pub.publish(self.camera_ready)

if __name__ == "__main__": 
    try: 
        rospy.init_node('ur5_comms_vision_send')
        publisher = Publisher()
        rate = rospy.Rate(0.5)
        # message_wait = rospy.Rate(2)
        while not rospy.is_shutdown(): 
            # connections = publisher.pub.get_num_connections()
            # if connections > 0: 
            #     publisher.run()
            #    # break
            
            # rate.sleep()
            val = str(raw_input("> "))
            if val.lower() in ["ready", "r"]: 
                publisher.run()

        rospy.spin()
    except rospy.ROSInterruptException, e: 
        raise e
