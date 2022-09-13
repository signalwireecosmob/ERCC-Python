# Overview :

ERCC is a telephony based emergency notification system designed to provide instant emergency notification with configured phone numbers when notification triggered by inbound call. With ERCC Installed, your mobile phone will become a trigger for the Emergency Alarm. 

# Call flow : 
- Make Inbound call to the purchased Signalwire phone number.
- The call will be answered, and two menus will be played.
- Press 1 to record voice as a emergency notification
- Press 2 to select predefined emergency notification:
- If option 1 is selected: Voice recording process will get started maximum 30 sec recording
    - Recorded voice transcription will be sent as SMS to the configured phone numbers
    - Recorded Voice will be played by calling configured phone numbers
- If option 2 is selected: Predefined emergency notification will be played and option will be given to select notification
    - Selected emergency notifications will be sent to configured phone numbers by SMS and voice call.

# Prerequisites :
- Docker
- Signalwire space
- Google cloud platform account (for voice transcription)


# Signalwire configuration:
- Project ID
- APP token
- Purchased Phone number/Service number (To receive Inbound calls from caller)
- Accept incoming call as:  Voice call
- Handle call using : Relay
- Context: contexts_incoming
- Configuration and other integrations:
```sh
{
  "SIGNALWIRE_CONFIG": {
    "PROJECT_ID": "**************************",
    "APP_TOKEN": "****************************"
  },
  "GOOGLE_CONFIG": "service_account.json",
  "DIALING_LIST_VOICE": [
    {
      "servicenumber": "+************", "number_list": ["+********"]
    }
  ],
  "DIALING_LIST_SMS": [
    {
      "servicenumber": "+************", "number_list": ["+*********"]
    }
  ],
  "PREDEFINED_EMERGENCY_MENU":
   {
    "SUB_MENU_PHRASE":"Press 1 to notify Fire in building, Press 2 to notify Emergenncy help needed",
    "DTMF_ALLOWED":["1","2"]
   }
  ,
 
  "DIALING_LIST_VOICE_PHRASE":
    {
      "DTMF_1": "Fire in building notification is raised by someone",
      "DTMF_2": "Emergency help needed notification is raised by someone"
    },
 
  "DIALING_LIST_SMS_PHRASE":
    {
      "DTMF_1": "Fire in building notification is raised by someone",
      "DTMF_2": "Emergency help needed notification is raised by someone"
    },
  "IVR_AUDIO_GENDER":"female",
  "DIGIT_INPUT_TIMEOUT" : 7,
  "MAX_TRIES" : 3
 
}
```


# For Google Speech to text api  integration:

### Google cloud Platform (GCP)  billing account
#### GCP service account 
 GCP -> Navigation menu -> IAM & Admin -> Service accounts -> create service account -> Give service account name and ID -> Create and Continue -> Under select role-> Cloud speech administrator->Continue and Done

#### Enable speech to text API 
 GCP->Navigation menu -> API’s and services -> Library -> Search for cloud    speech to text api ->Select cloud speech to text api -> Enable and select billing account -> Done

#### Private key
Private Key for service account -> IAM & Admin -> service account for 

#### Speech-To-Text API
Speech to text api -> Keys -> Add key -> Create new key -> JSON create -> Rename it as service account.json and pasted it over in your project folder
```sh
{
  "type": "service_account",
  "project_id": "<Your Project ID>",
  "private_key_id": "*****************************",
  "private_key": "-----BEGIN PRIVATE KEY-----\n*****************************************************\n*************************/***/**/**************\n***************/***********/**************\n/X0+-----END PRIVATE KEY-----\n",
  "client_email": "***********@project-*****.iam.gserviceaccount.com",
  "client_id": "********************",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/********************.iam.gserviceaccount.com"
}
```

# Steps to run sample code:

##### With Docker :

##### Install docker and  run following commands

```sh
sudo  docker build -t python-ercc .
```
```sh
sudo  docker run -t python-ercc
```
##### Without Docker :

##### Install requirements  using command:


```sh
pip install -r requirements.txt
```

##### To run sample code:
```sh
python main.py
```
OR

```sh
python3 main.py
```

Please refer to the demonstration video for more details (demo.webm)
# ERCC-Python
# ERCC-Python
# ERCC-Python
# ERCC-Python
