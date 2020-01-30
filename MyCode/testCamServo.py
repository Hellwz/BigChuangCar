#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
#舵机引脚定义
CamServoPin1 = 11
CamServoPin2 = 9
boundaries = [ ( [170, 43, 46 ],    #红色范围下阈值
             [180, 255, 255] ) ]  #红色范围上阈值

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#舵机引脚设置为输出模式
def init():
    global pwm_servo1,pwm_servo2
    GPIO.setup(CamServoPin1, GPIO.OUT)
    GPIO.setup(CamServoPin2, GPIO.OUT)
    #设置pwm引脚和频率为50hz
    pwm_servo1 = GPIO.PWM(CamServoPin1, 50)
    pwm_servo2 = GPIO.PWM(CamServoPin2, 50)
    pwm_servo1.start(7)#2.5-11.5
    pwm_servo2.start(6)#4.5-12
    time.sleep(0.1)
    pwm_servo1.stop()
    pwm_servo2.stop()
    
def setServoDC(servo, dc):
    pwm = GPIO.PWM(servo, 50) #channel,frequence=50Hz
    pwm.start(dc) #start pwm
    pwm.ChangeDutyCycle(dc) #change pwm
    time.sleep(0.01)
    pwm.stop()
#延时2s       
time.sleep(2)
#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。

init()
anglex = 7
angley = 6
while True:
    ret, frame = cap.read()
    cv2.imshow('Image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #RGB转HSV
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        mask = cv2.inRange(hsv, lower, upper)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        center = None
        if len(cnts) > 4:
            c = max(cnts, key=cv2.contourArea)
            ((x,y), radius) = cv2.minEnclosingCircle(c)  #得到物体中心点和物体半径大小
            print(radius,x,y)
            if radius > 10:  #检测到的物体的半径大于35像素
                if (x > 220) and (x < 420):
                    continue
                elif (x <= 220):
                    anglex = anglex + 0.05
                    if (anglex > 11.5): anglex = 11.5
                elif (x >= 420):
                    anglex = anglex - 0.05
                    if (anglex < 2.5): anglex = 2.5
                setServoDC(CamServoPin1,anglex)

                if (y > 140) and (y < 340):
                    continue 
                elif (y <=140):
                    angley = angley + 0.05
                    if (angley > 12):angley = 12
                elif (y >= 340):
                    angley = angley - 0.05
                    if (angley < 4.5): angley = 4.5
                setServoDC(CamServoPin2,angley)
            else:continue
            
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()