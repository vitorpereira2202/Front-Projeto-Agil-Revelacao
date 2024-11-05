import streamlit as st
import pandas as pd
import requests

Base_url= "http://127.0.0.1:5000"

users = {}

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="password", key="signup_password")

    if st.button("Cadastrar"):
        if not email or not senha:
            st.error("Email e senha são obrigatórios.")
        else:
            user_data = {"email": email, "senha": senha}
            response = requests.post(f"{Base_url}/cadastro", json=user_data)
            
            if response.ok:  # Verifica se a resposta foi bem-sucedida
                st.success("Usuário cadastrado com sucesso!")
            else:
                try:
                    error_message = response.json().get('msg', 'Erro ao cadastrar.')
                except ValueError:  # Captura erro de decodificação JSON
                    error_message = response.text  # Usa o texto da resposta
                st.error(error_message) 
    
    st.markdown("""
        <style>
        button[kind="primary"] {
            background-color: black;
        }
        
        button {
            height: auto;
            padding-top: 10px !important;   
            padding-bottom: 10px !important;
            padding-left: 25px !important;
            padding-right: 25px !important;       
        }            
        </style>
    """, unsafe_allow_html=True)


def predios():
    st.title("Prédios")

    st.write("")  # Espaço vazio para ajudar na centralização

    # Botões centralizados
    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("Prédio 1", key='button1', type="primary"):
            st.session_state.page = "predio_1"
    with col2:
        if st.button("Prédio 2", key='button2', type="primary"):
            st.session_state.page = "predio_2"
    with col2:
        if st.button("Prédio 3", key='button3', type="primary"):
            st.session_state.page = "predio_3"

    st.markdown("""
        <style>
        button[kind="primary"] {
            background-color: black;
        }
        button {
            height: auto;
            padding-top: 25px !important;   
            padding-bottom: 25px !important;
            padding-left: 75px !important;
            padding-right: 75px !important;
            margin-top: 25px !important;
        }        
        </style>
    """, unsafe_allow_html=True)

def mostrar_salas(predio_id):
    # Dados de exemplo das salas divididas por andar
    salas = {
        "2º Andar": [
            {"nome": "Sala 1", "status": "DISPONIVEL"},
            {"nome": "Sala 2", "status": "INDISPONIVEL"},
            {"nome": "Sala 3", "status": "DISPONIVEL"},
            {"nome": "Sala 4", "status": "INDISPONIVEL"}
        ],
        "5º Andar": [
            {"nome": "Sala 1", "status": "DISPONIVEL"},
            {"nome": "Sala 2", "status": "DISPONIVEL"}
        ]
    }

    st.markdown("""
    <style>
        .sala {
            padding: 20px;
            color: black;
            font-weight: bold;
            border-radius: 5px;
            text-align: center;
            margin: 10px;
            width: 150px;
            height: 100px;
            display: inline-block;
        }
        .disponivel {
            background-color: #4CAF50;
        }
        .indisponivel {
            background-color: #F44336;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title(f"Prédio {predio_id}")
    for andar, salas_do_andar in salas.items():
        st.subheader(andar)
        for sala in salas_do_andar:
            status_class = "disponivel" if sala["status"] == "DISPONIVEL" else "indisponivel"
            st.markdown(
                f'<div class="sala {status_class}">{sala["nome"]}<br>{sala["status"]}</div>',
                unsafe_allow_html=True
            )

def predio_1():
    mostrar_salas(predio_id=1)

def predio_2():
    mostrar_salas(predio_id=2)

def predio_3():
    mostrar_salas(predio_id=3)

def Login():
    st.title("Login")

    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if not email or not senha:
            st.error("Email e senha são obrigatórios.")
        else:
            user_data = {"email": email, "senha": senha}
            response = requests.post(f"{Base_url}/login", json=user_data)
            
            if response.ok:  # Verifica se a resposta foi bem-sucedida
                st.success("Login bem-sucedido!")
            else:
                try:
                    error_message = response.json().get('msg', 'Erro ao fazer login.')
                except ValueError:
                    error_message = response.text
                st.error(error_message)

def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro", "Login", "Prédios"])

    if option == "Cadastro":
        cadastro()
        if 'page' in st.session_state:
            del st.session_state['page']
    elif option == "Prédios":
        predios()
        if 'page' in st.session_state:
            if st.session_state.page == "predio_1":
                predio_1()
            elif st.session_state.page == "predio_2":
                predio_2()
            elif st.session_state.page == "predio_3":
                predio_3()
    elif option == "Login":
        Login()

if __name__ == "__main__":
    main()
