from flask import Flask, render_template, json, request
from pprint import pprint
from custom_socketserver.go import Go
import asyncio

host = 'localhost'
port = 3010

   
async def async_singin(ci,email):
    def cb():
        print('RESULT ----------')
        print('body:')
        print(body)
        print('----------')
    
    body = {
        'ci': int(ci),
        'email': email,
    }
    
    Go('POST', '/signin', host_port = (host, port), body=body).with_callback(cb)
    #jsonSingUp = json.dumps(body)
    #print("json"+ jsonSingUp)
    
def fight(responses):
    return "Why can't we all just get along?"

async def async_singup(ci,email,phone,name,lastName):
    
    def cb(fut):
        print('RESULT ----------')
        print(body)
        print('----------')

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImNpIjoyMjU0MDgyMCwiZW1haWwiOiJlcmljQG1haWwuY29tIn0sImV4cCI6MTU3MjQ2MzA5Mn0.37RYLjikjTol0wRKfoxMGlIdQe8B2nlUcLDaVkmoOCI'

    body = {
    'ci': int(ci),
    'email': email,
    'phone': phone,
    'name': name,
    'last_name': lastName
    
    }

    Go('POST', '/signup', host_port = (host, port), body=body).with_callback(cb)
    
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup',methods=['POST'])
def signup():
    # create user code will be here !!
    ci = request.form['inputCi']
    email = request.form['inputEmail']
    phone = request.form['inputPhone']
    name = request.form['inputName']
    lastName= request.form['inputlastName']
    
    # create json for singUp
    loop.run_until_complete(async_singup(ci,email,phone,name,lastName))
    
    return "SingUp"
@app.route('/signin',methods=['POST'])
def signin():
    # INIT LOOP
    # hago la inicialización del loop aquí por que, no se de que forma manejan
    # los hilos, entonces, creo que es un poco mpas seguro de esta forma
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()

    ci = request.form['inputCi']
    email = request.form['inputEmail']
    
    body = {
        'ci': ci,
        'email': email,
	}
    
    # llamada asincrona
    header, body = loop.run_until_complete(
        Go('POST', '/signin', host_port = (host, port), body=body).as_coroutine()
    )
    
    # Creo que es adecuado cerrar el loop al finalizar el handler
    if (loop.is_running()):
        loop.stop()
    loop.close()

    return body
    
    

app.run(host='localhost', port=4000 ,debug =True)    
