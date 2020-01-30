#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
IN1 = 26
IN2 = 19
IN3 = 21
IN4 = 20
ENA = 13
ENB = 16
Servo1 = 23
Servo2 = 10
Servo3 = 25
Servo4 = 2

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

#小车前进	
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)
    brake(0)

#小车后退
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(10)
    pwm_ENB.ChangeDutyCycle(10)
    time.sleep(delaytime)
    brake(0)

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
#从而让except语句捕获异常信息并处理。。
try:
    motor_init()
    init()
    '''
    while True:
        command = input()
        for i in range(len(command)):
            if command[i] == 'a':
                spin_left(1)
            elif command[i] == 'w':
                run(1)
            elif command[i] == 'd':
                spin_right(1)
            elif command[i] == 's':
                back(1)
            elif command[i] == 'x':
                brake(1)
    brake(1)
    '''
    #run(2)
    spin_right(1.85)
    #back(0.1)
    setServo2DC(12.2)
    setServo1DC(2.8)
    setServo4DC(9)
    setServo1DC(10)
    setServo4DC(5.5)
    setServo1DC(7.5)
    setServo4DC(9)
    setServo3DC(11.8)
    setServo2DC(2.5)
except KeyboardInterrupt:
    pass
pwm_ENA.stop()
pwm_ENB.stop()
GPIO.cleanup() 

