import streamlit as st
import pandas as pd
import requests

Base_url= "http://127.0.0.1:5000"

users = {}

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Senha", type="password", key="signup_password")
    

    if st.button("Cadastrar"):
        if email in users:
            st.error("Email já cadastrado.")
        else:
            users[email] = password
            st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
            st.session_state["signup_success"] = True


def predios():
    st.title("Predios")


        # # Cria um espaço vazio antes do botão para centralizá-lo
    st.write("")  # Espaço vazio para ajudar na centralização

    # Botões
    col1, col2, col3 = st.columns(3)

    with col2:  # Centraliza o botão na segunda coluna
        if st.button("Prédio 1", key='button1'):
            st.session_state.page = "predio_1"

    # Outro botão, se necessário
    with col2:  # Coloca o próximo botão na mesma coluna
        if st.button("Prédio 2", key='button2'):
            st.session_state.page = "predio_2"
    
    with col2:  # Coloca o próximo botão na mesma coluna
        if st.button("Prédio 3", key='button3'):
            st.session_state.page = "predio_3"
 

def predio_1():
    st.title("Prédio 1")
    st.write("Detalhes do Prédio 1")
    email = st.text_input("Email", key="signup_email")

def predio_2():
    st.title("Prédio 2")
    st.write("Detalhes do Prédio 2")
    email = st.text_input("Email", key="signup_email")

def predio_3():
    st.title("Prédio 3")
    st.write("Detalhes do Prédio 3")
    email = st.text_input("Email", key="signup_email")

def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro", "Predios"])

    # Renderiza a página de acordo com o estado da sessão
    if option == "Cadastro":
        cadastro()
        # Redefine a página para evitar que os prédios apareçam na tela de cadastro
        if 'page' in st.session_state:
            del st.session_state['page']
    elif option == "Predios":
        predios()

        # Renderiza a página de acordo com o estado da sessão
        if 'page' in st.session_state:
            if st.session_state.page == "predio_1":
                predio_1()
            elif st.session_state.page == "predio_2":
                predio_2()
            elif st.session_state.page == "predio_3":
                predio_3()

if __name__ == "__main__":
    main()