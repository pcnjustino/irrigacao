import network
import time
SSID='ssid'
PASSWORD='password'
def connect(SSID,PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('conectando a rede...')
        time.sleep(1)
        wlan.connect(SSID,PASSWORD)
        while not wlan.isconnected():
            pass
    print('Conectado......')
    print('network config:', wlan.ifconfig())
    
connect(SSID,PASSWORD)