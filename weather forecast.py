#making a weather forecast app :))

#import libraries
import customtkinter as ctk
import requests
import datetime
from tkinter import messagebox #added this back
from PIL import Image

class WeatherForecast(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weather Forecasting App")
        self.geometry("600x780")

        # Set appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        # API key and history file
        self.API_KEY = "86116f47d13a53b6569ae11ebb6c5302"
        self.HISTORY_FILE = "weather_history.txt"
        self.HISTORY_MAX = 5
        self.WEATHER_HISTORY = []
        self.undo_stack = []

        # Mode (light/dark)
        self.current_mode = ['light' if self.day() else "dark"]

        # Load images
        self.sun_img = ctk.CTkImage(Image.open("images/sun.png").resize((100, 100)))
        self.moon_img = ctk.CTkImage(Image.open("images/moon.png").resize((100, 100)))

        # Build UI
        self.build_ui()
        self.load_history()
        self.update_time_theme()
        self.mainloop()

    def build_ui(self):
        self.city_var = ctk.StringVar()
        self.city_entry = ctk.CTkEntry(self, width=300, placeholder_text="Enter city", textvariable=self.city_var)
        self.city_entry.place(x=20, y=20)

        self.searchbtn = ctk.CTkButton(self, text="Search", command=self.fetch_weather)
        self.searchbtn.place(x=340, y=20)

        self.modebtn = ctk.CTkButton(self, text="Toggle Light/Dark", command=self.toggle)
        self.modebtn.place(x=420, y=300)

        self.date_lbl = ctk.CTkLabel(self, text="", font=("Narrow Arial", 18))
        self.date_lbl.place(x=20, y=100)
        self.month_lbl = ctk.CTkLabel(self, text="", font=("Narrow Arial", 16))
        self.month_lbl.place(x=150, y=100)
        self.time_lbl = ctk.CTkLabel(self, text="", font=("Arial", 15))
        self.time_lbl.place(x=20, y=130)

        self.icon_label = ctk.CTkLabel(self, text="")
        self.icon_label.place(x=250, y=170)

        # Weather info labels
        self.citylbl = ctk.CTkLabel(self, text="City", font=("Arial", 18))
        self.countrylbl = ctk.CTkLabel(self, text="Country", font=("Arial", 18))
        self.templbl = ctk.CTkLabel(self, text="Temp...", font=("Arial", 80))
        self.humiditylbl = ctk.CTkLabel(self, text="Humidity...", font=("Arial", 18))
        self.maxtemplbl = ctk.CTkLabel(self, text="Max Temp...", font=("Arial", 18))
        self.mintemplbl = ctk.CTkLabel(self, text="Min Temp...", font=("Arial", 18))
        self.latlbl = ctk.CTkLabel(self, text="Lat: ...", font=("Arial", 18))
        self.longlbl = ctk.CTkLabel(self, text="Lon: ...", font=("Arial", 18))
        self.notelbl = ctk.CTkLabel(self, text="All temperatures in °C", font=("Arial", 14))

        self.citylbl.place(x=20, y=70)
        self.countrylbl.place(x=160, y=70)
        self.templbl.place(x=30, y=270)
        self.humiditylbl.place(x=20, y=420)
        self.maxtemplbl.place(x=20, y=450)
        self.mintemplbl.place(x=20, y=480)
        self.latlbl.place(x=20, y=520)
        self.longlbl.place(x=160, y=520)
        self.notelbl.place(x=20, y=550)

        # History Frame
        self.hist_frame = ctk.CTkFrame(self, width=250, height=180)
        self.hist_frame.place(x=320, y=80)
        ctk.CTkLabel(self.hist_frame, text="Search History", font=("Arial", 14)).pack(pady=5)
        self.hist_box = ctk.CTkTextbox(self.hist_frame, width=220, height=100)
        self.hist_box.pack()

        # Clear and Undo Buttons
        self.clearbtn = ctk.CTkButton(self.hist_frame, text="Clear History", command=self.clear_history)
        self.clearbtn.pack(pady=3)
        self.undobtn = ctk.CTkButton(self.hist_frame, text="Undo", command=self.undo_history)
        self.undobtn.pack(pady=2)

    def load_history(self):
        try:
            with open(self.HISTORY_FILE, "r") as f:
                lines = f.read().splitlines()
                self.WEATHER_HISTORY = lines[:self.HISTORY_MAX]
                self.refresh_history_box()
        except FileNotFoundError:
            self.WEATHER_HISTORY = []

    def refresh_history_box(self):
        self.hist_box.delete("0.0", "end")
        for item in self.WEATHER_HISTORY:
            self.hist_box.insert("end", item + "\n")

    def save_history(self):
        try:
            with open(self.HISTORY_FILE, "w") as f:
                f.write("\n".join(self.WEATHER_HISTORY))
        except Exception as e:
            print(f"Error saving history: {e}")
    
    #reminder to not use self.day
    def day(self):
        hour = datetime.datetime.now().hour
        return 7 <= hour <= 18

    def update_time_theme(self):
        now = datetime.datetime.now()
        self.date_lbl.configure(text=now.strftime("%A"))
        self.month_lbl.configure(text=now.strftime("%d %B"))
        self.time_lbl.configure(text=now.strftime("%I:%M %p"))

        desired_mode = "light" if self.day() else "dark"
        if desired_mode != self.current_mode[0]:
            ctk.set_appearance_mode(desired_mode)
            self.current_mode[0] = desired_mode
        self.update_icon()

        self.after(60000, self.update_time_theme)

    def toggle(self):
        new_mode = "dark" if self.current_mode[0] == "light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.current_mode[0] = new_mode
        self.update_icon()

    def update_icon(self):
        icon = self.sun_img if self.current_mode[0] == "light" else self.moon_img
        self.icon_label.configure(image=icon)

    def update_history(self, entry):
        if entry in self.WEATHER_HISTORY:
            self.WEATHER_HISTORY.remove(entry)
        self.undo_stack.append(self.WEATHER_HISTORY[:])  # Save current state for undo
        self.WEATHER_HISTORY.insert(0, entry)
        if len(self.WEATHER_HISTORY) > self.HISTORY_MAX:
            self.WEATHER_HISTORY.pop()
        self.refresh_history_box()
        self.save_history()

    def undo_history(self):
        if self.undo_stack:
            self.WEATHER_HISTORY = self.undo_stack.pop()
            self.refresh_history_box()
            self.save_history()

    def clear_history(self):
        if messagebox.askyesno("Confirm", "Clear all weather history?"):
            self.undo_stack.append(self.WEATHER_HISTORY[:])
            self.WEATHER_HISTORY = []
            self.refresh_history_box()
            self.save_history()
    
    #get weather 
    def fetch_weather(self):
        city = self.city_var.get().strip()
        if not city:
            return

        try:
            res = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={self.API_KEY}"
            )
            res.raise_for_status()
            data = res.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            country = data["sys"]["country"]
            city_name = data["name"]

            self.templbl.configure(text=f"{temp}°C")
            self.humiditylbl.configure(text=f"Humidity: {humidity}%")
            self.maxtemplbl.configure(text=f"Max: {temp_max}°C")
            self.mintemplbl.configure(text=f"Min: {temp_min}°C")
            self.latlbl.configure(text=f"Lat: {lat}")
            self.longlbl.configure(text=f"Lon: {lon}")
            self.countrylbl.configure(text=f"{country}")
            self.citylbl.configure(text=f"{city_name}")

            self.update_history(f"{city_name}: {temp}°C")

        except requests.RequestException:
            self.templbl.configure(text="Error")

# Run App
if __name__ == "__main__":
    WeatherForecast()