# lge360MQTT

Effortlessly connect and monitor your Landis+Gyr E360 Energy Meter using this Python library. Utilizing the H1 serial port to read telegrams and Home Assistant MQTT Discovery, integrate your energy meter seamlessly with Home Assistant and enjoy insight into your energy bill.

## Features

- **Monitor OBIS codes:** Read the OBIS codes provided by the H1 serial port, and publish to MQTT.
- **Handle unidentified OBIS codes:** Log the unidentified OBIS codes to stdout.
- **Home Assistant Energy Dashboard:** Provide the datapoints Home Assistant's Energy Dashboard needs to visualize energy consumption.

## Installation

To install the library, clone the repository and create a symbolic link to your Python library directory:

```sh
git clone https://github.com/slespersen/lge360MQTT.git
ln -s $(pwd)/lge360MQTT /path/to/your/python/site-packages/lge360MQTT
```

### Usage

`main.py` is provided for running the library. Below are the arguments it accepts:

### Arguments

- `--serial_port`: (Optional) Serial port for the meter. Default is: /dev/ttyUSB0
- `--baudrate`: (Optional) Baud rate for serial communication. Default is: 115200.
- `--bytesize`: (Optional) Byte size for serial communication. Default is: 8.
- `--parity`: (Optional) Parity for serial communication. Default is: N.
- `--stopbits`: (Optional) Stop bits for serial communication. Default is: 1.
- `--mqtt_broker`: (Required) MQTT broker address.
- `--mqtt_port`: (Optional) MQTT broker port. Default is: 1883.
- `--mqtt_topic`: (Optional) MQTT topic. Default is: landisgyr_e360.

### Example

Here’s a quick example to get you started:

sh

```
python main.py --mqtt_broker 169.254.1.45 --mqtt_port 1883
```

### Systemd Service File
A systemd service file is provided to enable the script to be run as a service.

Remember to update the variables, according to your setup.

## Inspiration, Resources & Acknowledgements

-   [Greenpower Denmark](https://greenpowerdenmark.dk/): [Branchestandard for fjernaflæste elmåleres eksterne port](https://greenpowerdenmark.dk/files/media/document/Branchestandard-for-fjernaflaeste-elmaaleres-eksterne-port.pdf)

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Support

For any questions or issues, please open an issue.