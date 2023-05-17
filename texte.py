import streamlit as st
import pandas as pd
import datetime
import mysql.connector
from util import converte_data
from PIL import Image
import streamlit_authenticator as stauth
from util import soma_basica
from util import string_to_list
from util import string_to_datetime
from random import randint
from util import converte_data
import string


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()

st.set_page_config(page_title="Avaliar Colaborador",  page_icon=Image.open('icon.png'),layout="wide" )
image = Image.open(('logo.png'))
st.image(image, width = 250)


comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()

sql = 'SELECT * FROM parametro_indicadores;'
mycursor.execute(sql)
listDadosIndicadores = mycursor.fetchall()

sql = 'SELECT * FROM parametro_procedimento;'
mycursor.execute(sql)
listDadosPC = (mycursor.fetchall())

sql = 'SELECT * FROM Colaboradores;'
mycursor.execute(sql)
listDados2 = (mycursor.fetchall())


def limpar_lista(lista_de_listas):
    lista_final = []
    for lista in lista_de_listas:
        for info in lista:
            lista_final.append(info)
    
    return lista_final


def mostrarIcon(image_url):
  st.markdown(
      f"""
      <style>
      .display-flex {{
          display: flex;
          justify-content: center;
          align-items: center;
      }}
      </style>
      <div class="display-flex">
          <img src="{image_url}" width="50%" height="50%">
      </div>
      """,
      unsafe_allow_html=True
  )

style = """
.loader {
  --cell-size: 50px;
  --cell-spacing: 5px;
  --cells: 3;
  --total-size: calc(var(--cells)  (var(--cell-size) + 2  var(--cell-spacing)));
  display: flex;
  flex-wrap: wrap;
  width: var(--total-size);
  height: var(--total-size);
}

.cell {
  flex: 0 0 var(--cell-size);
  margin: var(--cell-spacing);
  background-color: transparent;
  box-sizing: border-box;
  border-radius: 4px;
  animation: 8s ripple ease infinite;
}

.cell.d-1 {animation-delay: 400ms;}

.cell.d-2 {animation-delay: 800ms;}

.cell.d-3 {animation-delay: 1200ms;}

.cell.d-4 {animation-delay: 1600ms;}

.cell:nth-child(1) {--cell-color: #03FC52;}

.cell:nth-child(2) {--cell-color: #50AFEE;}

.cell:nth-child(3) {--cell-color: #020FFA;}

.cell:nth-child(4) {--cell-color: #FED002;}

.cell:nth-child(5) {--cell-color: #03FC52;}

.cell:nth-child(6) {--cell-color: #50AFEE;}

.cell:nth-child(7) {--cell-color: #FD0606;}

.cell:nth-child(8) {--cell-color: #FED002;}

.cell:nth-child(9) {--cell-color: #03FC52;}

/*Animation*/
@keyframes ripple {
  0% {background-color: transparent;}
  30% {background-color: var(--cell-color);}
  60% {background-color: transparent;}
  100% {background-color: transparent; }
}
"""

html = """
<div class="loader">
  <div class="cell d-0"></div>
  <div class="cell d-1"></div>
  <div class="cell d-2"></div>

  <div class="cell d-1"></div>
  <div class="cell d-2"></div>
  
  <div class="cell d-2"></div>
  <div class="cell d-3"></div>
  
  <div class="cell d-3"></div>
  <div class="cell d-4"></div>
</div>
"""



names = [x[5] for x in dadosUser if x[5] != None]
usernames = [x[7] for x in dadosUser if x[7] != None]
hashed_passwords = [stauth.Hasher([x[8]]).generate()[0] for x in dadosUser if x[8] != None]
funcao = [x[6] for x in dadosUser if x[6] != None]

def creat_numberRandom():
    number = randint(1,9999999999999)
    return int(number)

def convert_to_dict(names, usernames, passwords):
    credentials = {"usernames": {}}
    for name, username, password in zip(names, usernames, passwords):
        user_credentials = {
            "email":username,
            "name": name,
            "password": password
        }
        credentials["usernames"][username] = user_credentials
    return credentials

credentials = convert_to_dict(names, usernames, hashed_passwords)
authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)

