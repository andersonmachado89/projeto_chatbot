# Passo a passo:
# 1 - Título
# 2 - Input do chat
# 3 - A cada mensagem enviada:
    # Mostrar a mensagem do usuario enviou no chat
    # Enviar essa mensagem para a IA responder
    # Aparece na tela a resposta da IA
# Streamlit - Frontend e Backend

import streamlit as st
from openai import OpenAI     
import os
from dotenv import load_dotenv

# Oculte a barra de código
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    #fileMenu {visibility: hidden;}
    #sidebarContainer {visibility: hidden;}
    .sidebar {visibility: hidden;}
    .viewerBadge_link__1S137 {display: none;}
    </style>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("OPENAI_KEY")  

modelo = OpenAI(api_key=API_KEY)

st.write("Chatbot do Anderson com IA")

# session_state = memoria do streamlit
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []
    
#Adicionar uma mensagem
#st.session_state["lista_mensagens"] = []

#Exibir o histórico de mensagens
for msg in st.session_state["lista_mensagens"]:
    chave = msg["role"]
    texto = msg["content"] 
    st.chat_message(chave).write(texto)

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

if mensagem_usuario:
    # user -> Ser humano
    # assistant -> Inteligência Artificial
    st.chat_message("user").write(mensagem_usuario)
    mensagem = {"role":"user", "content":mensagem_usuario}
    st.session_state["lista_mensagens"].append(mensagem)
    
    #Resposta da IA
    resposta_modelo = modelo.chat.completions.create(
        messages=st.session_state["lista_mensagens"],
        model="gpt-4o"
    )
    
    resposta_ia = resposta_modelo.choices[0].message.content
    
    #Exibir a IA na tela
    st.chat_message("ai").write(resposta_ia)    
    mensagem_ia = {"role":"assistant", "content":resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)
    
    #print(st.session_state["lista_mensagens"])