import time as delay
from urllib.request import urlopen
import RPi.GPIO as gpio
import requests

gpio.setmode(gpio.BOARD)

ledVermelho = 11
ledVerde = 12
pin_t = 15
pin_e = 16
lixeira_v = 20

gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.output(ledVermelho, False)
gpio.output(ledVerde, False)

def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)
    tempo_i = delay.time()
    tempo_f = delay.time()

    while gpio.input(pin_e) == False:
        tempo_i = delay.time()
    while gpio.input(pin_e) == True:
        tempo_f = delay.time()

    tempo_d = tempo_f - tempo_i

    distancia = (tempo_d*34300)/2
    return distancia

def conexao():
    try:
        urlopen('https://materdei.edu.br/pt', timeout=1)
        return True
    except:
        return False

if conexao() == True:
    while True:
        consulta_t = requests.get("https://api.thingspeak.com/channels/2317864"
        + "/fields/4/last?key=GRZDARI8NL2H2HBQ")
        consulta_u = requests.get("https://api.thingspeak.com/channels/2317864"
        + "/fields/3/last?key=GRZDARI8NL2H2HBQ")
        consulta_lix = requests.get("https://api.thingspeak.com/channels/2317864"
        + "/fields/3/last?key=GRZDARI8NL2H2HBQ")

        print(float(consulta_t.text))
        print(float(consulta_lix.text))
        delay.sleep(20)

        valorRecebido = distancia()
        print("Distancia = %.1f CM" % valorRecebido)
        espaco_d = (valorRecebido/float(consulta_lix.text))*100
        print("Espaço disponível na lixeira = %.1f" % espaco_d, '%')
        espaco_o = 100 - espaco_d
        print("Espaço ocupado na lixeira = %.1f" % espaco_o, '%')
        delay.sleep(5)

else:
    print("Sem conexão")