from flask import Flask, render_template, json, request , redirect,url_for, session
from pprint import pprint
from custom_socketserver.go import Go
import asyncio, sys
import time

#host = 'localhost'
#port = 3010
app = Flask(__name__)
app.secret_key = 'secret_key'
 


@app.route('/config',methods=['GET','POST'])
def config():
    ip = session['ip']
    port = session['port']
    print(" ip y puerto cambiado: " + ip + ":"+ port)
    return render_template('/config.html',ip=ip,port=port)

@app.route('/dataconfig',methods=['GET','POST'])
def dataconfig():
    print("el request esssss:" + request.method)
    
    ip = request.form.get('ip')
    port = request.form.get('port')
    session['ip'] = ip
    session['port'] = port
 
    return redirect(url_for('config'))

@app.route('/')
def home():
    session['ip'] ="172.17.0.1"
    session['port'] = "3010"
    ip = session['ip']
    port = session['port']
    print(" ip y puerto por defecto: " + ip + ":"+ port)
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
    ip = session['ip']
    port = session['port']
    # llamada asincrona
    header, data = loop.run_until_complete(
        Go('POST', '/signup', host_port = (ip, int(port)), body=body).as_coroutine()
    )

    print(data, file=sys.stderr)
    
    # Creo que es adecuado cerrar el loop al finalizar el handler
    if (loop.is_running()):
        loop.stop()
    loop.close()
    jsonSingUp = json.dumps(data)

    return "registro exitoso"

