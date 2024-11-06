import streamlit as st
import requests
import base64
Base_url = "http://127.0.0.1:5000"

def fetch_data(endpoint):
    try:
        headers = {}
        if 'email' in st.session_state and 'senha' in st.session_state:
            credentials = f"{st.session_state['email']}:{st.session_state['senha']}"
            credentials_bytes = credentials.encode('ascii')
            base64_bytes = base64.b64encode(credentials_bytes)
            base64_credentials = base64_bytes.decode('ascii')
            headers['Authorization'] = f'Basic {base64_credentials}'

        response = requests.get(f"{Base_url}/{endpoint}", headers=headers)
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

def login():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_password")

    if st.button("Entrar"):
        user_data = {"email": email, "senha": senha}
        response = requests.post(f"{Base_url}/login", json=user_data)
        
        if response.ok:
            st.success("Login bem-sucedido!")
            st.session_state['is_authenticated'] = True  # Define como autenticado
            # Armazena as credenciais na sessão
            st.session_state['email'] = email
            st.session_state['senha'] = senha
            st.session_state['logged_in'] = True
            st.session_state['page'] = 'predios'  # Redireciona para a página dos prédios
        else:
            error_message = response.json().get('msg', 'Erro ao fazer login.')
            st.error(error_message)

def predios():
    # Verifica autenticação antes de mostrar a tela de prédios
    if not st.session_state.get('is_authenticated', False):
        st.error("Você precisa fazer login para acessar a tela de Prédios.")
        return

    if not st.session_state.get('logged_in'):
        st.error("Você precisa estar logado para acessar esta página.")
        return
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

    if st.button("Voltar"):
        st.session_state['page'] = "menu_principal"

# Função para exibir uma tela em branco com informações do aquário e botão para alterar ocupação
def tela_aquario(predio, andar, numero):
    st.title(f"Detalhes do Aquário {numero}")
    st.write(f"Prédio: {predio}")
    st.write(f"Andar: {andar}º")

    # Botão para ocupar/desocupar o aquário
    ocupacao = fetch_data(f"predios/{predio}/andar/{andar}/aquario/{numero}")
    ocupado = ocupacao.get("ocupado", False) if ocupacao else False

    # Preparar o cabeçalho com as credenciais
    headers = {}
    if 'email' in st.session_state and 'senha' in st.session_state:
        credentials = f"{st.session_state['email']}:{st.session_state['senha']}"
        credentials_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(credentials_bytes)
        base64_credentials = base64_bytes.decode('ascii')
        headers['Authorization'] = f'Basic {base64_credentials}'
    else:
        st.error("Você precisa estar logado para ocupar ou desocupar um aquário.")
        return

    # Botões para ocupar/desocupar o aquário
    if st.button("Ocupar"):
        endpoint = f'aquarios/ocupar/{predio}/{andar}/{numero}'
        response = requests.post(f"{Base_url}/{endpoint}", headers=headers)
        
        if response.ok:
            st.success("Aquário ocupado com sucesso!")
        else:
            st.error(response.json().get("msg", "Erro ao ocupar o aquário"))
    if st.button("Desocupar"):
        endpoint = f'aquarios/desocupar/{predio}/{andar}/{numero}'
        response = requests.post(f"{Base_url}/{endpoint}", headers=headers)
        
        if response.ok:
            st.success("Aquário desocupado com sucesso!")
        else:
            st.error(response.json().get("msg", "Erro ao desocupar o aquário"))

    if st.button("Voltar"):
        st.session_state['page'] = "predios" 

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
    if 'is_authenticated' not in st.session_state:
        st.session_state['is_authenticated'] = False

    if 'page' not in st.session_state:
        st.session_state['page'] = "menu_principal"
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    st.sidebar.title("Menu")
    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            # Limpa as informações de autenticação
            st.session_state['logged_in'] = False
            st.session_state.pop('email', None)
            st.session_state.pop('senha', None)
            st.session_state['page'] = "menu_principal"
            st.success("Logout realizado com sucesso.")
        else:
            st.sidebar.write(f"Logado como: {st.session_state['email']}")
            st.sidebar.write("---")
            option = st.sidebar.radio("Navegar", ["Prédios"])
            if option == "Prédios":
                st.session_state['page'] = "predios"
    else:
        option = st.sidebar.radio("Navegar", ["Cadastro", "Login"])
        if option == "Cadastro":
            cadastro()
        elif option == "Login":
            login()
        elif option == "Prédios":
            predios()

    # Navegação entre as páginas
    if st.session_state['page'] == "predio_1":
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
    elif st.session_state['page'] == "menu_principal":
        st.title("Bem-vindo ao Sistema de Reservas de Aquários")
        st.write("Por favor, utilize o menu ao lado para navegar.")


if __name__ == "__main__":
    main()