col1, col2,col3 = st.columns([1,3,1])
with col2:
    name, authentication_status, username = authenticator.login('Acesse o sistema 9box', 'main')

if authentication_status == False:
    with col2:
        st.error('Email ou Senha Incorreto')
elif authentication_status == None:
    with col2:
        st.warning('Insira seu Email e Senha')
elif authentication_status:
    matric_gestores_avaliadores = list(set(limpar_lista([[x[8],x[10]] for x in listDados2])))

    matriUser = [x[4] for x in dadosUser if x[7] == username]
    perfilUser = str([x[9] for x in dadosUser if x[7] == username][0]).upper()

    #if perfilUser == 'A' or perfilUser == 'B':

    #QUALQUER UM VAI PODER RESPONDER A PARTE DE AVALIAR COLABORADOR
    
    st.title("Avaliar Colaborador")
    df1 = pd.read_excel("dadosAvaliação.xlsx", sheet_name="Avaliação")
    listDados1 = df1.values.tolist()
    liscod = [str(x[11]) for x in listDados2]
    col1, col2 = st.columns((2, 3))
    with col1:
        codA = st.text_input("Código de acesso da avaliação", type='password')
    if codA not in liscod:
        with col2:
            st.text_input("", "Avaliação não encontrada")
    else:
        linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][11]) == codA][0]
        st.write("---")
        col1, col2, col3, = st.columns((1, 2, 1))
        with col1:
            st.text_input('Matrícula', listDados2[linhaBD][0])
        with col2:
            st.text_input("Nome Colaborador", listDados2[linhaBD][1])
        with col3:
            anoQuadr = st.text_input("Data", f"{converte_data(str(listDados2[linhaBD][12]))}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input('Função', listDados2[linhaBD][40])
        with col2:
            st.text_input("Unidade de negócio", listDados2[linhaBD][2])
        with col3:
            st.text_input('Macroprocesso', listDados2[linhaBD][3])
        st.text_input('Processo', listDados2[linhaBD][4])
        col1, col2 = st.columns(2)
        with col1:
            st.text_input('Gestor de Carreira', listDados2[linhaBD][7])
        with col2:
            st.text_input('Avaliador', listDados2[linhaBD][9])
        not_funcao = ['Dono de processo', "Líder de Processos", "Gestor de Processos"]
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                ["Competências", "Desempenho | Processos", "Desempenho | Projetos", "BSC", "CPA", "Compromissos Assumidos"])
        with tab1:
            if listDados2[linhaBD][28] == 1:
                st.error("Avaliação já foi preenchida")
            else:
                with st.expander("Critérios para aplicar a nota", expanded=True):
                        st.info(
                            "1- Não executa \n\n 2-Executa Abaixo do Esperado \n\n 3-Executa Conforme o Esperado \n\n 4-Executa Algumas Atividades Acima do Esperado \n\n 5-Executa todas as atividades Acima do Esperado")
                with st.form("my_form"):
                        compObg = ["Orientação para Pessoas, Processos e Resultados", "Pensamento Crítico e Criativo",
                                "Comunicação", "Foco no cliente"]
                        optAval = ["1 - Não executa",
                                "2 - Abaixo do Esperado",
                                "3 - Conforme o Esperado",
                                "4 - Acima do Esperado",
                                "5 - Além do Esperado"]
                        lismediasObg = []
                        for i in compObg:
                            listmedia = []
                            st.subheader(i)
                            for j in listDados1:
                                if j[0] == i:
                                    st.write("")
                                    nota = int([st.select_slider(j[1], options=optAval, value=optAval[2])][0][0:1])
                                    listmedia.append(nota)
                                    # st.slider(j[1], 1,5,3,step=1)
                                    # st.selectbox(j[1], options=optAval,)
                                    st.write("---")
                            lismediasObg.append(int(sum(listmedia) / len(listmedia) * 100 / 5))
                        competenEspEucatur = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                            "Futuro e Tendências", "Raciocínio Analítico", "Empreendedorismo",
                                            "Tomada de Decisão", "Visão Estratégica", "Visão Inovadora", "Liderança"]
                        compEsp_aux = listDados2[linhaBD][6].split(',')
                        compEsp = [str(x).strip() for x in compEsp_aux]

                        lismediasEsp = []
                        for i in competenEspEucatur:
                            listmedia = []
                            if i not in compEsp:
                                lismediasEsp.append(None)
                            else:
                                st.subheader(i)
                                for j in listDados1:
                                    if j[0] == i:
                                        nota = int([st.select_slider(j[1], options=optAval, value=optAval[2])][0][0:1])
                                        listmedia.append(nota)
                                        # st.slider(j[1], 1,5,3,step=1)
                                        # st.selectbox(j[1], options=optAval,)
                                        st.write("---")
                                lismediasEsp.append(int(sum(listmedia) / len(listmedia) * 100 / 5))
                        lismedias = lismediasObg + lismediasEsp + [1]
                        submitted = st.form_submit_button("Registrar Avaliação do Colaborador")
                        if submitted:
                            if listDados2[linhaBD][28] == 1:
                                st.error("Avaliação já foi preenchida")
                            else:
                                linrow = ['(NULL)' if str(x) == "None" else x for x in lismedias]
                                colunas = ["C_OPPR",
                                        "C_PCC",
                                        "C_Com",
                                        "C_FC",
                                        "C_IntEmo",
                                        "C_AutPro",
                                        "C_RelNet",
                                        "C_FutTen",
                                        "C_RacAna",
                                        "C_Emp",
                                        "C_TomDec",
                                        "C_VisEst",
                                        "C_VisIno",
                                        "C_Lid",
                                        "C_Check"]
                                for i in range(len(colunas)):
                                    sql = f"UPDATE Colaboradores SET {colunas[i]} = {linrow[i]} WHERE CódAce = {int(codA)}"
                                    mycursor.execute(sql)
                                    conexao.commit()
                                st.info(f"Colaborador Avaliado com Sucesso")
            with tab2:
                if listDados2[linhaBD][33] == 1:
                    st.error("Registro do processo já foi realizado")
                else:
                    if listDados2[linhaBD][40] == "Líder de Processos":
                        procCola = [listDados2[linhaBD][3]]
                    else:
                        procCola = listDados2[linhaBD][4].split(",")

                    L_ind = []
                    L_met = []
                    L_Des = []
                    L_Pol = []
                    number_indicadores = []
                    st.write(' ')
                    col1, col2, col3 = st.columns((1.2, 1, 0.9))
                    with col2:
                        st.subheader('Desempenho Processos')
                    st.text(' ')
                   
                    procedimentos_BD = [[x[2],x[3]] for x in listDadosPC]
                    indicadores_BD = [[x[2], x[4]] for x in listDadosIndicadores]
                    
                    periodicidade = listDados2[linhaBD][41]
                    if periodicidade == 'Trimestral':
                        vezes_periodo = 3
                    elif periodicidade == 'Bimestral':
                        vezes_periodo = 2
                    else:                               
                        vezes_periodo = 1

                    cont = 0
                    name_newIndicador = []
                    for procin in range(len(procCola)):
                        cont += 2
                        name_newIndicador_aux = []
                                                
                        col1, col2 = st.columns((1,4))
                        with col1:
                            add_indicador = st.number_input('Adcione Indicadores',min_value=0, step=1, key= f'{procin + cont}')
                        
                        with col2:      
                            if add_indicador > 0:      
                                for a in range(add_indicador):
                                    cont+= 1
                                    number_random = cont + creat_numberRandom()
                                    name_newIndicador_aux.append(st.text_input('Novo indicador', key = f'{number_random}'))
                            else:
                                name_newIndicador_aux = ''
                        
                        name_newIndicador.append(name_newIndicador_aux)
                    with st.form("my_form1"):
                        cont = 0
                        for proc in range(len(procCola)):
                            titulo_proc = f'<div style="text-align:center; color:White;font-size:20px">{procCola[proc]}</div>'
                            st.markdown(titulo_proc, unsafe_allow_html=True)
                            st.text(' ')
                            
                            procedimentos = []
                            
                            if string_to_list(listDados2[linhaBD][49])[proc] != '[]' and string_to_list(listDados2[linhaBD][49])[proc] != '' and string_to_list(listDados2[linhaBD][49])[proc] != None:
                                for a in (string_to_list(listDados2[linhaBD][49])[proc]):
                                    procedimentos.append(a)
                            
                            procedimentos_numbers = [x[0] for x in procedimentos_BD if x[1] in procedimentos]

                            #INDICADORES DOS PROCEDIMENTOS DAQUELE PROCESSO
                            indicadores_to_proc = [x[1] for x in indicadores_BD if x[0] in procedimentos_numbers]

                            if len(name_newIndicador[proc])> 0:
                                indicadores_to_proc.extend(name_newIndicador[proc])
            
                            number_indicadores = len(indicadores_to_proc)
                            
                            col1, col2, col3, col4 = st.columns((1.20, 0.4, 0.5, 0.5))
                            with col1:
                                st.info(f"Indicadores")
                            with col2:
                                st.info("Meta")
                            with col3:
                               st.info("Realizado")
                            with col4:
                                st.info("Polaridade")
                            L_aux1 = []
                            L_aux2 = []
                            L_aux3 = []
                            L_aux4 = []

                            polarid = ['Positivo', 'Negativo']

                            for index_indic in range(number_indicadores):
                                periodo_inicial = string_to_datetime(listDados2[linhaBD][12])

                                for a in range(vezes_periodo):
                                    dias = datetime.timedelta(days=30 * a)
                                    periodo_ind = periodo_inicial + dias
                                    
                                    cont+=1
                                    with col1:
                                        L_aux1.append(st.text_input(f'a{proc} {a + 1}', f'{indicadores_to_proc[index_indic]}({converte_data(str(periodo_ind))})', label_visibility="hidden",key=f'{cont+1000}'))
                                    with col2:
                                        L_aux2.append(st.number_input(f'b{proc} {a + 1}', label_visibility="hidden", min_value=(0.00), step=0.01, key=f'{cont+23}'))
                                    with col3:
                                        L_aux3.append(st.number_input(f'c{proc} {a + 1}', label_visibility="hidden", min_value=(0.00), step=0.01, key=f'{cont+100}'))
                                    with col4:
                                        L_aux4.append(st.selectbox(f'd{proc} {a + 1}', polarid, label_visibility="hidden", key=f'{cont+300}'))
                                L_ind.append(L_aux1)
                                L_met.append(L_aux2)
                                L_Des.append(L_aux3)
                                L_Pol.append(L_aux4)
                                print(L_Pol)
                                print(L_met, L_Des, L_ind)
                                st.text(" ")

                        submitted1 = st.form_submit_button("Registrar Desempenho Processos")
                        if submitted1:
                            if listDados2[linhaBD][33] == 1:
                                st.error("Avaliação já foi preenchida")
                            else:
                                linrow = [L_ind, L_met, L_Des, L_Pol, 1]
                                colunas = ["N_IPROC", "M_IPROC", "D_IPROC", "P_IPROC", "DPROC_Check"]
                                for i in range(len(colunas)):
                                    sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                    mycursor.execute(sql)
                                    conexao.commit()
                                st.success('Registro realizado')
                # REGISTRO DE PROCEDIMENTOS DE PROCESSOS
                if listDados2[linhaBD][51] == '1':
                    st.error("Registro de Procedimento já foi realizado")
                else:
                    if listDados2[linhaBD][40] == "Líder de Processos":
                        procCola = [listDados2[linhaBD][3]]
                    else:
                        procCola = listDados2[linhaBD][4].split(",")

                    procedimentos_BD = [[x[2],x[3]] for x in listDadosPC]
                    
                    procediment_BD_colab = list(string_to_list(listDados2[linhaBD][49]))

                    st.write(' ')
                    st.write(' ')
                    col1, col2, col3 = st.columns((1.1, 1, 0.9))
                    with col2:
                        st.subheader('Carga Horária Processos')
                    new_number_procedim = []
                    st.write(' ')
                    colun1, colun2, colun3 = st.columns((3, 1, 1))
                    for proc in range(len(procCola)):
                        with colun1:
                            new_number_procedim.append(st.number_input(f'Procedimentos - {procCola[proc]}', min_value=(0), step=(1)))

                            for a in range(int(new_number_procedim[0])):
                                var_aux = list(procediment_BD_colab[proc])
                                var_aux.extend([' '])
                                procediment_BD_colab[proc] = var_aux


                    lista_final_proced = []
                    lista_final_horas = []
                    with st.form('form_proced'):
                        for proc in range(len(procCola)):
                            colP1, colP2 = st.columns((3, 1))
                            with colP1:
                                st.markdown(f'Procedimentos - {procCola[proc]}')
                            with colP2:
                                st.markdown(f'Horas')
                            lista_procedimentos = []
                            lista_horas_proced = []
                            
                            number_total_proced = len(procediment_BD_colab[proc])

                            for a in range(number_total_proced):
                                coluna1, coluna2 = st.columns((3, 1))
                                with coluna1:
                                    proced = st.text_input(f'Procedimentos {a + 1}', f'{procediment_BD_colab[proc][a]}', key=f'Procedimentos {a + 1} - {procCola[proc]}', label_visibility='hidden')
                                    lista_procedimentos.append(proced)
                                with coluna2:
                                    horas_proced = st.number_input(f'Horas {a + 1}', min_value=(1), step=(1), key=f'Horas {a + 1} - {procCola[proc]}', label_visibility='hidden')
                                    lista_horas_proced.append(horas_proced)
                            lista_final_proced.append(lista_procedimentos)
                            lista_final_horas.append(lista_horas_proced)
             
                        proced_button = st.form_submit_button("Registrar Procedimentos de Processos")
                        if proced_button:
                            if listDados2[linhaBD][33] == '1':
                                st.error("Avaliação já foi preenchida")
                            else:
                                linrow = [lista_final_proced, lista_final_horas, 1]
                                colunas = ["Procedimento", "hrs_procedim", "Check_proced"]
                                for i in range(len(colunas)):
                                    sql = f'UPDATE Colaboradores SET {colunas[i]} =  "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                    mycursor.execute(sql)
                                    conexao.commit()
                                st.success('Registro realizado')
            with tab3:
                if listDados2[linhaBD][38] == 1:
                    st.error("Registro já foi realizado")
                else:
                    st.subheader("Desempenho Projetos")
                    lista_projetos = []
                    lista_indicadores = []
                    lista_horas = []
                    col1, col2, col3 = st.columns((1.5, 0.75, 0.75))
                    with col3:
                        qnt_projetos = st.number_input("N° Projetos", min_value=(1), step=(1))
                    with col1:
                        for a in range(qnt_projetos):
                            lista_projetos.append(st.text_input(f"", f'Nome Projeto {a + 1}',key=f'Nome Projeto {a + 1}'))
                    with col2:
                        for a in range(qnt_projetos):
                            lista_indicadores.append(st.number_input(f'Indicadores', key=f'Indicadores {a + 1}', min_value=(1), step=(1)))
                    
                    st.text(' ')
                    st.text(' ')
                    st.text(' ')
                    with st.form("my_form3"):
                        if listDados2[linhaBD][40] == "Líder de Processos":
                            procCola = [listDados2[linhaBD][3]]
                        else:
                            procCola = listDados2[linhaBD][4].split(",")
                        L_ind = []
                        L_met = []
                        L_Des = []
                        L_Pol = []
                        
                    
                        for proj in range(qnt_projetos):
                            colu1, colu2 = st.columns((3, 1))
                            with colu1:
                                st.text(' ')
                                st.text(' ')
                                st.subheader(f"**{lista_projetos[proj]}**")
                            with colu2:
                                lista_horas.append(st.number_input(f'Horas', key=f'Horas {proj + 1}',min_value=(1), step=(1)))
                            L_aux1 = []
                            L_aux2 = []
                            L_aux3 = []
                            L_aux4 = []
                            polarid = ['Positivo', 'Negativo']
                            #with col1:
                            #    st.write("Indicador")
                            #with col2:
                            #    st.write("Meta")
                            #with col3:
                            #    st.write("Realizado")
                            #with col4:
                            #    st.write("Polaridade")
                            for a in range(int(lista_indicadores[proj])):
                                col1, col2, col3, col4 = st.columns((1.50, 0.5, 0.5, 0.75))
                                with col1:
                                    L_aux1.append(st.text_input(f'Indicador', key=f'Indicador {lista_projetos[proj]} {a + 1}'))
                                with col2:
                                    L_aux2.append(st.number_input(f'Meta', key=f'Meta {lista_projetos[proj]} {a + 1}', min_value=(0.00), step=0.01))
                                with col3:
                                    L_aux3.append(st.number_input(f'Realizado', key=f'Realizado {lista_projetos[proj]} {a + 1}',min_value=(0.00), step=0.01))
                                with col4:
                                    L_aux4.append(st.selectbox(f'Polaridade', polarid, key=f'Polaridade {lista_projetos[proj]} {a + 1}'))
                            
                                st.write("---")
                            
                            L_ind.append(L_aux1)
                            L_met.append(L_aux2)
                            L_Des.append(L_aux3)
                            L_Pol.append(L_aux4)
                            print(L_Pol)
                            print(L_met, L_Des, L_ind)
                        submitted2 = st.form_submit_button("Registrar Desempenho Projetos")
                        if submitted2:
                            if listDados2[linhaBD][38] == 1:
                                st.error("Registro já foi realizado")
                            else:
                                linrow = [L_ind, L_met, L_Des, L_Pol, 1, lista_projetos, lista_horas]
                                colunas = ["N_IPROJ", "M_IPROJ", "D_IPROJ", "P_IPROJ", "DPROJ_Check", "NAME_PROJ", "HORAS_PROJ"]
                                for i in range(len(colunas)):
                                    sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                    mycursor.execute(sql)
                                    conexao.commit()
                                st.success('Registro do colaborador encaminhado.')
            lista_pesos = ['Peso de Competências','Peso de Processos', 'Peso de Projetos']
            with tab4:
                if listDados2[linhaBD][56] == '1':
                    st.error("Registro já foi realizado")
                else:
                    pesos = []
                    st.header('Pesos BSC')
                    st.text(' ')
                    with st.form('BSC'):
                        for a in lista_pesos:
                            coluna1, coluna2 = st.columns((3,1))
                            with coluna1:
                                st.text(' ')
                                st.text(' ')
                                st.markdown(f'{a}')
                            with coluna2:
                                peso_user = st.number_input('Porcetagem',max_value=100, step=1, key=f'{a}')
                        
                            st.write('---')
                            pesos.append(peso_user)
                        submitted = st.form_submit_button("Registrar pesos")  
                        
                        if submitted:
                            soma = soma_basica(pesos)
                            if soma != 100:
                                st.warning('Impossível prosseguir! A soma dos campos deve ser 100%.')
                            else:
                                pesos.append(1)
                                coluna = ['BSC_Peso_Compr', 'BSC_Peso_Proces', 'BSC_Peso_Proj', 'BSC_check']
                                for a in range(len(pesos)):    
                                    comando = f'UPDATE Colaboradores SET {coluna[a]} = "{pesos[a]}"  WHERE CódAce = {int(codA)}'
                                    mycursor.execute(comando)
                                    conexao.commit()
                                st.success('Informações armazenadas com sucesso')
            
            with tab5:
                st.header('CPA')
                st.text(' ')
                lista_valores = []
                topicos = ['Capacitação', 'Perfil', 'Atitude']
                
                with st.form('CPA'):
                    for top in topicos:
                        col_CPA, col_CPA1 = st.columns((3,1))
                        with col_CPA:
                            st.text(' ')
                            st.text(' ')
                            st.markdown(f'{top}')
                        
                        with col_CPA1: 
                            valores = st.number_input('Porcetagem',max_value=100, step=1, key=f'{top}')
                        
                        st.write('---')
                        lista_valores.append(valores)
                    
                    submittedCPA = st.form_submit_button("Registrar CPA")
                    if submittedCPA: 
                        for a in range(len(lista_valores)):
                            coluna = ['CPA_Perfil', 'CPA_Capacit', 'CPA_Atitude']
                            comando = f'UPDATE Colaboradores SET {coluna[a]} = "{lista_valores[a]}"  WHERE CódAce = {int(codA)}'
                            mycursor.execute(comando)
                            conexao.commit()
                        st.success('Informações armazenadas com sucesso')
                       
