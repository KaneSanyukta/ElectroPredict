import pandas as pd # type: ignore
import numpy as np
import pickle as pkl
import os
from flask import Flask, jsonify, url_for, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt

# Initialize Flask app
app = Flask(__name__)

# Database configuration for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Set up secret key for session management
app.secret_key = os.urandom(24)

# Define User model with SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

# Signup and login forms using Flask-WTF
class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email Id Already Exists. Try another email.')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/signup', methods=['POST','GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Insert the user into the database
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of an error
            flash(f"Error inserting record into DB: {str(e)}", 'error')
            print(f"Error: {str(e)}")
    
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            # Compare hashed password with the one stored in the database
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password!', 'error')
                return redirect(url_for('login'))
        else:
            flash('User does not exist!', 'error')
            return redirect(url_for('login'))

    return render_template('index.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)

        if user:
            return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.clear()
    flash("You have been logged out successfully.")
    return redirect(url_for('login'))

# Create the database (SQLite) tables for SQLAlchemy (for local development/testing)
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def index():
    return redirect("/login")
    
if __name__ == '__main__':
    app.run(debug=True)

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
    return render_template("tablet.html", name=name, processor_brand=processor_brand,num_processor=num_processor,processor_speed=processor_speed,ram=ram,battery_capacity=battery_capacity,resolution_width=resolution_width,resolution_height=resolution_height,ppi=ppi,primary_front_camera=primary_front_camera,primary_rear_camera=primary_rear_camera,memory_card_upto=memory_card_upto,sim=sim,is_5G=is_5G,memory_inbuilt=memory_inbuilt)
    
@app.route("/tab-price-result")
def TabPriceResult():
   
    name = request.args.get("name")  
    processor_brand = request.args.get("processor_brand")
    num_processor = request.args.get("num_processor")
    processor_speed = request.args.get("processor_speed")
    ram = request.args.get("ram")
    memory_inbuilt = request.args.get("memory_inbuilt")
    battery_capacity = request.args.get("battery_capacity")
    resolution_width = request.args.get("resolution_width")
    resolution_height = request.args.get("resolution_height")
    ppi = request.args.get("ppi", 0)
    primary_front_camera = request.args.get("primary_front_camera")
    primary_rear_camera = request.args.get("primary_rear_camera")
    memory_card_upto = request.args.get("memory_card_upto")
    sim = request.args.get("sim")
    is_5G = request.args.get("is_5G")
    # Load trained model
    pipe = pkl.load(open('TabModel.pkl', 'rb'))
    columns = ["name","processor_brand","num_processor","processor_speed","ram","memory_inbuilt","battery_capacity","resolution_width","resolution_height","ppi","primary_front_camera","primary_rear_camera","memory_card_upto","sim","is_5G"]
    data = np.array([name,processor_brand,num_processor,processor_speed,ram,memory_inbuilt,battery_capacity,resolution_width,resolution_height,ppi,primary_front_camera,primary_rear_camera,memory_card_upto,sim,is_5G]).reshape(1, 15)
    myinput = pd.DataFrame(columns = columns, data = data)
    print("\n\n\n\n\n",name,processor_brand,num_processor,processor_speed,ram,memory_inbuilt,battery_capacity,resolution_width,resolution_height,ppi,primary_front_camera,primary_rear_camera,memory_card_upto,sim,is_5G,"\n\n\n\n")
    # Handle missing values
    myinput.fillna("Unknown", inplace=True)
    result = pipe.predict(myinput)
    return render_template("result.html", result = result)

@app.route("/cellphone-price")
def cellphone():
    dataset = pd.read_csv("cellphoneData.csv")
    brand = sorted(dataset["Brand"].unique())
    model = sorted(dataset["Model"].unique())
    storage = sorted(dataset["storage"].unique())
    ram = sorted(dataset["ram"].unique())
    screen_size= sorted(dataset["screen_size"].unique())
    camera = sorted(dataset["camera"].unique())
    battery_capacity = sorted(dataset["battery_capacity"].unique())
    return render_template("cellphone.html",brand=brand, model=model, storage=storage, ram=ram, screen_size=screen_size,camera=camera, battery_capacity=battery_capacity)

@app.route("/cellphone-price-result")
def CellphonePriceResult():
    model = request.args.get("model")
    brand = request.args.get("brand")
    battery_capacity = request.args.get("battery_capacity")
    storage = request.args.get("storage")
    ram = request.args.get("ram")
    camera = request.args.get("camera")
    screen_size = request.args.get("screen_size")
    pipe = pkl.load(open('cellphoneModel.pkl', 'rb'))

    columns = ["Brand","Model","storage","ram","screen_size","camera","battery_capacity"]
    data = np.array([brand,model,storage,ram,screen_size,camera,battery_capacity]).reshape(1, 7)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    return render_template("result.html", result = result)

@app.route("/television-price")
def television():
    # ,Product_Name,stars,ratings,price,channel,operating_system,picture_qualtiy,speaker,frequency
    dataset = pd.read_csv("televisionData.csv")
    brand = sorted(dataset["Product_Name"].unique())
    stars = sorted(dataset["stars"].unique())
    ratings = sorted(dataset["ratings"].unique())
    channel = sorted(dataset["channel"].unique())
    operating_system = sorted(dataset["operating_system"].unique())
    picture_quality = sorted(dataset["picture_qualtiy"].unique())
    speaker = sorted(dataset["speaker"].unique())
    frequency = sorted(dataset["frequency"].unique())
    
    return render_template("television.html",brand=brand,stars=stars,ratings=ratings,channel=channel,operating_system=operating_system,picture_quality=picture_quality,speaker=speaker,frequency=frequency)

@app.route("/television-price-result")
def televisionPriceResult():
    brand = request.args.get("brand")
    stars = request.args.get("stars")
    ratings = request.args.get("ratings")
    channel = request.args.get("channel")
    operating_system = request.args.get("operating_system")
    speaker = request.args.get("speaker")
    frequency = request.args.get("frequency")
    picture_quality = request.args.get("picture_quality")

    pipe = pkl.load(open('TelevisionModel.pkl', 'rb'))
    columns = ["Product_Name","stars","ratings","channel","operating_system","picture_qualtiy","speaker","frequency"]
    data = np.array([brand,stars,ratings,channel,operating_system,picture_quality,speaker,frequency]).reshape(1, 8)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    return render_template("result.html",result=result)

@app.route("/refregirator-price")
def fridge():
    # ,Brand,Capacity,Energy Rating,Type,Features,Color,Material,Warranty Period,Country of Manufacture,Price
    dataset = pd.read_csv("fridgeData.csv")
    brand = sorted(dataset["Brand"].unique())
    capacity = sorted(dataset["Capacity"].unique())
    energy_rating = sorted(dataset["Energy Rating"].unique())
    type1 = sorted(dataset["Type"].unique())
    features = dataset["Features"].unique()
    color = sorted(dataset["Color"].unique())
    material = sorted(dataset["Material"].unique())
    warranty_period = sorted(dataset["Warranty Period"].unique())
    country_of_manufacture = sorted(dataset["Country of Manufacture"].unique())
    return render_template("refrigerators.html",brand=brand,capacity=capacity,energy_rating=energy_rating,type1=type1,features=features,color=color,material=material,warranty_period=warranty_period,country_of_manufacture=country_of_manufacture)

@app.route("/fridge-price-result")
def fridgePriceResult():
    brand = request.args.get("brand")
    capacity = request.args.get("capacity")
    energy_rating = request.args.get("energy_rating")
    type1 = request.args.get("type1")
    features = request.args.get("features")
    color = request.args.get("color")
    material = request.args.get("material")
    warranty_period = request.args.get("warranty_period")
    country_of_manufacture = request.args.get("country_of_manufacture")
    pipe = pkl.load(open('fridgeModel.pkl', 'rb'))
    columns = ["Brand","Capacity","Energy Rating","Type","Features","Color","Material","Warranty Period","Country of Manufacture"]
    data = np.array([brand,capacity,energy_rating,type1,features,color,material,warranty_period,country_of_manufacture]).reshape(1, 9)
    myinput = pd.DataFrame(columns = columns, data = data)
    result = pipe.predict(myinput)
    result=result*85.51
    return render_template("result.html",result=result)
