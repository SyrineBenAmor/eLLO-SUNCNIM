import RPi.GPIO as GPIO

def config_input(marche,sens):
    print("configure input")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)#use physical pin numbering
    GPIO.setup(marche,GPIO.IN,pull_up_down=GPIO.PUD_DOWN )#set pin marche to be an input pin and set
    GPIO.setup(sens,GPIO.IN,pull_up_down=GPIO.PUD_DOWN )#set pin marche to be an input pin and set initial value to be pulled low(off)
    if GPIO.input(marche) == GPIO.HIGH:
        print("robot en mouvement")
    else:
        print("robot fixe")
    if GPIO.input(sens) == GPIO.HIGH:
        print("aller")
    else:
        print("retour")
