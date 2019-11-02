from flask import Flask, render_template, json, request , redirect,url_for, session
from pprint import pprint
from custom_socketserver.go import Go
import asyncio, sys

host = 'localhost'
port = 3010
app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup',methods=['POST'])
def signup():

    print('--> HIT', file=sys.stderr)
     # INIT LOOP
    # hago la inicialización del loop aquí por que, no se de que forma manejan
    # los hilos, entonces, creo que es un poco mpas seguro de esta forma
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
    # create user code will be here !!
    ci = request.form['inputCi']
    email = request.form['inputEmail']
    phone = request.form['inputPhone']
    name = request.form['inputName']
    lastName= request.form['inputlastName']

    body = {
        'ci': int(ci),
        'email': email,
        'phone': phone,
        'name': name,
        'last_name': lastName
    
    }
    
    # llamada asincrona
    header, data = loop.run_until_complete(
        Go('POST', '/signup', host_port = (host, port), body=body).as_coroutine()
    )

    print(data, file=sys.stderr)
    
    # Creo que es adecuado cerrar el loop al finalizar el handler
    if (loop.is_running()):
        loop.stop()
    loop.close()
    jsonSingUp = json.dumps(data)

    return "registro exitoso"
    


@app.route('/signin',methods=['GET','POST'])
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
        'ci': int(ci),
        'email': email,
	}
    
    # llamada asincrona
    header, data = loop.run_until_complete(
        Go('POST', '/signin', host_port = (host, port), body=body).as_coroutine()
    )
    
    # Creo que es adecuado cerrar el loop al finalizar el handler
    if (loop.is_running()):
        loop.stop()
    loop.close()
    jsonSingin = json.dumps(data)
    DecoSingin = json.loads(jsonSingin)
    try:
        ## se crear una variable de secion para pasar la data cuando redirecciona al main
        data =DecoSingin
        token = str(DecoSingin["user"]['session_token'])
        session['token'] = token
        session['data'] = data
        return redirect(url_for('main') )

    except KeyError:
        token = str(DecoSingin["error_code"])
        return token

@app.route('/main',methods=['GET','POST'])
def main():
    # INIT LOOP
    # hago la inicialización del loop aquí por que, no se de que forma manejan
    # los hilos, entonces, creo que es un poco mpas seguro de esta forma
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()

    ## esto es para bloquear las vistas si no esta logueado
    if 'token' in session:
        token = session['token']
        data = session['data']
        name = str(data["user"]['name'])
        lastName = str(data["user"]['last_name'])
        
        body = {
            'token': token,
        }

        resheader, resbody = loop.run_until_complete(
            Go('GET', '/tests/user', host_port = (host, port), body=body).as_coroutine()
        )
        pprint(resbody.get('tests')[0])

        if (loop.is_running()):
            loop.stop()
        loop.close()

        return render_template('main.html',name=name,lastName = lastName ) 
    else:
        if (loop.is_running()):
            loop.stop()
        loop.close()
        return redirect(url_for('home') )

app.run(host='localhost', port=4000 ,debug =True)    