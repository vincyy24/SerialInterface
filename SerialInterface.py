import serial
import serial.tools.list_ports
from typing import Optional

class SerialInterface:
    """
    A class to encapsulate serial port operations.
    """

    def __init__(
        self, port: Optional[str] = None, baudrate: int = 9600, timeout: float = 1.0
    ):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._connection: Optional[serial.Serial] = None

    @property
    def connection(self) -> Optional[serial.Serial]:
        return self._connection

    def list_ports(self) -> list:
        """
        Lists available serial ports.
        """
        try:
            ports = [port.device for port in serial.tools.list_ports.comports()]
            return ports
        except Exception as e:
            print(f"Error listing ports: {e}")
            return []

    def connect(self, port: Optional[str] = None) -> Optional[serial.Serial]:
        """
        Connect to a serial port.
        """
        if port is not None:
            self.port = port
        if self.port is None:
            raise ValueError("No port specified for connection.")
        try:
            self._connection = serial.Serial(
                self.port, self.baudrate, timeout=self.timeout
            )
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to port {self.port}: {e}")
            self._connection = None
        return self._connection

    def disconnect(self) -> None:
        """
        Disconnects from the serial port.
        """
        if self._connection and self._connection.is_open:
            self._connection.close()
            print("Disconnected from port.")

    def read(self, size: int = 1) -> Optional[bytes]:
        """
        Reads 'size' bytes from the serial port.
        """
        if self._connection and self._connection.is_open:
            try:
                data = self._connection.read(size)
                return data
            except Exception as e:
                print(f"Error reading from port: {e}")
                return None
        else:
            print("Connection not open; cannot read.")
            return None

    def write(self, data: bytes) -> None:
        """
        Writes data to the serial port.
        """
        if self._connection and self._connection.is_open:
            try:
                self._connection.write(data)
            except Exception as e:
                print(f"Error writing to port: {e}")
        else:
            print("Connection not open; cannot write.")

