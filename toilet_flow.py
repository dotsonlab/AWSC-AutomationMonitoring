'''
David Rodriguez

Goal: Continuously looping while to perform valve actions at specified times, 
introduce substance at a specific ratio based on flow data, recording 
and saving flow data, and actuating a flush at a specified time.

Inputs: A schedule of events based on entered times.

Outputs: Sequence of events to a screen as they happen. 
daily flow rate data
'''
#logic testing Below is the functional portion
import datetime
import time
import threading
import Adafruit_BBIO.GPIO as GPIO


class Flow:
    GPIO.setup("P8_7", GPIO.OUT) #stepper direction
    GPIO.setup("P8_9", GPIO.OUT) #step
    GPIO.setup("P8_11", GPIO.OUT) #(0: enabled, 1: disabled)
    GPIO.setup("P8_15", GPIO.OUT) #Direction for actuator 1
    GPIO.setup("P8_17", GPIO.OUT) #PWM for actuator 1
    GPIO.setup("P8_16", GPIO.OUT) #Direction for actuator 2
    GPIO.setup("P8_18", GPIO.OUT) #PWM for actuator 2
    GPIO.setup("P9_41", GPIO.IN) #flow sensor
    GPIO.output("P8_7", GPIO.LOW) #set stepper motor direction
    GPIO.add_event_detect("P9_41", GPIO.RISING)
    currentTime = datetime.time()
    tag = ""
    eventPulses = 0
    totalPulses = 0
    speed = .001
    
    def checkFlow(self, time):
        currentTime = time
        if GPIO.event_detected("P9_41"):
            self.totalPulses = self.totalPulses + 1


    def log(self):
        day = datetime.date.today()
        time = self.currentTime.isoformat()
        liters = self.computeLiters(self.totalPulses)
        LPM = self.computeLiters(self.eventPulses)
        self.eventPulses = 0

        filename = "%s_Toilet.csv" % day.isoformat()
        target = open(filename, 'a')
        target.write("%s, %d, %d\n" % (time, LPM, liters))
        target.close()
        threading.Timer(60.0, self.log).start()

    def computeLiters(self, numberOfPulses):
        self.liters = numberOfPulses / 2200
        return self.liters

    def enableStepper(self):
        GPIO.output("P8_11", GPIO.LOW)
            
    def disableStepper(self):
        GPIO.output("P8_11", GPIO.HIGH)

    def triggerStepper(self, numberOfTimes):
        for i in range(0, numberOfTimes):
            GPIO.output("P8_9", GPIO.HIGH)
            time.sleep(self.speed)
            GPIO.output("P8_9", GPIO.LOW)
            time.sleep(self.speed)

    def toiletTrigger(self, flushType):
        if flushType == "Full":
            self.toiletFull()
        else:
            self.toiletUrine()

    def toiletUrine(self):
        print "Toilet Urine Triggered"
        self.enableStepper()
        self.triggerStepper(28250)
        GPIO.output("P8_17", GPIO.HIGH) #pwm on
        GPIO.output("P8_15", GPIO.LOw)  #extend actuator
        time.sleep(.65)
        GPIO.output("P8_15", GPIO.HIGH) #retract actuator
        time.sleep(2)
        GPIO.output("P8_17", GPIO.LOW) #pwn off
        self.disableStepper()

    def toiletFull(self):
        print "Toilet Full Triggered"
        self.enableStepper()
        self.triggerStepper(28250)
        GPIO.output("P8_18", GPIO.HIGH) #pwm on
        GPIO.output("P8_16", GPIO.LOW) #extend actuator
        time.sleep(.65)
        GPIO.output("P8_16", GPIO.HIGH) #retract actuator
        time.sleep(1)
        GPIO.output("P8_18", GPIO.LOW) #pwm on
        self.disableStepper()
        