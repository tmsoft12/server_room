# Server Room Security System

This project monitors various security sensors (temperature, humidity, PIR, door, fire) in a server room and sends SMS alerts to authorized personnel when specific events occur. The system is developed using the ESP8266 microcontroller and Python.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features

- Monitoring temperature and humidity sensors
- Motion detection with PIR sensor
- Monitoring door open/close status with door sensor
- Fire detection with fire sensor
- Collecting and processing sensor data using ESP8266
- Sending SMS alerts via USB GSM modem when specific events occur
- Admin interface for checking sensor statuses and changing the authorized phone number

## Requirements

- ESP8266 microcontroller
- Temperature and humidity sensors (DHT11 or DHT22)
- PIR sensor
- Door sensor (magnetic contact)
- Fire sensor
- USB GSM modem
- Python 3.x
- Required Python libraries (specified below)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tmsoft12/server_room.git
    cd server_room
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the ESP8266 and connect the sensors. You can find the ESP8266 code in the `esp8266` folder.

4. Start the system by running the Python script:
    ```bash
    python main.py
    ```

## Usage

- Once the system is started, it will monitor the sensor data and send SMS alerts to the authorized person when specific events occur.
- You can access the admin interface to check the status of the sensors and change the authorized phone number.

## Contributing

If you want to contribute, please open an issue first. Contributions to improve the project are always welcome.

1. Fork the repository (https://github.com/tmsoft12/server_room/fork)
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a new Pull Request
