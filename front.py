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


def main():
    st.sidebar.title("Menu")
    option = st.sidebar.radio("Navegar", ["Cadastro"])

    if option == "Cadastro":
        cadastro()
    

if __name__ == "__main__":
    main()