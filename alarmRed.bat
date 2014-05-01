REM set the duty cycle for the lights to be 250ms on/ 250ms off
usbcmdap 0 0 101 22 50 50
REM start the flashing light (red)
usbcmdap 0 0 101 20 0 2

REM turn on the buzzer
usbcmdap 0 0 102 70 1 16 255 20 20
