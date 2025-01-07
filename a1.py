import re

def validate_time_format(time_str):
    # Define regular expression pattern for allowed time formats
    pattern = re.compile(r'^(1[0-2]|0?[1-9])\s?(AM|PM|am|pm)|((1[0-2]|0?[1-9]):([0-5][0-9])?\s?(AM|PM|am|pm))$')
    # Check if the time string matches the pattern
    if pattern.match(time_str):
        return True
    else:
        return False

# Test the function with sample inputs
time_inputs = ["10pm", "11 am", "11:00am", "10:00 pm", "12:30PM", "12", "8", "5pm", "3:45"]
for time_input in time_inputs:
    if validate_time_format(time_input):
        print(f"{time_input} - Valid")
    else:
        print(f"{time_input} - Invalid")
