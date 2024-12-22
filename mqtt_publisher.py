import json
import paho.mqtt.client as mqtt
import logging

class MQTTPublisher:
    def __init__(self, config, logger):
        self.logger = logger
        self.client = mqtt.Client()
        self.mqtt_broker = config.mqtt_broker
        self.mqtt_port = config.mqtt_port
        self.base_topic = config.mqtt_topic

        self.device_name = "landisgyr_e360"
        self.device_id = "landisgyr_e360_meter"

        self.client.on_connect = self.on_connect
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info(f"Connected with result code {rc}")
        
        # Publish discovery messages
        self.publish_discovery_messages()
        
        # Publish online state
        self.publish_availability('online')

    def publish_discovery_messages(self):
        discovery_prefix = "homeassistant/sensor/landisgyr_e360"

        sensors = [
            {"name": "Total Active Energy Import", "unique_id": "total_active_energy_fwd", "unit_of_measurement": "kWh", "icon": "mdi:flash", "state_class": "total_increasing", "device_class": "energy"},
            {"name": "Total Active Energy Export", "unique_id": "total_active_energy_rev", "unit_of_measurement": "kWh", "icon": "mdi:flash", "state_class": "total_increasing", "device_class": "energy"},
            {"name": "Total Reactive Energy Import", "unique_id": "reactive_energy_fwd", "unit_of_measurement": "varh", "icon": "mdi:flash", "state_class": "total_increasing", "device_class": "energy"},
            {"name": "Total Reactive Energy Export", "unique_id": "rective_energy_rev", "unit_of_measurement": "varh", "icon": "mdi:flash", "state_class": "total_increasing", "device_class": "energy"},
            {"name": "Active Power Import", "unique_id": "active_power_fwd", "unit_of_measurement": "kW", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Active Power Export", "unique_id": "active_power_rev", "unit_of_measurement": "kW", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Active Power L1", "unique_id": "active_power_l1_fwd", "unit_of_measurement": "kW", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Active Power L2", "unique_id": "active_power_l2_fwd", "unit_of_measurement": "kW", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Active Power L3", "unique_id": "active_power_l3_fwd", "unit_of_measurement": "kW", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Reactive Power L1", "unique_id": "reactive_power_l1_imp", "unit_of_measurement": "var", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Reactive Power L2", "unique_id": "reactive_power_l2_imp", "unit_of_measurement": "var", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Reactive Power L3", "unique_id": "reactive_power_l3_imp", "unit_of_measurement": "var", "icon": "mdi:flash", "state_class": "measurement", "device_class": "power"},
            {"name": "Voltage L1", "unique_id": "voltage_rms_l1", "unit_of_measurement": "V", "icon": "mdi:flash", "state_class": "measurement", "device_class": "voltage"},
            {"name": "Voltage L2", "unique_id": "voltage_rms_l2", "unit_of_measurement": "V", "icon": "mdi:flash", "state_class": "measurement", "device_class": "voltage"},
            {"name": "Voltage L3", "unique_id": "voltage_rms_l3", "unit_of_measurement": "V", "icon": "mdi:flash", "state_class": "measurement", "device_class": "voltage"},
            {"name": "Current L1", "unique_id": "current_rms_l1", "unit_of_measurement": "A", "icon": "mdi:flash", "state_class": "measurement", "device_class": "current"},
            {"name": "Current L2", "unique_id": "current_rms_l2", "unit_of_measurement": "A", "icon": "mdi:flash", "state_class": "measurement", "device_class": "current"},
            {"name": "Current L3", "unique_id": "current_rms_l3", "unit_of_measurement": "A", "icon": "mdi:flash", "state_class": "measurement", "device_class": "current"}
        ]

        for sensor in sensors:
            payload = {
                "name": sensor['name'],
                "state_topic": f"{self.base_topic}/state",
                "unique_id": f"{self.device_id}_{sensor['unique_id']}",
                "unit_of_measurement": sensor["unit_of_measurement"],
                "availability_topic": f"{self.base_topic}/availability",
                "device": {
                    "identifiers": [self.device_id],
                    "name": "Landis+Gyr E360",
                    "model": "E360",
                    "manufacturer": "Landis+Gyr"
                },
                "icon": sensor["icon"],
                "value_template": f"{{{{ value_json.{sensor['unique_id']} }}}}",
                "state_class": sensor["state_class"],
                "device_class": sensor["device_class"]
            }
            topic = f"{discovery_prefix}/{sensor['unique_id']}/config"
            self.client.publish(topic, json.dumps(payload), retain=True)

    def publish(self, data):
        json_message = json.dumps({key: value["value"] for key, value in data.items()})
        self.client.publish(f"{self.base_topic}/state", json_message)

    def publish_availability(self, state):
        self.client.publish(f"{self.base_topic}/availability", state, 0, True)

    def disconnect(self):
        # Publish offline state
        self.publish_availability('offline')
        
        # Stop loop
        self.client.loop_stop()
        
        # Disconnect MQTT
        self.client.disconnect()