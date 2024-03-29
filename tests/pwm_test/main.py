import machine
import time

# Set up the ADC pin (Phototransistor) and output pin (Coil)
adc = machine.ADC(machine.Pin(36))
out_pin = machine.Pin(23, machine.Pin.OUT)

# Define constants
# Define the threshold value for the ADC
ADC_THRESHOLD = 900
# Define the number of consecutive samples below the threshold needed to trigger the output pulse
CONSECUTIVE_SAMPLES = 5
# Define the duration of the output pulse in milliseconds
PULSE_DURATION = 10 # ms

# Initialize variables
# Number of consecutive samples below the threshold
consecutive_below_threshold = 0
# Time since the last output pulse
last_pulse_time = time.ticks_ms()
# Create hardware timer
tim = machine.Timer(1)
# Configure PWM
pwm_frequency = 1000 # Hz
# Create an instance of the PWM object
pwm = machine.PWM(out_pin, freq=pwm_frequency, duty=0)
# Configure minimum time between pulses
max_pulse_interval = 10 # ms


# To be called when the timer triggers
def timer_callback(timer):
    print("Timer Callback")
    pwm.duty(0)


while True:
    # Read the ADC value
    adc_value = adc.read()
    print(adc_value)

    # Check if the ADC value is below the threshold
    if adc_value < ADC_THRESHOLD:
        consecutive_below_threshold += 1
    else:
        consecutive_below_threshold = 0

    # Check if we have enough consecutive samples below the threshold to trigger the output pulse
    if consecutive_below_threshold >= CONSECUTIVE_SAMPLES:
        # Calculate the elapsed time since the last pulse
        elapsed_time = time.ticks_diff(time.ticks_ms(), last_pulse_time)

        # Check if we have waited long enough to trigger another pulse
        if elapsed_time >= max_pulse_interval:
            print("Pulsing! ADC:", adc_value, "Elapsed:", elapsed_time, "Consecutive:", consecutive_below_threshold)
            # Turn on the output pin PWM signal
            pwm.duty(150)
        
            # Set the timer to trigger after the pulse duration and call the timer_callback function
            # This will turn off the PWM signal on this coil after PULSE_DURATION ms
            tim.init(period=PULSE_DURATION, mode=machine.Timer.ONE_SHOT, callback=timer_callback)

            # Reset the consecutive samples counter and update the last pulse time
            consecutive_below_threshold = 0
            last_pulse_time = time.ticks_ms()