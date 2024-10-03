import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, 
                            QLabel, QLineEdit, QPushButton, 
                            QVBoxLayout, QHBoxLayout)

from PyQt5.QtCore import QTimer, QTime, Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather Data", self)
        self.temperature_label = QLabel(self)  
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)   
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        # set the layouts
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_name")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }                 
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segeo UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
            """)
        
        self.get_weather_button.clicked.connect(self.get_weather)
        
        
    def get_weather(self):
        api_key = "72636e0ce773d830723a4ab8b6d21018"
        #get input text
        city = self.city_input.text()  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"  
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            # convert to json
            data = response.json()
     
            if data["cod"] == 200:
                self.display_weather(data)
       
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                    
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                    
                case 403:
                    self.display_error("Forbidden:\nAcess Denied")
                    
                case 404:
                    self.display_error("Error Not Found:\nCity not found")
                    
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                    
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                    
                case 503:
                    self.display_error("Service Unavailable:\nServer down, try again after some minutes")
                
                case 504:
                    self.display_error("Gateway Timeout:\nNo response fro server")
                 
                case _:
                    self.display_error("HTTP error occured:\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connnection Error: \n Check your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: \n Request time out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects: \n Check the URL")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request_error:\n{req_error}")
    
    
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px; padding-top: 10px")
        self.temperature_label.setText(message)
    
    
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 60px; padding-top: 10px")
        temp_k = data["main"]["temp"]
        # convert to celcius
        temp_c = temp_k - 273.1
        # convert to faraheit (F)
        temp_f = (temp_k * 9/5) - 459.67
        weather_description = data["weather"][0]["description"]
        # get weather id
        weather_id = data["weather"][0]["id"]
        
        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)
        
    
    @staticmethod
    def get_weather_emoji(weather_id):
       
        if 200 <= weather_id <= 232:
            # hold win-key + ;
            return "⛈"
        elif 300 <= weather_id <= 321:
            # hold win-key + ;
            return "🌦"
        elif 500 <= weather_id <= 521:
            # hold win-key + ;
            return "🌧"
        elif 600 <= weather_id <= 622:
            # hold win-key + ;
            return "❄"
        elif 701 <= weather_id <= 741:
           # hold win-key + ;
           return "🌫"
        elif weather_id == 752:
           # hold win-key + ;
           return "🌋"
        elif weather_id == 771:
           # hold win-key + ;
           return "💨"
        elif weather_id == 781:
           # hold win-key + ;
           return "🌪"
        elif weather_id == 800:
           # hold win-key + ;
           return "🌞"
        elif weather_id == 804:
           # hold win-key + ;
           return "☁"
        else:
            return ""
           
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = WeatherApp()
    stopwatch.show()
    sys.exit(app.exec_())






#weather_key = 72636e0ce773d830723a4ab8b6d21018
