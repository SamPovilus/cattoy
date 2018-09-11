# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time
import random
import datetime

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min0 = 270  # Min pulse length out of 4096
servo_max0 = 410  # Max pulse length out of 4096
servo_min1 = 430  # Min pulse length out of 4096
servo_max1 = 490  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 100       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
speed = 50

f = open('/run/cattoylog.txt', 'w')
while True:
    if not ((datetime.datetime.now().hour  > 20) or (datetime.datetime.now().hour < 7)):
    
        f.write("cat toy running at " + str(datetime.datetime.now()))

        pwm.set_pwm(15,0,100)

        pwm.set_pwm(0, 0, servo_min0)
        pwm.set_pwm(1, 0, servo_min1)
        time.sleep(1.5)
        pwm.set_pwm(0, 0, servo_max0)
        pwm.set_pwm(1, 0, servo_min1)
        time.sleep(1.5)
        pwm.set_pwm(0, 0, servo_max0)
        pwm.set_pwm(1, 0, servo_max1)
        time.sleep(1.5)
        pwm.set_pwm(0, 0, servo_min0)
        pwm.set_pwm(1, 0, servo_max1)
        time.sleep(1.5)

        pos0 = servo_min0
        pos1 = servo_min1
        for _ in range(0,100):
            dest0 = random.randint(servo_min0,servo_max0)
            dest1 = random.randint(servo_min1,servo_max1)
            speed0 = (dest0 - pos0)/speed
            speed1 = (dest1 - pos1)/speed    
            for _ in range(0,speed):
                pos0 += speed0
                pos1 += speed1
                pwm.set_pwm(0, 0, int(pos0))
                pwm.set_pwm(1, 0, int(pos1))
                time.sleep(0.1)
                if(random.randint(0,35) == 1):
                    time.sleep(2.0)

        pwm.set_pwm(15,0,000)
    time.sleep(60.0*60.0*random.uniform(2.5,3.5))
