from emergencyVoiceBroadcast import initiate_outbound_calls
from emergencySMSBroadcast import initiate_sms_broadcast


async def prompt_custom_tts(call, tts_message, tts_nomatch_message,tts_blank_message, dtmf_inputs_allowed, dtmf_timeout, max_tries, gender):
    
    for tries in range(1,max_tries+1):
        result = await call.prompt_tts(digits_timeout = dtmf_timeout, prompt_type='digits', text=tts_message, digits_max=1, volume= 5, gender=gender)
        
        if result.successful:
            if result.result in dtmf_inputs_allowed:
                return result.result
            else:
                if tries < max_tries:
                    await call.play_tts(text=tts_nomatch_message, volume= 5, gender=gender)
                    continue
        else:
            if tries < max_tries:
                await call.play_tts(text=tts_blank_message, volume= 5, gender=gender)
                continue
        
    if result.successful == True:
        return 'NOMATCH'
    else :
        return 'BLANK'

async def play_custom_tts(call, tts_message, gender):
    await call.play_tts(text = tts_message, language = "en-US", volume= 5, gender=gender)


async def record_voice_message(call, beep, stereo, direction, end_silence_timeout, terminators):
    result = await call.record(beep=beep, stereo=stereo, direction=direction, end_silence_timeout=end_silence_timeout, terminators=terminators)
    return result


def process_outbound_notifications(self, service_number, is_recorded_msg , recording_url, sub_menu_selected):
    initiate_outbound_calls(self, service_number, is_recorded_msg, recording_url, sub_menu_selected)
    initiate_sms_broadcast(self, service_number, is_recorded_msg, recording_url, sub_menu_selected)