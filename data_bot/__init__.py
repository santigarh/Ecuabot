from structs import text_message
from structs import item_quick_replie
from structs import quick_replie_message
from structs import quick_replies_location
from structs import template_message_generic
from structs import element_template_message
from structs import button_item_template_message_url
from structs import button_item_template_message_postback

from structs import typing_message
from structs import multimedia_message

def create_text_message(user, data, data_model = {}):
	message = data['content']
	if 'format' in data:
		message = message.format(**data_model)
	return text_message(user['user_id'], message)
	
def create_quick_replies(user, data):
	replies = [ item_quick_replie(replie['title'], replie['payload']) for replie in data['replies'] ]
	return quick_replie_message(user['user_id'], data['content'], replies)
	
def create_quick_replies_location(user, data):
	return quick_replies_location(user['user_id'], data['content'])

def create_template_message(user, data):
	elements = [ create_element_template_message(element) for element in data['elements']]
	return template_message_generic(user['user_id'], elements)

def create_element_template_message(data):
	buttons =  [ create_button_item_template_message(button) for button in data['buttons'] ]
	return element_template_message(data['title'], data['subtitle'],data['item_url'], data['image_url'], buttons )

def create_button_item_template_message(data):
	if data['type'] == 'web_url':
		return button_item_template_message_url(data['title'], data['url'])
	else:
		return button_item_template_message_postback(data['title'], data['payload'])
		
def create_image_message(user, data):
	url = data.get('url', '')
	
	#if not url:
	#	url = Aqui consumimos api
		
	return multimedia_message(user['user_id'], 'image' ,data['url'])

def create_video_message(user, data):
	url = data.get('url', '')
	return multimedia_message(user['user_id'],'video',url)

def create_audio_message(user, data):
	url = data.get('url', '')
	return multimedia_message(user['user_id'],'audio' ,url)

def create_file_message(user, data):
	url = data.get('url', '')
	return multimedia_message(user['user_id'],'file', url)
	
def create_typing_message(user):
	return typing_message(user['user_id'])