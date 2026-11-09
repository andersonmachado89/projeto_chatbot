# Passo a passo:
# 1 - Título
# 2 - Input do chat
# 3 - A cada mensagem enviada:
    # Mostrar a mensagem do usuario enviou no chat
    # Enviar essa mensagem para a IA responder
    # Aparece na tela a resposta da IA
# Streamlit - Frontend e Backend

import streamlit as st
import ollama

st.set_page_config(page_title="Chatbot Local", page_icon="🤖")

MODELO = "qwen3.5:2b"

if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configurações")
    prompt_sistema = st.text_area(
        "Personalidade da IA",
        "Você é um assistente útil e responde sempre em português.",
    )
    if st.button("🗑️ Limpar conversa", use_container_width=True):
        st.session_state["lista_mensagens"] = []
        st.rerun()

    historico = "\n\n".join(
        f"{m['role']}: {m['content']}" for m in st.session_state["lista_mensagens"]
    )
    st.download_button("💾 Baixar conversa", historico, "conversa.txt")

# Cabeçalho
st.title("🤖 Chatbot Local")
st.caption(f"Rodando localmente com Ollama • {MODELO}")

# Histórico
for msg in st.session_state["lista_mensagens"]:
    avatar = "🤖" if msg["role"] == "assistant" else "🧑"
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

# Streaming da resposta
def gerar_resposta():
    mensagens = [{"role": "system", "content": prompt_sistema}] + st.session_state["lista_mensagens"]
    stream = ollama.chat(
        model=MODELO,
        messages=mensagens,
        think=False,
        stream=True,
    )
    for chunk in stream:
        yield chunk.message.content or ""

mensagem_usuario = st.chat_input("Escreva sua mensagem aqui")

if mensagem_usuario:
    st.chat_message("user", avatar="🧑").write(mensagem_usuario)
    st.session_state["lista_mensagens"].append({"role": "user", "content": mensagem_usuario})

    with st.chat_message("assistant", avatar="🤖"):
        resposta_ia = st.write_stream(gerar_resposta())

    st.session_state["lista_mensagens"].append({"role": "assistant", "content": resposta_ia})