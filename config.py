import argparse

def get_config():
    parser = argparse.ArgumentParser(description="Read from Landis+Gyr E360 and publish to MQTT")

    parser.add_argument("--serial_port", default="/dev/ttyUSB0", help="Serial port for the meter")
    parser.add_argument("--baudrate", type=int, default=115200, help="Baud rate for serial communication")
    parser.add_argument("--bytesize", type=int, default=8, help="Byte size for serial communication")
    parser.add_argument("--parity", default='N', choices=['N', 'E', 'O', 'M', 'S'], help="Parity for serial communication")
    parser.add_argument("--stopbits", type=int, default=1, help="Stop bits for serial communication")
    parser.add_argument("--mqtt_broker", type=str, help="MQTT broker address")
    parser.add_argument("--mqtt_port", type=int, default=1883, help="MQTT broker port")
    parser.add_argument("--mqtt_topic", default="landisgyr_e360", help="MQTT topic")

    return parser.parse_args()