@app.route('/logout',methods=['GET','POST'])
def logout():
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
    ci = session['data']['user']['ci']
    email = session['data']['user']['ci']
    token = session['token']
    body = {
        'ci': int(ci),
        'email': email,
        'token':token
	}   
    
    # llamada asincrona
    ip = session['ip']
    port = session['port']
    header, data = loop.run_until_complete(
        Go('POST', '/logout', host_port = (ip,int(port)), body=body).as_coroutine()
    )
    print("logaout"+ str(data))
    # Creo que es adecuado cerrar el loop al finalizar el handler
    if (loop.is_running()):
        loop.stop()
    loop.close()
    return redirect(url_for('home'))
  
 


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
    ip = session['ip']
    port = session['port']
    header, data = loop.run_until_complete(
        Go('POST', '/signin', host_port = (ip, int(port)), body=body).as_coroutine()
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
        ip = session['ip']
        port = session['port']
        resheader, resbody = loop.run_until_complete(
            Go('GET', '/tests/user', host_port = (ip, int(port)), body=body).as_coroutine()
        )
        tests = resbody.get('tests')
        pprint(resbody.get('tests'))
        jsonGetTest = json.dumps(resbody)
        DecoGetTest  = json.loads(jsonGetTest)
        pprint
        #dando formato a fechar
        for test in tests:
            inscription_start = time.localtime(test['inscription_start'])
            inscription_start_f = time.strftime("%Y-%m-%d %H:%M:%S", inscription_start)
            inscription_end = time.localtime(test['inscription_end'])
            inscription_end_f = time.strftime("%Y-%m-%d %H:%M:%S", inscription_end)

            test_end = time.localtime(test['test_end'])
            test_end_f = time.strftime("%Y-%m-%d %H:%M:%S", test_end)

            test_start = time.localtime(test['test_end'])
            test_start_f = time.strftime("%Y-%m-%d %H:%M:%S", test_start)

            
            test['inscription_start'] = inscription_start_f
            test['inscription_end'] = inscription_end_f
            test['test_end'] = test_end_f
            test['test_start'] = test_start_f

        
        for test in tests:   
            idtest = test['id']
            status_onroll = False
            if request.method == 'POST':
                btn_onroll= request.form['btn_onroll']
                
                print("btn_onroll", btn_onroll ,idtest )
                if int(btn_onroll) == idtest:
                    onroll(token,idtest)
                    try:
                        print("inscripcion para",idtest,onroll(token,idtest)['error_code'] ) 
                        if(str(onroll(token,idtest)['error_code']) == "user-already-enrolled") or (str(onroll(token,idtest)['message']==True)):
                            status_onroll = True
                            print("inscrito",status_onroll )
                            
                            
                    except KeyError: 

                        if(str(onroll(token,idtest)['error_code']) == "enrolment-period-missed"):
                            status_onroll = False
                            print("no inscrito",status_onroll )
                            test['userHasEnrrolled'] = status_onroll

                    print("status inscrito",status_onroll ) 
                    if status_onroll:
                        print("prueba activa")   
                        test = test['type']
                        return redirect(url_for('pres',idtest=idtest  ))
                    else: 
                        print("prueba inactiva")   
                
                
        #pprint(resbody.get('tests'))
                    

        if (loop.is_running()):
            loop.stop()
        loop.close()


        return render_template('main.html',name=name,lastName = lastName, tests=tests ) 
    else:
        if (loop.is_running()):
            loop.stop()
        loop.close()
        return redirect(url_for('home') )

def onroll(token,idtest):
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()

    body = {
        'token': token,
        'test_id': idtest
        }
    ip = session['ip']
    port = session['port']
    resheader, resbody = loop.run_until_complete(
        Go('POST', '/tests/user/enroll', host_port = (ip, int(port)), body=body).as_coroutine()
        )

    if (loop.is_running()):
        loop.stop()
        loop.close()
    
    return resbody
@app.route('/pres',methods=['GET','POST'])
def pres():
    idtest=request.args.get('idtest')
    print(str(idtest))
    if request.method == 'POST':
        btn_accept= request.form['btn_accept']   
        print("hollaaaas",btn_accept)
        return redirect(url_for('test',idtest=1 ))
    return render_template('/presentar.html',idtest=idtest)


@app.route('/newtest',methods=['GET','POST'])
def test():
    loop = None
    
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
        
    if 'token' in session:
        token = session['token']
    
    idtest=request.args.get('idtest')
    print('parametro id',idtest)
    body = {
        'token': token,
        'test_id': int(idtest),
        'location_code': 'LOC_HUM_1'
        }
    ip = session['ip']
    port = session['port']
    resheader, resbody = loop.run_until_complete(
        Go('GET', '/tests/new', host_port = (ip, int(port)), body=body).as_coroutine()
        )
    if (loop.is_running()):
        loop.stop()
        loop.close()

   
    
    try:
        ## se crear una variable de secion para pasar la data cuando redirecciona al main
        global test 
        test = resbody["test"]
        if str(resbody["test"]):
            print ("prueba",idtest , test)
            
            return render_template('test.html',test=test)


    except KeyError:
        if str(resbody["error_code"]) == "test-already-generated":
            print ( test)
            return render_template('test.html',test=test)
        if str(resbody["error_code"]) == "wrong-location-code":
            return str(resbody["error_code"])
    print ("prueba",idtest)
    
@app.route('/result',methods=['GET','POST'])
def result():
   
    
    loop = None
    idtest = request.form['idtest']
    point = request.form['point']
    select_quest_1 = request.form['1']
    select_quest_2 = request.form['2']
    select_quest_3 = request.form['3']
    select_quest_4 = request.form['4']
    select_quest_5 = request.form['5']
    
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
        
    if 'token' in session:
        token = session['token']
    
    
    
    body = {
        'token': token,
        'test_id':int(idtest),
        'location_code': 'LOC_HUM_1',
        'answers': [int(select_quest_1),int(select_quest_2),int(select_quest_3),int(select_quest_4),int(select_quest_5)]
        }
    ip = session['ip']
    port = session['port']
    resheader, resbody = loop.run_until_complete(
        Go('POST', '/results', host_port = (ip, int(port)), body=body).as_coroutine()
        )
    
    get_results(token,idtest)
    result = get_results(token,idtest)
    if (loop.is_running()):
        loop.stop()
        loop.close()
    
    #return "resultados " + point + idtest +str(resbody) + "Evaluacion de resultados"+ str(evaluateResult(token,idtest))
    return render_template('result.html', result=result)
def get_results(token,idtest):
    loop = None
    try:
        # chequeo si hay un loop corriendo
        loop = asyncio.get_event_loop()
    except Exception:
        loop = asyncio.new_event_loop()
        
    if 'token' in session:
        token = session['token']
    print("evaluate token" + token)
    print("evaluate id" + idtest)
    body = {
        'token': token,
        'test_id':int(idtest),
        
        }
    ip = session['ip']
    port = session['port']
    resheader, resbody = loop.run_until_complete(
        Go('GET', '/results/test', host_port = (ip, int(port)), body=body).as_coroutine()
        )
    if (loop.is_running()):
        loop.stop()
        loop.close()
    return resbody

app.run(host='localhost', port=4010 ,debug =True)    