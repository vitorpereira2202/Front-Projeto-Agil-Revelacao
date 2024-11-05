import streamlit as st
import pandas as pd
import requests

# 
Base_url= "http://127.0.0.1:5000"

users = {}


def fetch_data(endpoint):
    try:
        response = requests.get(f'{Base_url}/{endpoint}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        st.error(f"Erro ao acessar {endpoint}: {err}")
        return None

def display_table(data):
    if data:
        st.table(data)

def cadastro():
    st.title("Cadastro")

    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="password", key="signup_password")

    if st.button("Cadastrar",type='primary'):
        if email in users:
            st.error("Email já cadastrado.")
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
def renderizar_aquarios(dados_predio, nome_predio):
    st.title(f"Prédio {nome_predio}")
    
    # CSS para estilizar apenas os aquários e andares
    st.markdown("""
        <style>
        .aquario-card {
            display: inline-block;
            padding: 20px;
            margin: 10px;
            width: 120px;
            height: 80px;
            text-align: center;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
        .disponivel {
            background-color: #4CAF50; /* Verde */
        }
        .indisponivel {
            background-color: #F44336; /* Vermelho */
        }
        .andar-header {
            background-color: #e0e0e0;
            padding: 10px;
            text-align: center;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 5px;
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    for andar_info in dados_predio:
        andar = andar_info['andar']
        aquarios = andar_info['aquarios']
        
        # Cabeçalho do andar
        st.markdown(f'<div class="andar-header">Andar {andar}º</div>', unsafe_allow_html=True)
        
        # Exibição dos aquários como cartões
        for aquario in aquarios:
            numero = aquario['numero']
            ocupado = aquario['ocupado']
            status_class = "disponivel" if not ocupado else "indisponivel"
            status_text = "DISPONÍVEL" if not ocupado else "INDISPONÍVEL"
            
            # Renderiza cada aquário com a classe CSS correspondente
            st.markdown(
                f'<div class="aquario-card {status_class}">Sala {numero}<br>{status_text}</div>',
                unsafe_allow_html=True
            )

# Funções para exibir os aquários de cada prédio
def predio_1():
    response = fetch_data("predios/p1")
    if response:
        renderizar_aquarios(response, "P1")
    else:
        st.error("Erro ao carregar os dados do Prédio 1")

def predio_2():
    response = fetch_data("predios/p2")
    if response:
        renderizar_aquarios(response, "P2")
    else:
        st.error("Erro ao carregar os dados do Prédio 2")

def predio_3():
    response = fetch_data("predios/p4")
    if response:
        renderizar_aquarios(response, "P4")
    else:
        st.error("Erro ao carregar os dados do Prédio 3")
# def predio_1():
#     st.title("Prédio 1")
#     st.write("Detalhes do Prédio 1")
#     predio = fetch_data('predios/p1')
#     display_table(predio)
    

# def predio_2():
#     st.title("Prédio 2")
#     st.write("Detalhes do Prédio 2")    
#     predio = fetch_data('predios/p2')
#     display_table(predio)

# def predio_3():
#     st.title("Prédio 3")
#     st.write("Detalhes do Prédio 4")
#     predio = fetch_data('predios/p4')
#     display_table(predio)




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
