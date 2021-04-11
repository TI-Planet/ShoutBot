# python3 -m pip install flask
# python3 -m pip install pyopenssl
# python3 -m flask run --cert=adhoc

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

@app.route('/forum/ucp.php', methods=['POST'])
def login():
	return 'whatever you say'

@app.route('/forum/chat/', methods=['POST'])
def chat():
	with open('tiplanet.org.xml', encoding='utf-8') as xml_file:
		return xml_file.read()

if __name__ == "__main__":
	app.run(ssl_context='adhoc')
