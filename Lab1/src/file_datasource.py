from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
import config

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None
    
    def startReading(self) -> None:
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')

        # Skip header lines
        next(self.accelerometer_file)
        next(self.gps_file)
    
    def stopReading(self) -> None:
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()
    
    def read(self) -> AggregatedData:
        if not self.accelerometer_file or not self.gps_file:
            raise ValueError("Files are not open for reading. Call startReading() first.")

        accelerometer_data = self.accelerometer_file.readline().strip().split(',')
        gps_data = self.gps_file.readline().strip().split(',')
        
        while not gps_data[0]:
            gps_data = self.gps_file.readline().strip().split(',')
        
        accelerometer = Accelerometer(int(accelerometer_data[0]), int(accelerometer_data[1]), int(accelerometer_data[2]))
        gps = Gps(float(gps_data[0]), float(gps_data[1]))
        time = datetime.now()
        
        return AggregatedData(accelerometer, gps, time, config.USER_ID)
