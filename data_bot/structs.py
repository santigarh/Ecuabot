def typing_message(recipient_id): #Estructura enviar eventos - Accion escribiendo
		message_data = {
			'recipient': { 'id' : recipient_id },
			'sender_action': 'typing_on'
		}
		return message_data
	
def text_message(recipient_id, message_text): #Estructura enviar mensajes
	message_data = {
		'recipient': { 'id': recipient_id },
		'message' :{'text': message_text }
	}
	return message_data
	
def item_quick_replie(title, payload):
		item ={
			'content_type': 'text',
			'title': title,
			'payload': payload
		}
		return item
	
def quick_replie_message(recipient_id, title, quick_replies):
	message_data = {
		'recipient': { 'id': recipient_id },
		'message' :{ 
		'text' : title,
		'quick_replies': quick_replies		
		}
	}
	return message_data

def quick_replies_location(recipient_id, title):
	message_data = {
		'recipient': { 'id': recipient_id },
		'message' :{ 
		'text' : title,
		'quick_replies': [
			{
				'content_type': 'location',
			}
		]		
		}
	}
	return message_data

def button_item_template_message(title, payload):
		button={ "type": "postback",
				 "title": title,
				 "payload": payload }
		return button

def button_item_template_message_url(title, url):
    button = {  "type": "web_url",
                "title": title,
                "url": url }
    return button

def button_item_template_message_postback(title, payload):
	button = {  "type": "postback",
                "title": title,
                "payload": payload }
	return button

def element_template_message(title, subtitle, item_url, image_url, buttons):
	item = { 
	    "title": title,
	    "subtitle": subtitle,
	    "item_url": item_url,
	    "image_url": image_url,
	    "buttons": buttons
    }
	return item

def template_message_generic(recipient_id, elements):
	message_data = {
        "recipient":{ "id":recipient_id},
        "message":{
            "attachment":
                {
                    "type":"template",
                    "payload":
                    {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
        }
    }
	return message_data 

def multimedia_message(recipient_id, type_message, url):
	message_data = {
		'recipient': { 'id': recipient_id },
		'message': {
			'attachment': {
				'type': type_message,
				'payload': {
					'url': url
				}
			}
		}
	}
	return message_data
	
	{u'mid': u'mid.$cAAdYzIfefRZnGMdlwFg54IX67awO', u'seq': 196348, u'attachments': 
	[{u'url': u'https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D-0.3139627%252C%2B-78.443724%26FORM%3DFBKPL1%26mkt%3Den-US&h=ATPby1DbHW5yq7biZVNWiCg7kR4HnBajmPazQHntwL7u_guHBONYbUvEms-I3ZeA-9KXwg0u2Eh_E0oBxt7qxGgWmQ_p30zVYpu97POVr3-Yx6ewfQ&s=1&enc=AZMq3q4Or5pw0LszKS5DybomIbL_ML02VDAmMWm-nolGnbyf0Vf07ODNvag8DRsv7iKaxpjzWPVFsVacpW2Ra_ct', 
	u'type': u'location', u'payload': {u'coordinates': {u'lat': -0.3139627, u'long': -78.443724}}, u'title': u"Juan's Location"}]}

	
