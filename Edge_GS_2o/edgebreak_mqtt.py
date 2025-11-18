# =====================================================
# EdgeBreak - Versão MQTT (para Node-RED)
# Autor: Diego Bondezan
# Projeto: Global Solution 2025 - WorkVerse / Edge Computing
# Objetivo: Monitorar postura e ambiente, sugerindo pausas automáticas,
#           com comunicação via MQTT (Node-RED).
# =====================================================

import machine
import time
import dht
import sys
import select
import network
from umqtt.simple import MQTTClient

# ==== CONFIGURAÇÃO DE REDE (Wi-Fi) ====
SSID = "Wokwi-GUEST"       # ou o nome da sua rede Wi-Fi real
PASSWORD = ""              # Wokwi-GUEST não tem senha

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando ao Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        tentativas = 0
        while not wlan.isconnected() and tentativas < 10:
            time.sleep(1)
            tentativas += 1
    if wlan.isconnected():
        print("✅ Conectado ao Wi-Fi:", wlan.ifconfig())
        return True
    else:
        print("❌ Falha ao conectar ao Wi-Fi.")
        return False

# ==== CONFIGURAÇÃO DOS PINOS ====
sensor_dht = dht.DHT22(machine.Pin(4))
pot = machine.ADC(machine.Pin(34))
pot.atten(machine.ADC.ATTN_11DB)
led = machine.Pin(2, machine.Pin.OUT)
buzzer = machine.Pin(25, machine.Pin.OUT)
botao = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

# ==== CONFIGURAÇÃO MQTT ====
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "ESP32_EdgeBreak_Client"
TOPIC_DATA = b"ESP32_EdgeBreak"

# ==== VARIÁVEIS DE CONTROLE ====
alertas_ativos = True
client = None

# ==== CONEXÃO MQTT ====
def conectar_mqtt():
    global client
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print("✅ Conectado ao broker MQTT!")
    except Exception as e:
        print("❌ Falha ao conectar ao MQTT:", e)
        time.sleep(3)
        conectar_mqtt()

# ==== FUNÇÕES DE SENSOR E ALERTA ====
def ler_sensores():
    """Lê temperatura, umidade e postura"""
    try:
        sensor_dht.measure()
        temperatura = sensor_dht.temperature()
        umidade = sensor_dht.humidity()
        postura = pot.read() / 4095  # normaliza entre 0 e 1
        return temperatura, umidade, postura
    except Exception as e:
        print(f"Erro DHT22: {e}")
        return None, None, None

def verificar_condicoes(temp, umid, postura):
    """Verifica se há risco de fadiga e aciona alerta"""
    global alertas_ativos

    if not alertas_ativos:
        led.off()
        buzzer.off()
        return "DESATIVADO"

    if temp is None or umid is None:
        return "ERRO_SENSOR"

    if temp > 29 or postura > 0.7:
        led.on()
        buzzer.on()
        return "ALERTA"
    else:
        led.off()
        buzzer.off()
        return "NORMAL"

def checar_botao():
    """Botão para ativar/desativar alertas"""
    global alertas_ativos
    if botao.value() == 0:
        alertas_ativos = not alertas_ativos
        estado = "ativados" if alertas_ativos else "desativados"
        print(f"🔘 Alertas {estado}")
        time.sleep(0.5)

def receber_comando():
    """Recebe comandos do Node-RED via Serial"""
    global alertas_ativos
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        comando = sys.stdin.readline().strip().lower()
        if comando == "led_on":
            led.on()
        elif comando == "led_off":
            led.off()
        elif comando == "buzzer_on":
            buzzer.on()
        elif comando == "buzzer_off":
            buzzer.off()
        elif comando == "alerta_toggle":
            alertas_ativos = not alertas_ativos
            print(f"Alertas {'ativados' if alertas_ativos else 'desativados'}")

# ==== INICIALIZAÇÃO ====
print("Iniciando EdgeBreak - Modo MQTT para Node-RED")
time.sleep(2)

if not conectar_wifi():
    sys.exit()

conectar_mqtt()

# ==== LOOP PRINCIPAL ====
while True:
    try:
        checar_botao()
        temp, umid, postura = ler_sensores()
        status = verificar_condicoes(temp, umid, postura)

        if temp is not None:
            msg = f"TEMP:{temp:.1f};HUM:{umid:.1f};POST:{postura:.2f};STATUS:{status}"
            print(msg)
            try:
                client.publish(TOPIC_DATA, msg)
            except Exception as e:
                print("Erro ao publicar MQTT:", e)
                conectar_mqtt()

        # Leitura de comandos (Serial)
        try:
            receber_comando()
        except Exception:
            pass

        time.sleep(5)

    except OSError as e:
        print("⚠ Erro de conexão MQTT:", e)
        conectar_mqtt()
