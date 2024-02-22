# Python Imports
import os
import json
import yaml
import socket
import subprocess

# Local Import
from network_call.logging import logger

# Constants
UDP_IP = "0.0.0.0"  # Default ( listen to any IPv4 in the same Network)
UDP_PORT = 12345    # Fixed Port

socket.gethostname()


class UDPSocket:
    def __init__(self) -> None:

        # Default Values
        self.machine_id = None
        self.wifi_ip = None
        self.ethernet_ip = None

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP address and port
        self.sock.bind((UDP_IP, UDP_PORT))

        logger.info("UDP server is running...")
        self.ethernet_ip = self.get_ethernet_ip()
        self.wifi_ip = self.get_wifi_ip()
        self.get_machine_id()

    def get_ethernet_ip(self):
        """
        Get ip of ethernet connection
        """
        try:
            # Get Available Network Interfaces
            result = subprocess.run(
                ["ls", "/sys/class/net"], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            network_interfaces = result.split("\n")[:-1]

            for interface in network_interfaces:
                command = "ifconfig %s | grep 'inet' | cut -d: -f2 | awk '{print $2}'" % (
                    interface
                )
                # Need to remove last 2 \n s
                ip_address = os.popen(command).read()[:-2]

                if ip_address != "" and interface.startswith("e"):
                    return ip_address.strip()

        except Exception as ex:
            logger.error(
                "ppmt_nav_common: Exception in get_ethernet_ip: " + str(ex))

    def get_wifi_ip(self):
        """
        Get ip of wifi connection
        """
        try:
            # Get Available Network Interfaces
            result = subprocess.run(
                ["ls", "/sys/class/net"], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            network_interfaces = result.split("\n")[:-1]

            for interface in network_interfaces:
                command = "ifconfig %s | grep 'inet' | cut -d: -f2 | awk '{print $2}'" % (
                    interface
                )
                # Need to remove last 2 \n s
                ip_address = os.popen(command).read()[:-2]

                if ip_address != "" and interface.startswith("w"):
                    return ip_address.strip()

        except Exception as ex:
            logger.error(
                "ppmt_nav_common: Exception in get_wifi_ip: " + str(ex))

    def get_machine_id(self):
        """Get the Machine Id from the robot local storage.
        """
        machine_info_path = os.path.join(
            os.getenv("HOME"), ".machineinfo.yaml")
        try:
            with open(machine_info_path, "r") as file:
                data = yaml.safe_load(file)
                self.machine_id = data.get('MACHINEID', 'Unknown')
        except FileNotFoundError:
            self.get_logger().info(
                f"The file {machine_info_path} does not exist.")
        except Exception as e:
            self.get_logger().error(
                f"Exception while reading the file - {str(e)}")

    def reply(self):
        try:
            response = {
                "machineId": self.machine_id,
                "wifiIp": self.wifi_ip,
                "ethernetIp": self.ethernet_ip
            }

            # Encode the JSON object as a string
            json_string = json.dumps(response)
            encoded_json = json_string.encode()
            return encoded_json
        except Exception as e:
            logger.error(f"Unable to Reply!! - {str(e)}")
