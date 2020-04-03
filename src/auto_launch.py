#!/usr/bin/env python

import rospy

from rosflight_msgs.msg import RCRaw
from std_srvs.srv import TriggerRequest, Trigger

def main():
    rospy.init_node('auto_launch', anonymous=True)
    rc_pub = rospy.Publisher('RC', RCRaw, queue_size=1)
    delay_seconds = rospy.get_param('~delay',0)
    start_time = rospy.get_time()
    states = [
            ("neutral", 1),
            ("calibration", 3.),
            ("arming", 0.5),
            ("flight", 3600)]
    msg = RCRaw()
    msg.values = [1500]*8
    msg.values[2] = 1000
    rate = rospy.Rate(1)
    rospy.sleep(delay_seconds)
    for state, duration in states:
        start_time = rospy.get_time()
        rospy.logwarn(state)
        if state=='calibration':
            services = ['calibrate_baro', 'calibrate_imu']
            for s in services:
                print(s)
                call_service(s)
        if state=='arming':
            msg.values[4]=2000
        if state=='flight':
            msg.values[2]=2000

        while rospy.get_time() - start_time < duration and not rospy.is_shutdown():
            msg.header.seq += 1
            rc_pub.publish(msg)
            rate.sleep()
        if rospy.is_shutdown():
            break

def call_service(service_name):
    rospy.wait_for_service(service_name)
    srv = rospy.ServiceProxy(service_name, Trigger)
    srv(TriggerRequest())
    #rospy.sleep(1)





if __name__=='__main__':
    main()
