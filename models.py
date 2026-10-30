from flask import Flask, redirect, session, request, render_template, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
import os
from flask_mysqldb import MySQL, MySQLdb
from flask import jsonify
import pandas as pd
import numpy as np
import pickle as pkl

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html',user="amruta")


if __name__ == '__main__':
    app.run(debug=True)  # Run the app with debug mode enabled




# ,Unnamed: 0,name,price,rating,wifi,gps,voice_calling,touch,ram_gb,water_resistance,dust_proof,heart_rate_monitor,blood_pressure_monitor,step_count,blood_oxygen,alarm_clock,stopwatch,timer

@app.route("/smart-watch-price")
def SmartWatchPrice():
    dataset = pd.read_csv("smartwatchData.csv")
    name = sorted(dataset["name"].unique())
    rating = sorted(dataset["rating"].unique())
    wifi = sorted(dataset["wifi"].unique())
    gps = sorted(dataset["gps"].unique())
    voice_calling = sorted(dataset["voice_calling"].unique())
    touch = sorted(dataset["touch"].unique())
    ram_gb = sorted(dataset["ram_gb"].unique())
    water_resistance = sorted(dataset["water_resistance"].unique())
    dust_proof = sorted(dataset["dust_proof"].unique())
    heart_rate_monitor = sorted(dataset["heart_rate_monitor"].unique())
    blood_pressure_monitor = sorted(dataset["blood_pressure_monitor"].unique())
    step_count = sorted(dataset["step_count"].unique())
    blood_oxygen = sorted(dataset["blood_oxygen"].unique())
    alarm_clock = sorted(dataset["alarm_clock"].unique())
    stopwatch = sorted(dataset["stopwatch"].unique())
    timer = sorted(dataset["timer"].unique())
    return render_template("smartWatch.html",name=name,rating=rating,wifi=wifi,gps=gps,voice_calling=voice_calling,touch=touch,ram_gb=ram_gb,water_resistance=water_resistance,dust_proof=dust_proof,heart_rate_monitor=heart_rate_monitor,step_count=step_count,blood_oxygen=blood_oxygen,alarm_clock=alarm_clock,stopwatch=stopwatch,timer=timer,blood_pressure_monitor=blood_pressure_monitor)

@app.route("/smartwatch-price-result")
def SmartWatchPriceResult():
    # Get query parameters and convert to correct data types
    name = request.args.get("name", "Unknown")  # Default to 'Unknown' if missing
    rating = float(request.args.get("rating", 5))  # Default rating is 5
    wifi = int(request.args.get("wifi", 0))  # Convert to integer
    gps = int(request.args.get("gps", 0))
    voice_calling = int(request.args.get("voice_calling", 0))
    touch = int(request.args.get("touch", 0))
    ram_gb = int(request.args.get("ram_gb", 0))
    water_resistance = int(request.args.get("water_resistance", 0))
    dust_proof = int(request.args.get("dust_proof", 0))
    heart_rate_monitor = int(request.args.get("heart_rate_monitor", 0))
    blood_pressure_monitor = int(request.args.get("blood_pressure_monitor", 0))
    step_count = int(request.args.get("step_count", 0))
    blood_oxygen = int(request.args.get("blood_oxygen", 0))
    alarm_clock = int(request.args.get("alarm_clock", 0))
    stopwatch = int(request.args.get("stopwatch", 0))
    timer = int(request.args.get("timer", 0))

    # Load trained model
    pipe = pkl.load(open('SmartWatchModel.pkl', 'rb'))
    print("------------------------------------------------------",water_resistance)
    columns = ["name","wifi","gps","voice_calling","touch","ram_gb","water_resistance","dust_proof","heart_rate_monitor","blood_pressure_monitor","step_count","blood_oxygen","alarm_clock","stopwatch","timer"]
    data = np.array([name,wifi,gps,voice_calling,touch,ram_gb,water_resistance,dust_proof,heart_rate_monitor,blood_pressure_monitor,step_count,blood_oxygen,alarm_clock,stopwatch,timer]).reshape(1,15)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    return render_template("result.html", result = result)
@app.route("/tab-price")
def TabPrice():
    dataset=pd.read_csv("TabData.csv")
    name = sorted(dataset["name"].unique())
    processor_brand = sorted(dataset["processor_brand"].unique())
    num_processor = sorted(dataset["num_processor"].unique())
    processor_speed = sorted(dataset["processor_speed"].unique())
    ram = sorted(dataset["ram"].unique())
    memory_inbuilt = sorted(dataset["memory_inbuilt"].unique())
    battery_capacity = sorted(dataset["battery_capacity"].unique())
    resolution_width = sorted(dataset["resolution_width"].unique())
    resolution_height = sorted(dataset["resolution_height"].unique())
    ppi = sorted(dataset["ppi"].unique())
    primary_front_camera = sorted(dataset["primary_front_camera"].unique())
    primary_rear_camera = sorted(dataset["primary_rear_camera"].unique())
    memory_card_upto = sorted(dataset["memory_card_upto"].unique())
    sim = sorted(dataset["sim"].unique())
    is_5G = sorted(dataset["is_5G"].unique())
    return render_template("tab.html", name=name, processor_brand=processor_brand,num_processor=num_processor,processor_speed=processor_speed,ram=ram,battery_capacity=battery_capacity,resolution_width=resolution_width,resolution_height=resolution_height,ppi=ppi,primary_front_camera=primary_front_camera,primary_rear_camera=primary_rear_camera,memory_card_upto=memory_card_upto,sim=sim,is_5G=is_5G,memory_inbuilt=memory_inbuilt)
    
@app.route("/tab-price-result")
def TabPriceResult():
    # name,price,processor_brand,num_processor,processor_speed,ram,memory_inbuilt,battery_capacity,resolution_width,resolution_height,ppi,primary_front_camera,primary_rear_camera,memory_card_upto,sim,is_5G
    # Get query parameters and convert to correct data types
    name = request.args.get("name", "Unknown")  # Default to 'Unknown' if
    processor_brand = request.args.get("processor_brand", "Unknown")
    num_processor = int(request.args.get("num_processor", 0))
    processor_speed = float(request.args.get("processor_speed", 2.0))  # Default
    ram = int(request.args.get("ram", 0))
    memory_inbuilt = int(request.args.get("memory_inbuilt", 0))
    battery_capacity = int(request.args.get("battery_capacity", 0))
    resolution_width = int(request.args.get("resolution_width", 0))
    resolution_height = int(request.args.get("resolution_height", 0))
    ppi = int(request.args.get("ppi", 0))
    primary_front_camera = int(request.args.get("primary_front_camera", 0))
    primary_rear_camera = int(request.args.get("primary_rear_camera", 0))
    memory_card_upto = request.args.get("memory_card_upto", 0)
    sim = request.args.get("sim", 0)
    is_5G = request.args.get("is_5G", 0)
    # Load trained model
    pipe = pkl.load(open('TabModel.pkl', 'rb'))
    columns = ["name","processor_brand","num_processor","processor_speed","ram","memory_inbuilt","battery_capacity","resolution_width","resolution_height","ppi","primary_front_camera","primary_rear_camera","memory_card_upto","sim","is_5G"]
    data = np.array([name,processor_brand,num_processor,processor_speed,ram,memory_inbuilt,battery_capacity,resolution_width,resolution_height,ppi,primary_front_camera,primary_rear_camera,memory_card_upto,sim,is_5G]).reshape(1, 15)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    return render_template("result.html", result = result)



   