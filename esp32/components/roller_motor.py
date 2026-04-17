"""Roller Motor control for MicroPython ESP32"""

import machine

PWM_PIN = 22
DIR_PIN = 23

pwm = None
dir_pin = None


def init():
    """Initialize motor PWM and direction control"""
    global pwm, dir_pin
    
    pwm = machine.PWM(machine.Pin(PWM_PIN))
    pwm.freq(2000)
    pwm.duty(0)
    
    dir_pin = machine.Pin(DIR_PIN, machine.Pin.OUT)
    dir_pin.off()


def set_speed(speed):
    """Set motor speed (0-1023)"""
    if pwm:
        pwm.duty(speed)


def feed_forward(speed=180):
    """Feed label forward"""
    dir_pin.on()
    set_speed(speed)


def feed_reverse(speed=180):
    """Retract label"""
    dir_pin.off()
    set_speed(speed)


def stop():
    """Stop motor"""
    set_speed(0)
