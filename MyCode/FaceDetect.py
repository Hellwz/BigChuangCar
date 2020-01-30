import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13
CamServoPin1 = 11
CamServoPin2 = 9

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化操作
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    
    global pwm_servo1,pwm_servo2
    GPIO.setup(CamServoPin1, GPIO.OUT)
    GPIO.setup(CamServoPin2, GPIO.OUT)
    #设置pwm引脚和频率为50hz
    pwm_servo1 = GPIO.PWM(CamServoPin1, 50)
    pwm_servo2 = GPIO.PWM(CamServoPin2, 50)
    pwm_servo1.start(6.8)#2.5-11.5
    pwm_servo2.start(9)#4.5-12
    time.sleep(0.1)
    pwm_servo1.stop()
    pwm_servo2.stop()
    
#小车前进   
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    #time.sleep(delaytime)
    #brake(0)

#小车后退
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    #time.sleep(delaytime)
    #brake(0)

#小车左转   
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)

#小车右转
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)
    brake(0)

#小车原地左转
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)
    brake(0)

#小车原地右转
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)
    brake(0)

#小车停止   
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(0)
    time.sleep(delaytime)
    
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
motor_init()
while True:
    #time.sleep(1)
    
    ret, img = cap.read()
    #img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    maxw = 0
    maxh = 0
    nowx = -1
    nowy = -1
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        if (w>maxw and h>maxh):
            maxw = max(maxw,w)
            maxh = max(maxh,h)
            nowx = x
            nowy = y
    cv2.imshow('video',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        brake(0)
        break
    '''
    if (nowx!=-1 and nowy!=-1):
        if nowx+2/w<280:spin_left(0.1)
        elif nowx+2/w>360:spin_right(0.1)
        else: brake(0)
    else: brake(0)
    '''
    if (maxw!=0 and maxh!=0):
        if (maxw>200 and maxh>200):back(0)
        elif (maxw<100 and maxh<100):run(0)
        else: brake(0)
    else:brake(0)
    
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()