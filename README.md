# COMP3278 Group 6 Project
## Members
<ul>
  <li>Chan Yu Yan Sam 3035188203</li>
  <li>Kwan Man Hei 3035460259</li>
  <li>Srivastava Dhruv 3035667792</li>
  <li>Tamanna Singhal 3035664647</li>
  <li></li>
</ul>

## Execution Instructions

### Step 1: Database Import

Run the `facerecognition.sql` file. This will create a new database `comp3278gr6`, with some dummy data for the application.

### Step 2: Environment Set Up

Create virtual environment using Anaconda with the help of the `requirements.txt` file provided.
```
conda create -n face python=3.x
conda activate face
pip install -r requirements.txt
```
Activate the environment once ready.

### Step 3: Set up face recognition

#### Step 3.1: Face Data Collection
Run the `face_capture.py` script to capture images for the user. As the dummy data already has entries for customers, please train the model according to the order in which the customers are present in the table by changing the value of the `user_name` variable to the names appearing in the customer table (the first name has already been added in the script). Before running the script, please ensure that a directory named `data` is present (the script may cause errors if the directory is not present).
```
"""
user_name = "Dhruv"   # the name
NUM_IMGS = 400       # the number of saved images
"""
python face_capture.py
```
#### Step 3.2: Train the Model
Run the `train.py` script to train the model.
```
python train.py
```
`train.yml` and `labels.pickle` will be created at the current folder.

### Step 4: Connect Script to the Database
Before running the `COMP3278_GR6_Application.py` script, please connect the script with the database by changing `user` and `passwd` values as follows:
```
# create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="xxxxx", database="comp3278gr6")
```
### Step 5: Run the Application
Run the `COMP3278_GR6_Application.py` script to run the application (it may take some time to start). Please refer to the demo video on how to use the application.
```
python COMP3278_GR6_Application.py
```
