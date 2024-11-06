import streamlit as st
import requests

Base_url = "http://127.0.0.1:5000"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{Base_url}/{endpoint}")
        return response.json() if response.ok else None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar {endpoint}: {e}")
        return None

def cadastro():
    st.title("Cadastro")
    email = st.text_input("Email", key="signup_email")
    senha = st.text_input("Senha", type="password", key="signup_password")

    if st.button("Cadastrar", type='primary'):
        user_data = {"email": email, "senha": senha}
        response = requests.post(f"{Base_url}/cadastro", json=user_data)
        
        if response.ok:
            st.success("Usuário cadastrado com sucesso!")
        else:
            error_message = response.json().get('msg', 'Erro ao cadastrar.')
            st.error(error_message)

def Login():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        user_data = {"email": email, "senha": senha}
        response = requests.post(f"{Base_url}/login", json=user_data)
        
        if response.ok:
            st.success("Login bem-sucedido!")
        else:
            error_message = response.json().get('msg', 'Erro ao fazer login.')
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
        if st.button("Prédio 4", key='button3', type="primary"):
            st.session_state.page = "predio_4"

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

# Função para exibir uma tela em branco com informações do aquário e botão para alterar ocupação
def tela_aquario(predio, andar, numero):
    st.title(f"Detalhes do Aquário {numero}")
    st.write(f"Prédio: {predio}")
    st.write(f"Andar: {andar}º")

    # Botão para ocupar/desocupar o aquário
    ocupacao = fetch_data(f"predios/{predio}/andar/{andar}/aquario/{numero}")  # Exemplo de endpoint para buscar o status atual
    ocupado = ocupacao.get("ocupado", False) if ocupacao else False


    if st.button("Ocupar"):
        endpoint = f'aquarios/{"ocupar"}/{predio}/{andar}/{numero}'
        response = requests.put(f"{Base_url}/{endpoint}")
        
        if response.ok:
            novo_status = "ocupado"
            st.success(f"Aquário {novo_status} com sucesso!")
        else:
            st.error(response.json().get("msg", "Erro ao atualizar o status do aquário")) 
    if st.button("Desocupar"):
        endpoint = f'aquarios/{"desocupar"}/{predio}/{andar}/{numero}'
        response = requests.put(f"{Base_url}/{endpoint}")
        
        if response.ok:
            novo_status = "desocupado"
            st.success(f"Aquário {novo_status} com sucesso!")
        else:
            st.error(response.json().get("msg", "Erro ao atualizar o status do aquário")) 

    if st.button("Voltar"):
        st.session_state['page'] = f"predio_{predio[-1]}" 

# Função para renderizar aquários como botões
def renderizar_aquarios(dados_predio, nome_predio):
    st.title(f"Prédio {nome_predio}")
    
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
            cursor: pointer;
        }
        .disponivel {
            background-color: #4CAF50; /* Verde */
        }
        .indisponivel {
            background-color: #F44336; /* Vermelho */
        }
        .andar-header {
            background-color: #F44336;
            padding: 10px;
            text-align: center;
            font-size: 1.1em;
            font-weight: bold;
            border-radius: 5px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    for andar_info in dados_predio:
        andar = andar_info['andar']
        aquarios = andar_info['aquarios']
        
        st.markdown(f'<div class="andar-header">Andar {andar}º</div>', unsafe_allow_html=True)
        
        colunas = st.columns(len(aquarios))
        for idx, aquario in enumerate(aquarios):
            numero = aquario['numero']
            ocupado = aquario['ocupado']
            status_class = "disponivel" if not ocupado else "indisponivel"
            status_text = "DISPONÍVEL" if not ocupado else "INDISPONÍVEL"
            
            with colunas[idx]:
                if st.button(f"Aquário {numero}\n{status_text}", key=f"{nome_predio}{andar}{numero}"):
                    st.session_state['predio'] = nome_predio
                    st.session_state['andar'] = andar
                    st.session_state['numero'] = numero
                    st.session_state['page'] = "tela_aquario"

def predio_1():
    response = fetch_data("predios/p1")
    if response:
        renderizar_aquarios(response, "P1")
    else:
        st.error("Erro ao carregar os dados do Prédio 1")

    if st.button("Voltar"):
        st.session_state['page'] = "predios"

def predio_2():
    response = fetch_data("predios/p2")
    if response:
        renderizar_aquarios(response, "P2")
    else:
        st.error("Erro ao carregar os dados do Prédio 2")

    if st.button("Voltar"):
        st.session_state['page'] = "predios"

def predio_4():
    response = fetch_data("predios/p4")
    if response:
        renderizar_aquarios(response, "P4")
    else:
        st.error("Erro ao carregar os dados do Prédio 4")

    if st.button("Voltar"):
        st.session_state['page'] = "predios"

def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = "menu_principal"

    if st.session_state['page'] == "menu_principal":
        st.sidebar.title("Menu")
        option = st.sidebar.radio("Navegar", ["Cadastro", "Login", "Prédios"])

        if option == "Cadastro":
            cadastro()
        elif option == "Login":
            Login()
        elif option == "Prédios":
            predios()

    elif st.session_state['page'] == "predio_1":
        predio_1()
    elif st.session_state['page'] == "predio_2":
        predio_2()
    elif st.session_state['page'] == "predio_4":
        predio_4()
    elif st.session_state['page'] == "tela_aquario":
        tela_aquario(
            st.session_state['predio'],
            st.session_state['andar'],
            st.session_state['numero']
        )
    elif st.session_state['page'] == "predios":
        predios()

if __name__ == "__main__":
    main()