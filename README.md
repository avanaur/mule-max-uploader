# Max Mule Uploader
Uploader of Max the Mule images to Mule Champions

### Overview

This python script automates the upload of Max the Mule images to Mule Champions. It fetches images from your Dropbox account (stored on a folder), and then uploads it to Mule Champions. A max of 3 images will be uploaded to Mule Champions (which is the limit daily)

### Requirements
- Dropbox account
    - **Authorization header**: Grants access to your account via Dropbox API (ex. Bearer JSLAJKJXNMCNXZmTERxnzcmxnzchofaojfioasj)
    - **Source folder**: source folder dedicated to images of Max the mule
    - **Target folder**: target acrhive folder where uploaded mule images are moved to
- Mule champions credentials
    - Login and password 
- Python (2.7)

### How to use
1. Updated champions-max.cfg with neccessary informations
2. Run champions-max-uploader-v1.py

### Note
It is important to only put unique and your own Max the Mule images on your Dropbox account source folder. Otherwise, you risk having your images rejected.

You may add this script on a cron scheduler so it will automate upload for you. 