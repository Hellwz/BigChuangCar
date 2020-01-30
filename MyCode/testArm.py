#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#舵机引脚定义
Servo1 = 23
Servo2 = 10
Servo3 = 25
Servo4 = 2

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

now1 = 7.5 #2.8-11.6
now2 = 7.5 #12.4
now3 = 7 #return 11.8
now4 = 5.5 #5.5-9

#舵机引脚设置为输出模式
def init():
    global pwm_servo1,pwm_servo2,pwm_servo3,pwm_servo4
    GPIO.setup(Servo1, GPIO.OUT)
    GPIO.setup(Servo2, GPIO.OUT)
    GPIO.setup(Servo3, GPIO.OUT)
    GPIO.setup(Servo4, GPIO.OUT)
    #设置pwm引脚和频率为50hz
    pwm_servo1 = GPIO.PWM(Servo1, 50)
    pwm_servo2 = GPIO.PWM(Servo2, 50)
    pwm_servo3 = GPIO.PWM(Servo3, 50)
    pwm_servo4 = GPIO.PWM(Servo4, 50)
    pwm_servo1.start(now1)
    time.sleep(1)
    pwm_servo2.start(now2)
    time.sleep(1)
    pwm_servo3.start(now3)
    time.sleep(1)
    pwm_servo4.start(now4)
    time.sleep(1)
    #pwm_servo1.stop()
    #pwm_servo2.stop()
    #pwm_servo3.stop()
    #pwm_servo4.stop()

def setServo1DC(dc):
    global now1
    if (dc > 11.6 or dc < 2.8):return
    while (now1<dc):
        now1 = now1 + 0.1
        pwm_servo1.ChangeDutyCycle(now1)
        time.sleep(0.05)
    while (now1>dc):
        now1 = now1 - 0.1
        pwm_servo1.ChangeDutyCycle(now1)
        time.sleep(0.05)
    time.sleep(0.2)    
def setServo2DC(dc):
    global now2
    if (dc > 12.4 or dc < 2.5):return
    while (now2<dc):
        now2 = now2 + 0.1
        pwm_servo2.ChangeDutyCycle(now2)
        time.sleep(0.05)
    while (now2>dc):
        now2 = now2 - 0.1
        pwm_servo2.ChangeDutyCycle(now2)
        time.sleep(0.05)
    time.sleep(0.2)    
def setServo3DC(dc):
    global now3
    if (dc > 11.8 or dc < 7):return
    while (now3<dc):
        now3 = now3 + 0.1
        pwm_servo3.ChangeDutyCycle(now3)
        time.sleep(0.05)
    while (now3>dc):
        now3 = now3 - 0.1
        pwm_servo3.ChangeDutyCycle(now3)
        time.sleep(0.05)
    time.sleep(0.2)    
def setServo4DC(dc):
    global now4
    if (dc > 9 or dc < 5.5):return
    while (now4<dc):
        now4 = now4 + 0.1
        pwm_servo4.ChangeDutyCycle(now4)
        time.sleep(0.05)
    while (now4>dc):
        now4 = now4 - 0.1
        pwm_servo4.ChangeDutyCycle(now4)
        time.sleep(0.05)
    time.sleep(0.2)    
#延时2s       
time.sleep(2)
#try/except语句用来检测try语句块中的错误，
#从而让except语句捕获异常信息并处理。
try:
    init()
    time.sleep(0.2)
    '''
    while True:
        a,b = map(float,input().split())
        if (a == 1):setServo1DC(b) #change pwm
        elif (a == 2):setServo2DC(b)
        elif (a == 3):setServo3DC(b)
        elif (a == 4):setServo4DC(b)
        '''
    setServo1DC(2.8)
    setServo4DC(9)
    setServo1DC(7.5)
    setServo2DC(12.2)
    setServo1DC(10)
    setServo4DC(5.5)
    setServo1DC(7.5)
    setServo4DC(9)
    setServo3DC(11.8)
    setServo2DC(2.5)
except KeyboardInterrupt:pass

GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
