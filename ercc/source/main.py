import asyncio
import json
import logging
from signalwire.relay.consumer import Consumer
from emergency_service import prompt_custom_tts, play_custom_tts, record_voice_message, process_outbound_notifications

data = json.load(open(file="config.json", encoding="utf-8"))

class CustomConsumer(Consumer):
    def setup(self):
        self.project = data['SIGNALWIRE_CONFIG'].get('PROJECT_ID')
        self.token = data['SIGNALWIRE_CONFIG'].get('APP_TOKEN')
        self.contexts = ['contexts_incoming']


    async def on_incoming_call(self, call):
        result = await call.answer()
        service_number = call.to_number
        ivr_audio_gender = data["IVR_AUDIO_GENDER"]

        if result.successful is False:
            logging.info('[INBOUND CALL] : Error answering the call')
            return

        if result.successful:
            logging.info("[INBOUND CALL] : Incoming Call Answered") 
            await play_custom_tts(call, 'Welcome to emergency notification service!', ivr_audio_gender)
            
            tts_message = "Press 1 for record voice notification. Press 2 for predefined emergency message selection"
            tts_nomatch_message = "You have selected invalid input. Please try again"
            tts_blank_message = "You have not selected any input. Please try again"
            dtmf_inputs_allowed = ['1', '2']
            max_tries = data["MAX_TRIES"]
            digits_timeout = data["DIGIT_INPUT_TIMEOUT"]
            result = await prompt_custom_tts(call, tts_message, tts_nomatch_message, tts_blank_message, dtmf_inputs_allowed, digits_timeout, max_tries, ivr_audio_gender)

            if result == 'NOMATCH' or result == 'BLANK':
                tts_message = "You have reached maximum tries. Thank you for calling emergency notification service"
                await play_custom_tts(call, tts_message, ivr_audio_gender)
                await call.hangup()
                return

            elif result == '1':
                tts_message = "Please record your voice notification message after the beep. Press # key to stop the recording."
                await play_custom_tts(call, tts_message, ivr_audio_gender)
                beep = True
                stereo = True
                direction = 'both'
                end_silence_timeout = 5.0
                terminators = '#'
                recorded_voice_message = await record_voice_message(call, beep, stereo, direction, end_silence_timeout, terminators)

                if recorded_voice_message.successful:
                    result = await play_custom_tts(call, "Successfully recorded the voice notification message. we will broadcast this to the authorized person. Thank you", ivr_audio_gender)
                    is_recorded_msg = True
                    recording_url = recorded_voice_message.url
                    sub_menu_selected = None
                    
                    await call.hangup()
                    process_outbound_notifications(self, service_number, is_recorded_msg , recording_url, sub_menu_selected)
                    
                else:
                    result = await play_custom_tts(call, "Unable to recorded voice nofication. Please try again after sometime or select pre-defined message", ivr_audio_gender)
                    await call.hangup()   
                return

            elif result == '2':
                tts_message = data['PREDEFINED_EMERGENCY_MENU'].get('SUB_MENU_PHRASE')
                tts_nomatch_message = "You have selected invalid input. Please try again"
                tts_blank_message = "You have not selected any input. Please try again"
                dtmf_inputs_allowed = data['PREDEFINED_EMERGENCY_MENU'].get('DTMF_ALLOWED')
                max_tries = data["MAX_TRIES"]
                digits_timeout = data["DIGIT_INPUT_TIMEOUT"]
                
                result = await prompt_custom_tts(call, tts_message, tts_nomatch_message, tts_blank_message, dtmf_inputs_allowed, digits_timeout, max_tries, ivr_audio_gender)
                
                if result == 'NOMATCH' or result == 'BLANK': 
                    tts_message = "You have reached maximum tries. Thank you for calling emergency notification service"
                    await play_custom_tts(call, tts_message, ivr_audio_gender)
                    await call.hangup()
                    return

                else:
                    if result in dtmf_inputs_allowed:
                        tts_message = f'Successfully selected the predefined notification . We will broadcast this to the authorized person. Thank you'

                await play_custom_tts(call, tts_message, ivr_audio_gender)
                
                is_recorded_msg = False
                recording_url = None
                sub_menu_selected = result
                await call.hangup()
                process_outbound_notifications(self, service_number, is_recorded_msg , recording_url, sub_menu_selected)
                return



consumer = CustomConsumer()
consumer.run()
