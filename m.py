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


@app.route("/camera-price")
def cameraprice():
   dataset = pd.read_csv("camera.csv")
   

   model = sorted(dataset["model"].unique())
   
   dimensions=sorted(dataset["dimensions"].unique())


   return render_template("camera.html", model = model,dimensions=dimensions)


@app.route("/camerapriceresult")
def camerapriceresult():

   model = request.args.get("model")
   max_resolution = request.args.get("max_resolution")
   low_resolution = request.args.get("low_resolution")
   effective_pixels = request.args.get("effective_pixels")
   zoom_wide = request.args.get("zoom_wide")

   zoom_tele = request.args.get("zoom_tele")
   normal_focus_range = request.args.get("normal_focus_range")
   macro_focus_range = request.args.get("macro_focus_range")
   storage = request.args.get("storage")
   weight = request.args.get("weight")
   dimensions = request.args.get("dimensions")


   pipe = pkl.load(open('cameraModel.pkl', 'rb'))

   columns = ["model","max_resolution","low_resolution","effective_pixels","zoom_wide","zoom_tele","normal_focus_range","macro_focus_range","storage","weight","dimensions"]
   data = np.array([model, max_resolution, low_resolution, effective_pixels , zoom_wide , zoom_tele, normal_focus_range , macro_focus_range, storage, weight, dimensions]).reshape(1, 11)
   myinput = pd.DataFrame(columns = columns, data = data)
   result = pipe.predict(myinput)
   return render_template("result.html", result = result)


@app.route("/laptop-price")
def laptopprice():
    dataset = pd.read_csv("laptop.csv")
    brand = sorted(dataset["brand"].unique())
    os = []
    
    selected_brand = None
    if request.method == "GET":
        selected_brand = request.form.get("brand")  # Get the selected brand from the form
        print(selected_brand)
        if selected_brand:
            # Filter the dataset based on the selected brand
            filtered_data = dataset[dataset["brand"] == selected_brand]
            os = sorted(filtered_data["os"].unique())
            print(os)

    ram_gb = sorted(dataset["ram_gb"].unique())
    ram_type = sorted(dataset["ram_type"].unique())
    ssd = sorted(dataset["ssd"].unique())
    hdd = sorted(dataset["hdd"].unique())
    os = sorted(dataset["os"].unique())
    processor = sorted(dataset["processor"].unique())
    graphic_card_gb = sorted(dataset["graphic_card_gb"].unique())
    weight = sorted(dataset["weight"].unique())
    warranty = sorted(dataset["warranty"].unique())

    return render_template("laptop.html", brand=brand, ram_gb= ram_gb, ram_type= ram_type, ssd= ssd, hdd= hdd, os= os,processor=processor, graphic_card_gb= graphic_card_gb, weight= weight, warranty= warranty, selected_brand=selected_brand)

@app.route("/laptoppriceresult")
def laptoppriceresult():

    brand = request.args.get("brand")
    ram_gb = request.args.get("ram_gb")
    ram_type = request.args.get("ram_type")
    ssd= request.args.get("ssd")
    hdd= request.args.get("hdd")
    os= request.args.get("os")

    processor= request.args.get("processor")
    graphic_card_gb= request.args.get("graphic_card_gb")
    weight= request.args.get("weight")
    warranty= request.args.get("warranty")
    touchscreen = request.args.get("Touchscreen")
    touchscreen_value = 1 if touchscreen == 'yes' else 0

    pipe = pkl.load(open('laptopModel.pkl', 'rb'))

    columns = ["brand","ram_gb","ram_type","ssd","hdd","graphic_card_gb","weight","warranty","Touchscreen","os","processor"]
    data = np.array([brand, ram_gb, ram_type, ssd, hdd,graphic_card_gb, weight, warranty, touchscreen_value, os, processor]).reshape(1, 11)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    return render_template("result.html", result = result)

@app.route("/get-options", methods=["GET"])
def get_options():
    dataset = pd.read_csv("laptop.csv")
    selected_brand = request.args.get("brand")

    # Filter dataset based on the selected brand
    filtered_data = dataset[dataset["brand"] == selected_brand]
    os_options = filtered_data["os"].unique().tolist()

    return jsonify({
        "os": os_options,
    })

@app.route("/washing-machine-price")
def washinhgmachineprice():
    dataset = pd.read_csv("Washing_Machine_Cleaned_Data.csv")

    brand_name = sorted(dataset["brand_name"].unique())
    model_name = sorted(dataset["model_name"].unique())
    washing_capacity=sorted(dataset["washing_capacity"].unique())
    color=sorted(dataset["color"].unique())
    maximum_spin_speed=sorted(dataset["maximum_spin_speed"].unique())
    function_type=sorted(dataset["function_type"].unique())
    inbuilt_heater=sorted(dataset["inbuilt_heater"].unique())
    washing_method=sorted(dataset["washing_method"].unique())
    return render_template("washingMachine.html",brand_name=brand_name,model_name=model_name,washing_capacity=washing_capacity,color=color,maximum_spin_speed=maximum_spin_speed,function_type=function_type,washing_method=washing_method)

   

@app.route("/washing-machine-price-result")
def WashingMachinePriceResult():
    brand_name = request.args.get("brand_name")
    model_name = request.args.get("model")
    washing_capacity = request.args.get("capacity")
    color = request.args.get("color")
    maximum_spin_speed = request.args.get("maximum_spin")
    function_type = request.args.get("function_type")
    inbuilt_heater = request.args.get("inbuilt_heater")
    washing_method = request.args.get("washing_method")
    pipe = pkl.load(open('washingMachineModel.pkl', 'rb'))
    print("\n\n\n",pipe)
    print("\n\n\n",brand_name, model_name, washing_capacity, color, maximum_spin_speed,function_type,inbuilt_heater,washing_method)
    # columns = ["brand_name","model_name","washing_capacity","color","maximum_spin_speed","function_type","inbuilt_heater","washing_method"]
    columns = ["brand_name","model_name","washing_capacity","color","maximum_spin_speed","function_type","inbuilt_heater","washing_method"]

    data = np.array([brand_name, model_name, washing_capacity, color, maximum_spin_speed,function_type,inbuilt_heater,washing_method]).reshape(1,8)
    myinput = pd.DataFrame(columns = columns, data = data)
    print("\n\n\n",myinput)
    result = pipe.predict(myinput)

    return render_template("result.html", result = result)
   