📘 EdgeBreak – Monitoramento Inteligente de Postura e Ambiente (ESP32 + MQTT)
Global Solution 2025 – O Futuro do Trabalho
FIAP – Edge Computing / WorkVerse

👥 Integrantes:
Diego Bondezan Yonamine - RM562013
Felipe madeira - RM563521
Matheus Gomes - RM562277

link do video do youtube: 
link do wokwi: https://wokwi.com/projects/448004154431471617
repositorio github: 

📌 1. Introdução

O trabalho remoto e híbrido trouxe impactos diretos na saúde física e mental dos profissionais. Má postura, ambientes inadequados e longos períodos contínuos de trabalho contribuem para dores, fadiga e queda de produtividade.
O EdgeBreak é uma solução IoT criada para o futuro do trabalho:
📡 monitora temperatura, umidade e postura,
⚙️ executa lógica inteligente no próprio ESP32 (Edge Computing),
➡️ envia dados para o Node-RED via MQTT,
🔔 sugere pausas automáticas por meio de LED e buzzer,
🖱 permite ativar/desativar alertas via botão físico ou comandos externos.



🎯 2. Objetivo da Solução

- Criar um sistema inteligente que:

- Detecta condições de risco (má postura, calor, umidade alta)

- Gera alertas locais (LED + buzzer)

- Comunica dados em tempo real via MQTT

- Interage com dashboards e automações no Node-RED

- Demonstra como IoT e Edge Computing podem melhorar o bem-estar e a produtividade no ambiente de trabalho



🧩 3. Tecnologias Utilizadas

- Hardware / Simulação

- ESP32

- Sensor DHT22 (temperatura e umidade)

- Potenciômetro (simulação de postura)

- LED

- Buzzer

- Botão

- Wokwi (simulação)

SOFTWARE

- MicroPython

- MQTT (HiveMQ Broker)

- Node-RED

- Dashboard (opcional)

- Wokwi IoT Cloud Simulation



📡 4. Arquitetura da Solução
[ Sensores ]
   |  (DHT22 + Potenciômetro)
   ↓
[ ESP32 com lógica Edge ]
   - Análise de risco
   - Alertas locais
   - Publicação MQTT
   - Comandos via Serial / Node-RED
   ↓
[ Broker MQTT (HiveMQ) ]
   ↓
[ Node-RED Dashboard ]
   - Gráficos
   - Indicadores
   - Comandos remotos



📊 5. Lógica de Funcionamento
🔍 Leitura de Sensores

- Temperatura e umidade → DHT22

- Postura → valores do potenciômetro normalizados (0 a 1)

⚠️ Detecção de Condições Críticas

Um alerta é ativado quando:

Condição	Descrição
temp > 29°C	Ambiente desconfortável / risco de fadiga
postura > 0.7	Postura inadequada / risco ergonômico

🔔 Alertas Locais

- LED acende

- Buzzer apita

- Mensagem MQTT com status ALERTA

🔘 Botão Físico

Pressão ativa/desativa todos os alertas (modo silencioso).

🖥 Comandos Externos (Node-RED via Serial)

- led_on / led_off

- buzzer_on / buzzer_off

- alerta_toggle



📤 6. Publicação MQTT
Broker
broker.hivemq.com
porta: 1883


Tópico Principal
ESP32_EdgeBreak


Formato da Mensagem
TEMP:27.5;HUM:60.0;POST:0.42;STATUS:NORMAL


Status possíveis

- NORMAL

- ALERTA

- DESATIVADO

- ERRO_SENSOR



⚙️ 7. Código-Fonte (MicroPython)

O código completo está no arquivo:
edgebreak_mqtt.py
(exatamente o código que você enviou, sem alterações)



🌍 8. Impacto e Futuro

O EdgeBreak contribui para ambientes de trabalho:

- Mais saudáveis

- Mais produtivos

- Com detecção precoce de riscos

- Integrados à automação inteligente

- Preparados para o futuro do trabalho

Possíveis expansões:

- IA para análise de padrões

- Histórico de dados no FIWARE ou InfluxDB

- Sensores de luminosidade e ruído

- App mobile para notificações

📄 9. Licença

Este projeto é de uso educacional para a Global Solution FIAP 2025.
Licença MIT opcional.

✔️ README Finalizado

Quando você me mandar:
✔ link do Wokwi
✔ link do vídeo
✔ nomes dos integrantes

Eu atualizo tudo automaticamente e deixo 100% pronto para seu GitHub.