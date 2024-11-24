# Weather-Predictor
A Python-based application that collects weather data using various sensors, logs this data into CSV files, provides weather predictions, and displays the results using a graphical user interface (GUI).

## Features
- **Data Collection**: Real-time weather data collection using multiple sensor classes (e.g., Humidity, Temperature, Rainfall, Wind Speed).
- **Data Logging**: Logs weather data into CSV files for persistent storage and historical analysis.
- **Weather Prediction**: Provides predictions using statistical analysis of collected data.
- **Interactive GUI**: User-friendly interface for viewing weather data, searching past records, and managing updates.


## Key Concepts

### Classes and Methods
- **Sensors**:
  - Abstract base class defining a common interface for all sensor types.
  - Derived classes implement specific data collection logic (e.g., `TemperatureSensor`, `HumiditySensor`).
- **Data Logger**:
  - Handles logging, searching, and updating weather data stored in CSV files.
- **Weather Predictor**:
  - Predicts weather conditions based on historical data.
- **Weather Station GUI**:
  - Manages user interaction, data display, and error handling.

### Inheritance and Polymorphism
- Sensor classes inherit common attributes and methods from the `Sensor` base class, promoting code reuse.
- Polymorphic behavior allows the system to interact with sensors dynamically without needing specific knowledge of sensor types.

### Exception and File Handling
- Handles file-related errors (e.g., missing data files) gracefully to ensure uninterrupted execution.
- Logs data in CSV format, allowing for easy data manipulation and retrieval.
