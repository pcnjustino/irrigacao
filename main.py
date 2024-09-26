import connect
import urequests
from machine import Pin,ADC
from time import sleep
# Configurando a bomba
bomba=Pin(32,Pin.OUT)


# Configurando o sensor
sensor=ADC(Pin(34)) # Sensor conectado pino GPIO32
sensor.atten(ADC.ATTN_11DB)# Atenuação para ler até 3.3v
sensor.width(ADC.WIDTH_10BIT) # Resolução de 10 bits(0-1023)

# Função para ler umidade
def ler_umidade():
    valor_adc = sensor.read()  # Leitura do valor analógico
    umidade = 100-(valor_adc / 1023.0) * 100  # Converte o valor em porcentagem
    return umidade

# URL Database real time
FIREBASE_URL = 'https://esp-irrigacao-default-rtdb.firebaseio.com/dados.json'


#Função para enviar dados para firebase
def enviar_dados_firebase(umidade_solo, estado_bomba):
    dados = {
        'umidade': umidade_solo,
        'bomba': estado_bomba
    }
    try:
        response = urequests.put(FIREBASE_URL, json=dados)
        print('Dados enviados ao Firebase:', dados)
        print('Resposta do Firebase:', response.text)
        response.close()
    except Exception as e:
        print("Erro ao enviar dados:", e)
        
        
while True:
    umidade_solo = ler_umidade()
    print("Umidade do solo: {:1.0f}%".format(umidade_solo))
    sleep(2)  # Atraso de 2 segundos entre as leituras
    
    if umidade_solo >= 50.00:
        print('solo umido')
        bomba.value(0)
    else:
        print('solo seco')
        bomba.value(1)

    estado_bomba=bomba.value()
    
    enviar_dados_firebase(umidade_solo,estado_bomba)
 