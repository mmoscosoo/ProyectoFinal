import streamlit as st
import paho.mqtt.client as mqtt
import json

# Configuración inicial de la página
st.set_page_config(page_title="Selector de Animal", page_icon=":paw_prints:")

# Guarda el último mensaje recibido
if "last_payload" not in st.session_state:
    st.session_state.last_payload = None

# Función que se llama cuando llega un mensaje MQTT
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        st.session_state.last_payload = data
    except Exception as e:
        st.session_state.last_payload = {"error": str(e)}

# Crear un cliente MQTT singleton
@st.experimental_singleton
def get_mqtt_client():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("broker.mqttdashboard.com", 1883, 60)
    client.subscribe("selector/animal")
    client.loop_start()
    return client

# Iniciar MQTT
get_mqtt_client()

# Interfaz de Streamlit
st.title("Visualizador de Animal por Potenciómetro")
st.write("Pulsa el botón para mostrar el último valor recibido del ESP32.")

if st.button("Ver Animal Actual"):
    if st.session_state.last_payload:
        data = st.session_state.last_payload
        if "error" in data:
            st.error(f"Error al procesar JSON: {data['error']}")
        else:
            st.success(f"Animal seleccionado: *{data['animal']}*")
            st.write(f"Valor del potenciómetro: {data['valor']}")
    else:
        st.warning("Esperando datos del ESP32...")
