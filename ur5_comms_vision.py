#!/usr/bin/env python

import rospy, sys
import geometry_msgs.msg

from time import sleep 
from std_msgs.msg import String 

class ur5_comms_vision: 
    def __init__(self): 
        rospy.init_node("ur5_comms_vision", anonymous=False)
        self.camera_ready = "not ready"
        
        self.pub = rospy.Publisher("/comms/cam_ready", String, queue_size=1)
    
    def callback(self, msg): 
        pass

    def run(self): 
        self.pub.publish(self.camera_ready)

if __name__ == "__main__": 
    try: 
        follower = ur5_comms_vision()
        rate = rospy.Rate(0.5)
        message_wait = rospy.Rate(2)
        # while not rospy.is_shutdown(): 
        #     connections = follower.pub.get_num_connections()
        #     if connections > 0: 
        #         follower.run()
        #        # break
        #     
        #     rate.sleep()
        rospy.spin()
    except rospy.ROSInterruptException, e: 
        rospy.loginfo("COMMS DIE")
        raise e

# print("Exec Before")

# follower = ur5_comms_vision()
# rate = rospy.Rate(0.5)
# sleep(1)
# follower.run()

# print("Exec After")

rospy.spin()
