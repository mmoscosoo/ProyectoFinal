import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# Variables para guardar el último mensaje recibido
st.set_page_config(page_title="Selector de Animal", page_icon=":paw_prints:")
if "last_animal" not in st.session_state:
    st.session_state.last_animal = None
    st.session_state.last_valor = None

# Función de callback al recibir mensaje
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        st.session_state.last_animal = data.get("animal")
        st.session_state.last_valor = data.get("valor")
    except Exception as e:
        st.session_state.last_animal = "Error"
        st.session_state.last_valor = str(e)

# Configurar el cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("broker.mqttdashboard.com", 1883, 60)
client.subscribe("selector/animal")
client.loop_start()

# Interfaz Streamlit
st.title("Visualizador de Animal por Potenciómetro")
st.write("Pulsa el botón para mostrar el animal seleccionado actualmente.")

if st.button("Ver Animal Actual"):
    st.info("Escuchando MQTT durante 3 segundos...")

    # Esperar y permitir que lleguen mensajes
    for _ in range(6):  # 6 ciclos de 0.5s = 3 segundos
        client.loop(timeout=0.5)
        time.sleep(0.5)

    # Mostrar el último mensaje recibido
    if st.session_state.last_animal:
        st.success(f"Animal seleccionado: *{st.session_state.last_animal}*")
        st.write(f"Valor del potenciómetro: {st.session_state.last_valor}")
    else:
        st.warning("No se recibió ningún dato durante la escucha.")
