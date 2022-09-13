import asyncio
import json
import logging
import os
import requests
from emergencyVoiceBroadcast import data
from google.cloud import speech

def initiate_sms_broadcast(self, service_number, is_recorded_msg, recording_url, sub_menu_selected):
    if is_recorded_msg:
        audio_file = download_recorded_audio(recording_url)
        transcription = transcript_file(audio_file)
        emergency_notification = f'You have received a recorded emergency notification : {transcription}'
        get_dialing_numbers(self, service_number, emergency_notification)

    else:
        notification = data['DIALING_LIST_VOICE_PHRASE'].get(f'DTMF_{sub_menu_selected}')
        emergency_notification = f'You have received a Predefined emergency notification : {notification}'
        get_dialing_numbers(self, service_number, emergency_notification)


def get_dialing_numbers(self, service_number, emergency_notification):
    number_config = data['DIALING_LIST_SMS']

    for item in number_config:
        if service_number in item.values():
            agents_to_call = item.get('number_list')

    for agent_number in agents_to_call:
        task = asyncio.create_task(make_outbound_sms(self, service_number, agent_number, emergency_notification))


async def make_outbound_sms(self, service_number, agent_number, emergency_notification):
    sms_result = await self.client.messaging.send(context='outbound_sms', from_number=service_number, to_number=agent_number, body= emergency_notification)
    
    if sms_result.successful:
        logging.info(f'[OUTBOUND SMS] : Message sent successfully. Message ID: {sms_result.message_id}, Message Body : {emergency_notification}')
  
    else:
        logging.info(f'[OUTBOUND SMS] : Unable to send sms to {agent_number} from {service_number}, Message Body : {emergency_notification}')


def download_recorded_audio(link):
  file_name = link.split('/')[-1]
  print(f"Downloaded file name : {file_name}")
  r = requests.get(link, stream=True)
  with open (file_name,'wb') as f:
    for chunk in r.iter_content(chunk_size= 1024*1024):
      if chunk:
        f.write(chunk)

  logging.info(f"[TRANSCRIPTION] : File Downloaded Successfully! : {file_name}")
  return file_name


def transcript_file(speech_file):
    service_account_config = data['GOOGLE_CONFIG']
    client = speech.SpeechClient.from_service_account_json(service_account_config)

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=24000,
        language_code="en-US")

    operation = client.long_running_recognize(config=config, audio=audio)
    logging.info("[TRANSCRIPTION] : Waiting for transcript operation to complete...")
    response = operation.result(timeout=90)

    transcription = ''
    for result in response.results:
        sentence = result.alternatives[0].transcript
        transcription = transcription + sentence   

    if os.path.isfile(speech_file):
        os.remove(speech_file)
        logging.info("[TRANSCRIPTION] : Local audio file has been deleted")
    else:
        logging.info("[TRANSCRIPTION] : Local audio file does not exist")
        
    logging.info('[TRANSCRIPTION] : ' + transcription)
    return transcription
