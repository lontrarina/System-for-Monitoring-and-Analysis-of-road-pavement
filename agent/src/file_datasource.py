from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:

    def __init__( self,accelerometer_filename: str,gps_filename: str,) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""

        accelerometer_data = self.accelerometer_file.readline().strip().split(',')
        gps_data = self.gps_file.readline().strip().split(',')

        if '' in gps_data or '' in accelerometer_data:
            self.accelerometer_file.seek(0)
            self.gps_file.seek(0)
            # Пропускаємо перший рядок
            self.accelerometer_file.readline()
            self.gps_file.readline()
            accelerometer_data = self.accelerometer_file.readline().strip().split(',')
            gps_data = self.gps_file.readline().strip().split(',')

        accelerometer = Accelerometer(*[int(value) for value in accelerometer_data])
        gps = Gps(*[float(value) for value in gps_data])

        return AggregatedData(
            accelerometer,
            gps,
            datetime.now(),
            config.USER_ID)


    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        # Пропускаємо перший рядок
        self.accelerometer_file.readline()
        self.gps_file.readline()



    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file:
            self.accelerometer_file.close()
        if self.gps_file:
            self.gps_file.close()