import mpu6050
import time
import json
from datetime import datetime
from supabase import create_client
import supabase

# Create a new Mpu6050 object
mpu6050_sensor = mpu6050.mpu6050(0x68)

# Define calibration parameters
NUM_CALIBRATION_READINGS = 100

# Define offset variables
accel_offset = {"x": 0, "y": 0, "z": 0}
gyro_offset = {"x": 0, "y": 0, "z": 0}

# Define a function to calibrate the sensor
def calibrate_sensor():
    global accel_offset, gyro_offset
    
    # Initialize sum variables
    accel_sum = {"x": 0, "y": 0, "z": 0}
    gyro_sum = {"x": 0, "y": 0, "z": 0}
    
    # Collect calibration data
    for _ in range(NUM_CALIBRATION_READINGS):
        accel_data, gyro_data, _ = read_sensor_data()
        accel_sum["x"] += accel_data["x"]
        accel_sum["y"] += accel_data["y"]
        accel_sum["z"] += accel_data["z"]
        gyro_sum["x"] += gyro_data["x"]
        gyro_sum["y"] += gyro_data["y"]
        gyro_sum["z"] += gyro_data["z"]
        time.sleep(0.01)
    
    # Calculate average offsets
    accel_offset["x"] = accel_sum["x"] / NUM_CALIBRATION_READINGS
    accel_offset["y"] = accel_sum["y"] / NUM_CALIBRATION_READINGS
    accel_offset["z"] = accel_sum["z"] / NUM_CALIBRATION_READINGS
    gyro_offset["x"] = gyro_sum["x"] / NUM_CALIBRATION_READINGS
    gyro_offset["y"] = gyro_sum["y"] / NUM_CALIBRATION_READINGS
    gyro_offset["z"] = gyro_sum["z"] / NUM_CALIBRATION_READINGS

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050_sensor.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050_sensor.get_gyro_data()

    # Read temp
    temperature = mpu6050_sensor.get_temp()

    return accelerometer_data, gyroscope_data, temperature

# Connect to Supabase
supabase_client = create_client("https://ljzrkwoyewivcfhthral.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxqenJrd295ZXdpdmNmaHRocmFsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDA1NzU3NzcsImV4cCI6MjAxNjE1MTc3N30.bSMt5zZF012w-YVjnLTKJO0yAeMonr7VgserYfadoPM")

# Start time
start_time = time.time()

# Calibration
calibrate_sensor()
pos =0
# Start a while loop to continuously read the sensor data
while True:
    # Read the sensor data
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    # Apply calibration offsets
    calibrated_accelerometer = {
        "x": accelerometer_data["x"] - accel_offset["x"],
        "y": accelerometer_data["y"] - accel_offset["y"],
        "z": accelerometer_data["z"] - accel_offset["z"]
    }
    calibrated_gyroscope = {
        "x": gyroscope_data["x"] - gyro_offset["x"],
        "y": gyroscope_data["y"] - gyro_offset["y"],
        "z": gyroscope_data["z"] - gyro_offset["z"]
    }

    # Print the sensor data
    print("Accelerometer data:", calibrated_accelerometer)
    print("Gyroscope data:", calibrated_gyroscope)
    print("Temp:", temperature)

    # Create a dictionary to store data
    data_dict = {
        "pos":pos,
        "x": calibrated_accelerometer["x"],
        "y": calibrated_accelerometer["y"],
        "z": calibrated_accelerometer["z"],
        "temperature": temperature
    }
    pos +=1
    # Convert dictionary to JSON
    json_data = json.dumps(data_dict)

    # Write JSON to a file
    with open("sensor_data.txt", "a") as file:
        file.write(json_data+'\n')

    # Upload JSON to Supabase
#    supabase_client.table("sensor_data").insert([data_dict]).execute()
    print("time: ", time.time()-start_time)
    if pos>=500:
        pos = 0 
        with open("sensor_data.txt", "r") as file:
        # Read all lines from the file
            lines = file.readlines()

            # Initialize an empty list to store the JSON data
            json_data = []

            # Process each line
            for line in lines:
                # Remove trailing newline character
                line = line.strip()

                # Convert the line to a dictionary
                data_dict = json.loads(line)

                # Append the dictionary to the list
                json_data.append(data_dict)
        
            
        print(" ")
        print("AAA",json_data)
        json_data = json.dumps(json_data)
            # Reset start time
        data, count = supabase_client.table('Raw').insert({
        "measurement": json_data,
        "average_temperature": temperature,
        "sampling_frequency": "1000"}).execute()
        with open("sensor_data.txt", "w") as file:
            file.write("")
    start_time = time.time()

