import re
import serial
import logging

class MeterReader:
    device_pattern = r'^/LGF5E360$'
    obis_pattern = r'(\d+-\d+:\d+\.\d+\.\d+)\(([\d.]+|\w+)\*?(\w+)?\)'

    def __init__(self, config, logger):
        self.logger = logger
        self.serial_port = config.serial_port
        self.baudrate = config.baudrate
        self.bytesize = config.bytesize
        self.parity = config.parity
        self.stopbits = config.stopbits
        self.timeout = 1
        self.ser = serial.Serial(
            port=self.serial_port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout
        )
        
        # These mappings are for Danish meters - might work for others
        # In general it is advised for Danish meters, to not expose their Meter ID
        # Source: https://greenpowerdenmark.dk/files/media/document/Branchestandard-for-fjernaflaeste-elmaaleres-eksterne-port.pdf
        self.label_map = {
            '0-0:1.0.0': {'name': 'datetime', 'unit': ''},
            '1-0:1.8.0': {'name': 'total_active_energy_fwd', 'unit': 'kWh'},
            '1-0:2.8.0': {'name': 'total_active_energy_rev', 'unit': 'kWh'},
            '1-0:3.8.0': {'name': 'reactive_energy_fwd', 'unit': 'kVArh'},
            '1-0:4.8.0': {'name': 'rective_energy_rev', 'unit': 'kVArh'},
            '1-0:1.7.0': {'name': 'active_power_fwd', 'unit': 'kW'},
            '1-0:2.7.0': {'name': 'active_power_rev', 'unit': 'kW'},
            '1-0:3.7.0': {'name': 'reactive_power_fwd', 'unit': 'kVAr'},
            '1-0:4.7.0': {'name': 'reactive_power_rev', 'unit': 'kVAr'},
            '1-0:21.7.0': {'name': 'active_power_l1_fwd', 'unit': 'kW'},
            '1-0:22.7.0': {'name': 'active_power_l1_rev', 'unit': 'kW'},
            '1-0:41.7.0': {'name': 'active_power_l2_fwd', 'unit': 'kW'},
            '1-0:42.7.0': {'name': 'active_power_l2_rev', 'unit': 'kW'},
            '1-0:61.7.0': {'name': 'active_power_l3_fwd', 'unit': 'kW'},
            '1-0:62.7.0': {'name': 'active_power_l3_rev', 'unit': 'kW'},
            '1-0:23.7.0': {'name': 'reactive_power_l1_imp', 'unit': 'kVAr'},
            '1-0:24.7.0': {'name': 'reactive_power_l1_exp', 'unit': 'kVAr'},
            '1-0:43.7.0': {'name': 'reactive_power_l2_imp', 'unit': 'kVAr'},
            '1-0:44.7.0': {'name': 'reactive_power_l2_exp', 'unit': 'kVAr'},
            '1-0:63.7.0': {'name': 'reactive_power_l3_imp', 'unit': 'kVAr'},
            '1-0:64.7.0': {'name': 'reactive_power_l3_exp', 'unit': 'kVAr'},
            '1-0:32.7.0': {'name': 'voltage_rms_l1', 'unit': 'V'},
            '1-0:52.7.0': {'name': 'voltage_rms_l2', 'unit': 'V'},
            '1-0:72.7.0': {'name': 'voltage_rms_l3', 'unit': 'V'},
            '1-0:31.7.0': {'name': 'current_rms_l1', 'unit': 'A'},
            '1-0:51.7.0': {'name': 'current_rms_l2', 'unit': 'A'},
            '1-0:71.7.0': {'name': 'current_rms_l3', 'unit': 'A'}
        }

    def read(self):
        if self.ser.in_waiting > 0:
            raw_data = self.ser.readline().decode('utf-8').strip()
            self.logger.debug(f"Raw message: {raw_data}")
            if re.search(self.device_pattern, raw_data):
                raw_data = self.ser.read_until(b'!').decode('utf-8').strip()
                self.logger.debug(f"Full telegram: {raw_data}")
                data = self.parse_data(raw_data)
                self.logger.info(f"New reading: {data}")
                self.log_unhandled_obis_codes(raw_data)
                return data
        return None

    def parse_data(self, data):
        obis_data = re.findall(self.obis_pattern, data)
        readings = {}
        for match in obis_data:
            obis_code = match[0]
            value = match[1]
            unit = match[2] if len(match) > 2 else None
            label = self.label_map.get(obis_code, {'name': obis_code, 'unit': unit})['name']
            if float(value) != 0.0 or "alt" not in label:
                readings[label] = {"value": value, "unit": unit}
        return readings

    def log_unhandled_obis_codes(self, raw_data):
        obis_codes = re.findall(self.obis_pattern, raw_data)
        received_obis_codes = set([code[0] for code in obis_codes])
        handled_obis_codes = set(self.label_map.keys())
        unhandled_obis_codes = received_obis_codes - handled_obis_codes

        if unhandled_obis_codes:
            self.logger.warning(f"Unhandled OBIS codes: {unhandled_obis_codes}")

    def close(self):
        self.ser.close()