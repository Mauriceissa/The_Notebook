# File: preparation.py

# Step 1: Creating a Project Folder
# ---------------------------------
# Create a new folder on your computer where you'll store all the code and files related to this project. 
# You can create a folder using the file explorer or terminal/command prompt with the following commands:

# For Windows:
# ------------ Navigate to the location where you want to create the folder and run
# mkdir MyLogBook

# For MacOS/Linux:
# ---------------- Navigate to the location where you want to create the folder and run
# mkdir MyLogBook

# Navigate into the project folder:
# cd MyLogBook


# Step 2: Creating a Virtual Environment
# --------------------------------------
# Create a virtual environment inside your project folder. This helps in isolating your project's
# dependencies. Replace "venv" with the name you'd like to give to your virtual environment.

# For Windows:
# ------------
# python -m venv venv
# venv\Scripts\activate

# For MacOS/Linux:
# ----------------
# python3 -m venv venv
# source venv/bin/activate

# Note: Ensure that Python is already installed on your computer.


# Step 3: Installing Required Packages
# -------------------------------------
# After activating the virtual environment, you'll need to install some packages that the project depends on.
# Run the following commands to install these packages.

# Install pycryptodome for encryption and decryption
# --------------------------------------------------
# pip install pycryptodome

# Install pyinputplus for enhanced user input features
# ----------------------------------------------------
# pip install pyinputplus

# If there are any other dependencies needed, install them using pip as well.


# Step 4: Environment Variables
# -----------------------------
# You should set up environment variables to store sensitive data such as the encryption key, password,
# and log directory. This is a safer practice than hardcoding such values into your script.

# You can set environment variables directly in your system, or use a .env file and a package like python-decouple
# to read them. Below are examples of setting environment variables directly in the system.

#first you should create your own encryption key by running this code:
from base64 import b64encode, b64decode
from hashlib import sha256
import os

# Generate a random 44 characters long encryption key string
encryption_key_string = b64encode(os.urandom(33)).decode('utf-8')[:44]

print(f"Your 44 characters encryption key is: {encryption_key_string}")


# For Windows:
# ------------
# $env:encryption_key="your-encryption-key"        the key generated above
# $env:LOG_DIRECTORY="path-to-your-log-directory"  wherever you want to store the txt files
# $env:THE_PASSWORD="your-password"                the password required to access the program

# For MacOS/Linux:
# ----------------
# export encryption_key="your-encryption-key"
# export LOG_DIRECTORY="path-to-your-log-directory"
# export THE_PASSWORD="your-password"

# Replace "your-encryption-key", "path-to-your-log-directory", and "your-password" with your actual values.


# Step 5: Running the Main Script
# --------------------------------
# Now, you can run the main script. Ensure the virtual environment is activated, and the environment variables
# are set each time you want to run the script. Navigate to the directory containing your script and run:

# python main_script.py   # Replace with the actual name of your script

# Follow the on-screen prompts to interact with the logbook.

# GOOD LUCK

# pyinstaller --onefile --icon=guld_note_book2.ico The_notebook.py