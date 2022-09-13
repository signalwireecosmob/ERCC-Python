import asyncio
import json
import logging


data = json.load(open(file="config.json", encoding="utf-8"))

def initiate_outbound_calls(self, service_number, is_recorded_msg, recording_url, sub_menu_selected):
    get_dialing_numbers(self, service_number, is_recorded_msg, recording_url, sub_menu_selected)


def get_dialing_numbers(self, service_number, is_recorded_msg, recording_url, sub_menu_selected):
    number_config = data['DIALING_LIST_VOICE']

    for item in number_config:
        if service_number in item.values():
            agents_to_call = item.get('number_list')

    for agent_number in agents_to_call:
        task = asyncio.create_task(make_outbound_call(self, service_number, is_recorded_msg, recording_url, sub_menu_selected, agent_number))


async def make_outbound_call(self, service_number, is_recorded_msg, recording_url, sub_menu_selected, agent_number):
    logging.info(f'[OUTBOUND CALL] : Calling {agent_number} from {service_number} ...........')
    dial_result = await self.client.calling.dial(from_number=service_number, to_number=agent_number)


    if dial_result.successful == True:
        call = dial_result.call

        if is_recorded_msg:
            logging.info('[OUTBOUND CALL] : Playing recorded emergency voice notification : ' + recording_url)
            await call.play_tts(text= 'Hi, You have received a Recorded emergency voice notification.')
            await call.play_audio(recording_url)
            await call.play_tts(text= 'Thank you!')


        else:
            notification = data['DIALING_LIST_VOICE_PHRASE'].get(f'DTMF_{sub_menu_selected}')
            logging.info('[OUTBOUND CALL] : Playing notification message : ' + notification)
            await call.play_tts(text= 'Hi, You have received a Predefined Emeregency Notification.')
            await call.play_tts(text=notification)
            await call.play_tts(text= 'Thank you!')
            logging.info('[OUTBOUND CALL] : Emergency Message has been notified successfully')

        await call.hangup()
    else:
         await call.hangup()

    logging.info('[OUTBOUND CALL] : Outbound call ended')

    return