from abc import ABC, abstractmethod
import random
import datetime
import csv
import tkinter as tk
from tkinter import ttk 

class Sensor(ABC):
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type

    @abstractmethod
    def get_data(self):
        pass 

    def update(self, current_value):
        var = random.uniform(-5, 5)  
        new_val = current_value + var
        return round(new_val, 2)

class HumiditySensor(Sensor):
    def __init__(self):
        super().__init__("humidity")

    def get_data(self):
        return random.randint(0, 100)

class TemperatureSensor(Sensor):
    def __init__(self):
        super().__init__("temperature")

    def get_data(self):
        return round(random.uniform(-10, 40), 2)

class RainfallSensor(Sensor):
    def __init__(self):
        super().__init__("rainfall")

    def get_data(self):
        return round(random.uniform(0, 50), 2)

class WindSpeedSensor(Sensor):
    def __init__(self):
        super().__init__("wind_speed")

    def get_data(self):
        return round(random.uniform(0, 100), 2)

class Sensors:
    def __init__(self):
        self.sensors = [
            HumiditySensor(),
            TemperatureSensor(),
            RainfallSensor(),
            WindSpeedSensor()
        ]

    def get_weather(self):
        data = {}
        for sensor in self.sensors:
            data[sensor.sensor_type] = sensor.get_data()
        return data

class DataLogger:
    def __init__(self, filename="weather_data.csv"):
        self.filename = filename

    def log_data(self, data, location):
        try:
            with open(self.filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                if any(reader):
                    write_headers = False
                else:
                    write_headers = True
        except FileNotFoundError:
            write_headers = True

        with open(self.filename, "a", newline="") as csvfile:
            fieldnames = ["timestamp", "location", "humidity", "temperature", "rainfall", "wind_speed"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if write_headers:
                writer.writeheader()

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow({"timestamp": timestamp,"location": location,"humidity": data['humidity'],"temperature": data['temperature'],"rainfall": data['rainfall'],"wind_speed": data['wind_speed']})

    def search_data(self, location):
        results = []
        try:
            with open(self.filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row["location"].lower() == location.lower():
                        results.append(row)
        except FileNotFoundError:
            print(f"No data found for {location}.")
            return None
        return results[-1]

    def update(self, location, sensors):
        updated_data = {}
        existing_data = self.search_data(location)

        if existing_data:
            updated_data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_data["location"] = location
            for sensor in sensors.sensors:
                sensor_type = sensor.sensor_type
                current_value = float(existing_data[sensor_type])
                updated_data[sensor_type] = sensor.update(current_value)
            data_logger.log_data(updated_data, location)
            return updated_data

        else:
            print(f"No data found for {location}.")
            return None

    def get_latest_data_for_all_cities(self):
        city_data = {}
        try:
            with open(self.filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    city = row["location"].lower()
                    city_data[city] = row 
        except FileNotFoundError:
            print(f"No data found in {self.filename}")
        return city_data

class predictor:
    def predict(self, data):
        if data["temperature"] > 25 and data["humidity"] > 60:
            return "It will likely be hot and humid."
        elif data["rainfall"] > 10:
            return "Expect heavy rain."
        elif data["wind_speed"] > 30:
            return "It will be windy."
        else:
            return "Pleasant weather expected."

class WeatherStationGUI:
    def __init__(self, master, sensors, data_logger, predictor):
        self.master = master
        master.title("Weather Station")
        self.sensors = sensors
        self.data_logger = data_logger
        self.predictor = predictor

        self.location_label = ttk.Label(master, text="Location:")
        self.location_label.grid(row=0, column=0, padx=5, pady=5)
        self.location_entry = ttk.Entry(master)
        self.location_entry.grid(row=0, column=1, padx=5, pady=5)

        self.get_data_button = ttk.Button(master, text="Get Weather Data", command=self.get_weather)
        self.get_data_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.search_button = ttk.Button(master, text="Search Data", command=self.search_data)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.update_button = ttk.Button(master, text="Update Data", command=self.update)
        self.update_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.all_cities_button = ttk.Button(master, text="Get All Cities Data", command=self.get_all_cities_data)
        self.all_cities_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.output_text = tk.Text(master, wrap=tk.WORD, height=15, width=50)
        self.output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def get_weather(self):
        location = self.location_entry.get()
        if location:
            weather_data = self.sensors.get_weather()
            weather_data["location"] = location
            self.display_data(weather_data, "Current Weather Data:")
            self.data_logger.log_data(weather_data, location)
            prediction = self.predictor.predict(weather_data)
            self.output_text.insert(tk.END, f"\nPrediction: {prediction}")
        else:
            self.show_error("Please enter a location.")

    def search_data(self):
        location = self.location_entry.get()
        if location:
            results = self.data_logger.search_data(location)
            if results:
                self.display_data(results, f"Latest data for {location}:")
            else:
                self.show_error(f"No data found for {location}.")
        else:
            self.show_error("Please enter a location.")

    def update(self):
        location = self.location_entry.get()
        if location:
            updated_data = self.data_logger.update(location, self.sensors)
            if updated_data:
                self.display_data(updated_data, f"Updated data for {location}:")
            else:
                self.show_error(f"No data found for {location} to update.")
        else:
            self.show_error("Please enter a location.")

    def get_all_cities_data(self):
        city_data = self.data_logger.get_latest_data_for_all_cities()
        if city_data:
            for city, data in city_data.items():
                self.output_text.insert(tk.END, f"\nLatest weather data for {city.capitalize()}:\n")
                for key, value in data.items():
                    self.output_text.insert(tk.END, f"  {key}: {value}\n")
        else:
            self.show_error("No data found for any city.")

    def display_data(self, data, title):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"{title}\n")
        for key, value in data.items():
            if key != "location":
                self.output_text.insert(tk.END, f"{key}: {value}\n")

    def show_error(self, message):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Error: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    sensors = Sensors()
    data_logger = DataLogger()
    predictor = predictor()
    app = WeatherStationGUI(root, sensors, data_logger, predictor)
    root.mainloop()