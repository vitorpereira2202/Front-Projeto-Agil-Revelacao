import streamlit as st
import pandas as pd
import requests as rq

Base_url= "http://127.0.0.1:5000"

users = {}

def fetch_data(endpoint):
    try:
        response = rq.get(f'{Base_url}/{endpoint}')
        response.raise_for_status()
        return response.json()
    except rq.exceptions.HTTPError as err:
        st.error(f"Erro ao acessar {endpoint}: {err}")
        return None

def display_table(data):
    if data:
        st.table(data)

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="password", key="signup_password")

    if st.button("Cadastrar"):
        if email in users:
            st.error("Email já cadastrado.")
        else:
            users[email] = senha
            st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
            st.session_state["signup_success"] = True


def predios():
    st.title("Predios")


        # # Cria um espaço vazio antes do botão para centralizá-lo
    st.write("")  # Espaço vazio para ajudar na centralização

    # Botões
    col1, col2, col3 = st.columns(3)

    with col2:  # Centraliza o botão na segunda coluna
        if st.button("Prédio 1", key='button1', type="primary"):
            st.session_state.page = "predio_1"

    # Outro botão, se necessário
    with col2:  # Coloca o próximo botão na mesma coluna
        if st.button("Prédio 2", key='button2', type="primary"):
            st.session_state.page = "predio_2"
    
    with col2:  # Coloca o próximo botão na mesma coluna
        if st.button("Prédio 3", key='button3', type="primary"):
            st.session_state.page = "predio_3"

    st.markdown("""
        <style>
         button[kind="primary"] {
        background-color: Black;
        }

        button[kind="seondary"] {
            background-color: Grey;
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
   

def predio_1():
    st.title("Prédio 1")
    predio = fetch_data('predios/p1')
    display_table(predio)
    

def predio_2():
    st.title("Prédio 2")
    st.write("Detalhes do Prédio 2")    
    predio = fetch_data('predios/p2')
    display_table(predio)

def predio_3():
    st.title("Prédio 3")
    st.write("Detalhes do Prédio 4")
    predio = fetch_data('predios/p4')
    display_table(predio)

def Login():
    st.title("Login")

    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if senha not in users:
            st.error("Usuário não cadastrado.")
        elif users[email] != senha:
            st.error("Senha incorreta.")
        else:
            st.success("Login realizado com sucesso!")
            st.session_state["logged_in"] = True 


def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro", "Login", "Predios"])


    if option == "Cadastro":
        cadastro()

        
        if 'page' in st.session_state:
            del st.session_state['page']
    elif option == "Predios":
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