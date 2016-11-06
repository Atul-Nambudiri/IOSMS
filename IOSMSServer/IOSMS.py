from lib.db_access import DBAccess

from flask import Flask, request, redirect
import subprocess
import twilio.twiml
import base64
import time
import re

app = Flask(__name__)
db_access = DBAccess('main.db')

@app.route("/", methods=['GET', 'POST'])
def respond():
    body = request.values.get('Body', None)
    print("This is the body: %s" % body)
    response = process_input(body)
    resp = twilio.twiml.Response()
    if response == None:
        resp.redirect('http://twimlets.com/echo?Twiml=%3CResponse%3E%3C%2FResponse%3E')
    else:
	resp.message(response)
    return str(resp)


def process_input(input):
    if "Start Image" in input:
        image_name = input[24:]
        db_access.add_image(image_name)
        print_string = "Starting processing image %s" % (image_name)
        print(print_string)
	return print_string
    elif 'texts were sent' in input:
        repart = re.match('(.+) texts were sent for (.+)', input)
    	number = repart.group(1)
        image_name = repart.group(2)
        db_access.add_total_section_count(image_name, number)
        return check_and_save(image_name)
    else:
    	repart = re.match('\$\$-(.+)-\$\$.*', input) 
        section = int(repart.group(1)[:4])
        image_name = repart.group(1)[4:]
        blob = input[(len(repart.group(1)) + 6):]
        
        print("Image Name: %s" % image_name)
        print("Section: %d" % (section))
        print("Blob: %s" % (blob))
        received_sections = db_access.get_received_sections_count(image_name)
        total_sections = db_access.get_total_sections_count(image_name)

        db_access.add_image_section(image_name, section, blob)
        db_access.update_received_sections(image_name, received_sections + 1)
        return check_and_save(image_name)

def check_and_save(image_name):
    """
    Check if the image is ready to save. Only saves when all parts of the image have been sent
    """
    received_sections = db_access.get_received_sections_count(image_name)
    total_sections = db_access.get_total_sections_count(image_name)
    
    if received_sections != total_sections:
        return None
    
    sections = db_access.get_image_sections(image_name)
    image_text = "".join([section[0] for section in sections])
    
    time_stamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    with open('output/%s-%s.jpg' % (image_name, time_stamp), 'wb') as image:
	binary = base64.b64decode(image_text)
        image.write(binary)
    
    db_access.delete_image_and_info(image_name)
    return("Done Processing Image: %s" % (image_name))

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
