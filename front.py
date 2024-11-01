import streamlit as st
import pandas as pd
import requests

Base_url= "http://127.0.0.1:5000"

users = {}

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="senha", key="signup_senha")

    if st.button("Cadastrar"):
        if email in users:
            st.error("Email já cadastrado.")
        else:
            users[email] = senha
            st.success("Usuário cadastrado com sucesso! Agora você pode fazer login.")
            st.session_state["signup_success"] = True


def Login():
    st.title("Login")

    Email = st.text_input("Email", key="login_email")
    Password = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        if Email not in users:
            st.error("Usuário não cadastrado.")
        elif users[Email] != Password:
            st.error("Senha incorreta.")
        else:
            st.success("Login realizado com sucesso!")
            st.session_state["logged_in"] = True 


def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro", "Login"])

    if option == "Cadastro":
        cadastro()
    elif option == "Login":
        Login()
    

if __name__ == "__main__":
    main()