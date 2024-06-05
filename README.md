# capstoneHardware

## MPU6050 Sensor Data Logger with Supabase Integration

This Python script enables the collection and logging of data from an MPU6050 sensor while also integrating with the Supabase database for storage. Below is an overview of its functionality:

1. **Installation**:
   - Ensure you have Python installed on your system.
   - Install the required dependencies using `pip`:
     ```
     pip install mpu6050 supabase-py
     ```

2. **Usage**:
   - Import the necessary modules at the beginning of your Python script:
     ```python
     import mpu6050
     import time
     import json
     from supabase import create_client
     ```

   - Initialize the MPU6050 sensor object with its specific address:
     ```python
     mpu6050_sensor = mpu6050.mpu6050(0x68)
     ```

   - Establish a connection to your Supabase database by providing the URL and API key:
     ```python
     supabase_client = create_client("YOUR_SUPABASE_URL", "YOUR_SUPABASE_API_KEY")
     ```

   - Run the script to start collecting data from the sensor and storing it locally in a file named "sensor_data.txt". Once the specified number of readings is reached, the data is uploaded to the Supabase database:
     ```bash
     python sensor_data_logger.py
     ```

3. **Functionality**:
   - **Calibration**: The script includes a function to calibrate the sensor by averaging a set number of readings. This ensures accurate data collection by compensating for sensor drift.
   - **Data Collection**: It continuously reads sensor data, applies calibration offsets, and logs it to a local file in JSON format. Additionally, it uploads batches of collected data to the Supabase database at specified intervals.
   - **Supabase Integration**: Data collected from the sensor is uploaded to a Supabase database table named "Raw" for further analysis and storage.

4. **Customization**:
   - Adjust the `NUM_CALIBRATION_READINGS` variable to change the number of readings used for calibration.
   - Modify the Supabase URL and API key to connect to your specific Supabase project.
   - Customize the script according to your specific sensor setup and data logging requirements.

5. **Dependencies**:
   - mpu6050: Python library for interfacing with the MPU6050 sensor.
   - supabase-py: Python client library for interacting with the Supabase database.
