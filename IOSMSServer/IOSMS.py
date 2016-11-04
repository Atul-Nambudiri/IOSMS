from flask import Flask, request, redirect
import subprocess
import twilio.twiml
import base64
import re

app = Flask(__name__)

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
        imageName = input[24:]
    	with open('progress', 'w+') as progress:
            progress.write("Started")
	with open('processed', 'w+') as processed:
	    processed.write('0')
        printString = "Starting processing image %s" % (imageName)
        print(printString)
	return printString
    elif 'texts were sent' in input:
        repart = re.findall('(.+) texts were sent', input)
    	number = repart[0]
        with open('progress', 'w') as progress:
            progress.write(number)
        resp = check_and_save()
        return resp			
    else:
    	repart = re.findall('\$\$-(.+)-\$\$.*', input)
        number = int(repart[0])
	filename = "imagelog/%s.out" % number
        with open(filename, 'w+') as imagelog:
            imagelog.write(input)
	
        parts = 0
	with open('processed', 'r') as processed:
	    parts = int(processed.read())
	    parts += 1

	with open('processed', 'w') as processed:
            processed.write(str(parts))

	resp = check_and_save()
        return resp

def check_and_save():
    """
    Check if the image is ready to save. Only saves when all parts of the image have been sent
    """
    progress = 0
    processed = 0
    with open('progress', 'r') as progress_file:
    	progress = progress_file.read()
    	if progress == "Started":
    	    return None
    	else:
    	    progress = int(progress)
    
    with open('processed', 'r') as processed_file:
        processed = int(processed_file.read())

    print("Progress %s" % progress)
    print("Processed %s" % processed)
    if progress == processed:
    	print("Done Processing Image")
	imagetext = ''
	for number in range(processed):
            filename = "imagelog/%s.out" % number
	    with open(filename, 'r') as imagelog:
                initial = imagelog.read()
		initial = initial[10:]
		imagetext += initial
				
        with open('out.txt', 'w+') as output:
	    output.write(imagetext)

        with open('out.jpg', 'wb') as image:
	    image.write(base64.b64decode(imagetext))

	return("Done Processing Image")

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
