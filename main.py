import time
import sys
import logging
from config import get_config
from meter_reader import MeterReader
from mqtt_publisher import MQTTPublisher

def main():
    config = get_config()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger('lge360MQTT')

    # Set up MQTT publisher
    mqtt_publisher = MQTTPublisher(config, logger)

    # Set up meter reader
    meter_reader = MeterReader(config, logger)

    try:
        while True:
            data = meter_reader.read()
            if data:
                mqtt_publisher.publish(data)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Disconnected by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        meter_reader.close()
        mqtt_publisher.disconnect()
        logger.info("Disconnected and cleaned up resources")

if __name__ == "__main__":
    main()