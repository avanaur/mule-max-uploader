
# coding: utf-8

# In[1]:

import requests
import shutil
import os
from bs4 import BeautifulSoup
import ConfigParser


# In[6]:

# CONFIGURATION

config = ConfigParser.RawConfigParser()
config.read('champions-max.cfg')

# dropbox auth token
auth_header = config.get('Dropbox', 'auth_header')
# dropbox image source folder
path = config.get('Dropbox', 'path') 
# dropbox archive folder
archive_path = config.get('Dropbox', 'archive_path') 
# champions login credentials
login_user = config.get('Mule Champions', 'login_user')
login_password = config.get('Mule Champions', 'login_password')


# In[3]:

# RETRIEVE IMAGE LISTS
bodyData = {
    'path': path
}
headerData = {
    'Authorization': auth_header,
    'Content-Type': 'application/json'
}
res = requests.post('https://api.dropboxapi.com/2/files/list_folder', json=bodyData, headers=headerData)
print "checking images available for upload: " + "success" if res.status_code == 200 else "failure"
jsonRes = { 
    'entries': []
}
if res.status_code == 200:
    jsonRes = res.json()


# In[7]:

# LOGIN TO CHAMPIONS
session  = requests.Session()
if len(jsonRes['entries']) > 0:
    res = session.get('http://champions.mulesoft.com')
    soup = BeautifulSoup(res.text, 'html.parser')
    auth_token = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
    formData = {
        'utf8': '✓',
        'authenticity_token' : auth_token,
        'user[email]': login_user,
        'user[password]': login_password,
        'commit': 'Sending..'
    }
    session.post('https://mulesoft.influitive.com/users/sign_in', data = formData)


# In[8]:

# process 3 image
for cnt in range(0, 3 if len(jsonRes['entries']) > 3 else len(jsonRes['entries'])):
    
    # processing each image
    image_file = jsonRes['entries'][cnt]['name']
    print "PROCESSING " + image_file
    
    # download image
    headerData = {
        'Authorization': auth_header,
        'Dropbox-API-Arg': "{\"path\":\"" + path + "/" + image_file + "\"}"
    }
    res = requests.post('https://content.dropboxapi.com/2/files/download', headers=headerData, stream=True)
    print "image retrieval: " + "success" if res.status_code == 200 else "failure"
    if res.status_code == 200:
        with open(image_file, 'wb') as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)
        print "local copy saved"
        
        # upload to champions
        res = session.get('http://champions.mulesoft.com/challenges/31/activities/new')
        soup = BeautifulSoup(res.text, 'html.parser')
        auth_token = soup.find_all('meta', attrs={'name': 'csrf-token'})[0].get('content')
        formData = {
            'utf8': '✓',
            'authenticity_token' : auth_token,
            'activity[challenge_id]': '31',
            'activity[subject_id]': '',
            'activity[stage_id]': '48',
            'activity[name]': 'Share Your Max the Mule Pic!',
            'activity[description]': '### Do you have an awesome picture of Max the Mule?',
            'stage_type': 'question_with_image',
            'activity[responses_attributes][0][question_id]': '37',
            'activity[responses_attributes][0][contact_id]': '1098',
            'challenge_analytics': '{"goal_count":0,"rewards_available":27}',
            'remotipart_submitted': 'true',
            'X-Requested-With': 'IFrame',
            'X-Http-Accept': 'application/json, text/javascript, */*; q=0.01',
            'commit': 'Share It!'
        }
        res = session.post('http://champions.mulesoft.com/activities', 
                            data = formData, 
                            files = {'activity[responses_attributes][0][body_image]': 
                                     (image_file, 
                                      open(image_file, 'rb'),
                                      'image/jpeg'
                                     )})
        print "uploading image to champions: " + "success" if res.status_code == 200 else "failure"
        
        # delete local copy
        os.remove(image_file)
        print "local copy deleted"

        # move dropbox copy
        bodyData = {
            'from_path': path + "/" + image_file,
            'to_path': archive_path + "/" + image_file
        }
        headerData = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }
        res = requests.post('https://api.dropboxapi.com/2/files/move', json=bodyData, headers=headerData, stream=True)
        print "archiving image: " + "success" if res.status_code == 200 else "failure"


# In[9]:

print "DONE"


# In[ ]:



