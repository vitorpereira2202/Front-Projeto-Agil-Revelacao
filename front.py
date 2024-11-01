import streamlit as st
import pandas as pd
import requests

# Conectando arquivo CSS

with open("style.css") as f:
    st.markdown(f"<style> {f.read()}</style>", unsafe_allow_html = True)

Base_url= "http://127.0.0.1:5000"

users = {}
st.button("Botão de teste")


def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="password", key="signup_password")
    cadastrar = st.button("Cadastrar") # pensei em nomear os botoes para poder editar cada um

    if cadastrar:
        if email in users:
            st.error("Email já cadastrado.")
        else:
            users[email] = senha
            st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
            st.session_state["signup_success"] = True


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

def predio_um():
    st.title("Térreo - Biblioteca")




def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro", "Login"])

    if option == "Cadastro":
        cadastro()
    elif option == "Login":
        Login()
    

if __name__ == "__main__":
    main()