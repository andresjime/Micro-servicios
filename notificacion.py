import os
from twilio.rest import Client
from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app =Flask(__name__)

#crear una url base para nuestros servicios
@app.route('/')
def inicio():
    twilio_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    return  twilio_sid


# servicio de envio de textos
@app.route('/sms')
def sms():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # numeros y mensajes dinamicos

    mensaje = request.args.get('mensaje')
    destino = "+57" + request.args.get('telefono')
   
    message = client.messages \
                    .create(
                        body=mensaje,
                        from_='+16812488430',
                        to= destino
                    )

    print(message.sid)
    return 'mensaje enviado de manera exitosa'


#Servicios de envio de correos electronicos con sendgrid
@app.route('/enviar-correo')
def enviarCorreo():
    #sendgrid_key= os.environ['SENDGRID_API_KEY']
    message = Mail(
    from_email='acamilojimenez@mail.uniatlantico.edu.co', # verify sender
    to_emails=request.args.get('correo'),
    subject=request.args.get('asunto'),
    html_content= request.args.get('mensaje'))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return 'El correo fue enviado de manera exitosa'
    except Exception as e:
        print(e.message)
        return 'No se pudo enviar el correo electronico'

if __name__=='__main__':
    app.run()