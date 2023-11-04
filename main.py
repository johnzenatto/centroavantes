import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 

import os

import tratamento

st.set_page_config(
    page_title="Comparativo",
    layout="wide"
)

esconde = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
          """
st.markdown(esconde, unsafe_allow_html=True)

dataframes = []

pasta = 'Planilhas/'

arquivos = os.listdir(pasta)

for arquivo in arquivos:
    if arquivo.endswith(".csv"):
        # Caminho completo para o arquivo
        caminho_arquivo = os.path.join(pasta, arquivo)
        # Carregar o arquivo CSV em um DataFrame
        df = pd.read_csv(caminho_arquivo)
        # Adicionar o DataFrame à lista
        dataframes.append(df)

# Concatenar todos os DataFrames da lista em um único DataFrame
df_concat = pd.concat(dataframes, ignore_index=True)

df_concat = tratamento.tratar(df_concat)

tit0,tit1,tit2 = st.columns([2,3,1])
with tit0:
    st.text('Fonte: https://fbref.com/en/comps/24/stats/Serie-A-Stats')
with tit1:
    st.title('Centroavantes Brasileirão 2023')
with tit2:
    st.text('dados dia:03/11/2023')

with st.expander('Média'):
    coli1, coli2, coli3, coli4, coli5, coli6 = st.columns(6)
    df_concat,golsmed, golspenmed, assmed,tqjogomed, mediapassmed,GmAmed, chutesmed, criafmed, criaf2med, passeprogmed, carryprogmed, controlemed, passcompletosmed, tdriblemed, cdriblemed, percdriblemed, minsmed,aproveitamentomed = tratamento.calculos(df_concat)
    with coli1:
        st.metric('Gols',golsmed)
        st.metric('Chutes a Gol', chutesmed)
        st.metric('Domínios', controlemed)
    with coli2:
        st.metric('Gols - Gols Penalti', golspenmed)
        st.metric('Criação de Chute',criafmed)
        st.metric('Tentativa Drible', tdriblemed)
    with coli3:
        st.metric('Assist.',assmed)
        st.metric('Criação de Gols', criaf2med)
        st.metric('Dribles Sucedidos', cdriblemed)
    with coli4:
        st.metric('Gols + Assits',GmAmed)
        st.metric('Conduzida Progressivos', carryprogmed)
        st.metric('Dribles Certos (%)',percdriblemed)
    with coli5:
        st.metric('Passes Certos %', mediapassmed)
        st.metric('Passes Progressivos', passeprogmed)
        st.metric('Minutos Jogados', minsmed/20)
    with coli6:
        st.metric('Passes Completos', passcompletosmed)
        st.metric('Toques/90', tqjogomed)
        st.metric('Aproveitamento (%)', aproveitamentomed)

with st.expander('Informações'):
    st.text('*As comparações do jogador 1 são referentes a média, enquanto as comparações do jogador 2 são referentes ao jogador 1') 
    st.text('*Os dados são a exibidos são a (soma / minutos jogados) * 90) ou seja, a média por 90 mins')
    st.text('*Os Gráficos são filtrados para a Série A')

col1, col2 = st.columns(2)
with col1:
    jogador1 = st.selectbox(
        "Jogador 1:",
        options=df_concat['Nome'].unique(),
        index=0
    )
    df1 = df_concat[df_concat['Nome'] == jogador1]

    liga1 = st.multiselect('Campeonato(s)',
        options=df1['Campeonato'].unique(),
        default='Série A'
    )
    df1 = df1[(df1['Campeonato'].isin(liga1))] 
    
        
    df1,gols, golspen, ass,tqjogo, mediapass,GmA, chutes, criaf, criaf2, passeprog, carryprog, controle, passcompletos, tdrible, cdrible, percdrible, mins,aproveitamento = tratamento.calculos(df1)
    coli1, coli2, coli3, coli4, coli5, coli6 = st.columns(6)
    def delta(val1,val2):
        val1 = float(val1)
        val2 = float(val2)
        delta = val1 - val2 
        delta = '{:.2f}'.format(delta)
        return delta

    with coli1:
        st.metric('Gols',gols, delta = delta(gols,golsmed) )
        st.metric('Chutes a Gol', chutes, delta = delta(chutes,chutesmed))
        st.metric('Domínios', controle, delta = delta(controle,controlemed))
    with coli2:
        st.metric('Gols - Gols Penalti', golspen, delta = delta(golspen,golspenmed))
        st.metric('Criação de Chute',criaf, delta = delta(criaf,criafmed))
        st.metric('Tentativa Drible', tdrible, delta = delta(tdrible,tdriblemed))
    with coli3:
        st.metric('Assist.',ass, delta = delta(ass,assmed))
        st.metric('Criação de Gols', criaf2, delta = delta(criaf2,criaf2med))
        st.metric('Dribles Sucedidos', cdrible, delta = delta(cdrible,cdriblemed))
    with coli4:
        st.metric('Gols + Assits',GmA, delta = delta(GmA,GmAmed))
        st.metric('Conduzida Progressivos', carryprog, delta = delta(carryprog,carryprogmed))
        st.metric('Dribles Certos (%)',percdrible, delta = delta(percdrible,percdriblemed) + '%')
    with coli5:
        st.metric('Passes Certos %', mediapass, delta = delta(mediapass,mediapassmed) + '%')
        st.metric('Passes Progressivos', passeprog, delta = delta(passeprog,passeprogmed))
        st.metric('Minutos Jogados', mins, delta = delta(mins,minsmed/20))
    with coli6:
        st.metric('Passes Completos', passcompletos, delta = delta(passcompletos,passcompletosmed))
        st.metric('Toques/90', tqjogo, delta = delta(tqjogo,tqjogomed))
        st.metric('Aproveitamento (%)', aproveitamento, delta = delta(aproveitamento,aproveitamentomed))
    
    with st.expander(f'Tabela {jogador1}'):
        st.write(df1)
with col2:
    jogador2 = st.selectbox(
        "Jogador 2:",
        options=df_concat['Nome'].unique(),
        index=1
    )
    df2 = df_concat[df_concat['Nome'] == jogador2]
    liga2_options = df2['Campeonato'].unique()

    if len(liga2_options) > 1:
        liga2 = st.multiselect('Campeonato(s)',
            options=df2['Campeonato'].unique(),
            default='Série A'
        )
        df2 = df2[(df2['Campeonato'].isin(liga2))] 
    else:   
        st.multiselect('Campeonato',
                       options=['Série A'],
                       default='Série A')
        df2 = df2[(df2['Campeonato'].isin(liga1))] 
        
    df1,gols1, golspen1, ass1, tqjogo1, mediapass1, GmA1, chutes1, criaf1, criaf21, passeprog1, carryprog1, controle1, passcompletos1, tdrible1, cdrible1, percdrible1, mins1, aproveitamento1 = tratamento.calculos(df2)
    coli1, coli2, coli3, coli4, coli5, coli6 = st.columns(6)
    with coli1:
        st.metric('Gols',gols1, delta = delta(gols1,gols))
        st.metric('Chutes a Gol', chutes1, delta = delta(chutes1,chutes))
        st.metric('Domínios', controle1, delta = delta(controle1,controle))
    with coli2:
        st.metric('Gols - Gols Penalti', golspen1, delta = delta(golspen1,golspen))
        st.metric('Criação de Chute',criaf1, delta = delta(criaf1,criaf))
        st.metric('Tentativa Drible', tdrible1, delta = delta(tdrible1,tdrible))
    with coli3:
        st.metric('Assist.',ass1, delta = delta(ass1,ass))
        st.metric('Criação de Gols', criaf21, delta = delta(criaf21,criaf2))
        st.metric('Dribles Sucedidos', cdrible1, delta = delta(cdrible1,cdrible))
    with coli4:
        st.metric('Gols + Assits',GmA1, delta = delta(GmA1,GmA))
        st.metric('Conduzida Progressivos', carryprog1, delta = delta(carryprog1,carryprog))
        st.metric('Dribles Certos (%)',percdrible1, delta = delta(percdrible1,percdrible)+'%')
    with coli5:
        st.metric('Passes Certos %', mediapass1, delta = delta(mediapass1,mediapass) + '%')
        st.metric('Passes Progressivos', passeprog1, delta = delta(passeprog1,passeprog))
        st.metric('Minutos Jogados', mins1, delta = delta(mins1,mins))
    with coli6:
        st.metric('Passes Completos', passcompletos1, delta = delta(passcompletos1,passcompletos))
        st.metric('Toques/90', tqjogo1, delta = delta(tqjogo1,tqjogo))
        st.metric('Aproveitamento (%)', aproveitamento1, delta = delta(aproveitamento1,aproveitamento))

    with st.expander(f'Tabela {jogador2}'):
        st.write(df2)

def Barras90min(df, campo):
    df_serie_a = df_concat[df_concat['Campeonato'] == 'Série A']

    # Calcular a soma do campo e a soma de minutos por jogador
    campo_minutos_por_jogador = df_serie_a.groupby('Nome')[[campo, 'Minutos']].sum().reset_index()

    # Calcular campo por minuto e multiplicar por 90
    campo_minutos_por_jogador[f'{campo} por 90 Minutos'] = (campo_minutos_por_jogador[campo] / campo_minutos_por_jogador['Minutos']) * 90

    # Calcular a média dos "campo por 90 Minutos"
    media_campo_por_90_minutos = campo_minutos_por_jogador[f'{campo} por 90 Minutos'].mean()

    # Formatar os valores com duas casas decimais
    campo_minutos_por_jogador[f'{campo} por 90 Minutos'] = campo_minutos_por_jogador[f'{campo} por 90 Minutos'].round(2)

    # Criar uma coluna para definir as cores com base nos jogadores
    campo_minutos_por_jogador['Cor'] = 'lightblue'  
    campo_minutos_por_jogador.loc[campo_minutos_por_jogador['Nome'] == jogador1, 'Cor'] = 'red'
    campo_minutos_por_jogador.loc[campo_minutos_por_jogador['Nome'] == jogador2, 'Cor'] = 'blue'

    # Ordenar o DataFrame por 'campo por 90 Minutos' do maior para o menor
    campo_minutos_por_jogador = campo_minutos_por_jogador.sort_values(by=f'{campo} por 90 Minutos', ascending=False)

    # Definir a ordem das barras com base na coluna 'Nome'
    fig = px.bar(campo_minutos_por_jogador, x='Nome', y=f'{campo} por 90 Minutos', text=f'{campo} por 90 Minutos', title=f'{campo} por 90 Minutos por Jogador', color='Cor', category_orders={"Nome": campo_minutos_por_jogador['Nome']})

    fig.update_xaxes(tickangle=45)  # Rotaciona os rótulos em um ângulo de 45 graus

    # Adicionar uma linha vermelha representando a média
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=-0.5,
            x1=len(campo_minutos_por_jogador) - 0.5,
            y0=media_campo_por_90_minutos,
            y1=media_campo_por_90_minutos,
            line=dict(color="red", width=1),
        )
    )
    st.write(f'Média {campo}/90: {media_campo_por_90_minutos:.2f}')

    # Remover a legenda
    fig.update_layout(showlegend=False)

    config = {'displaylogo':False}
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig,use_container_width=True, config=config)

col1,col2,col3 = st.columns(3)
with col1:
    Barras90min(df_concat, 'Gols')
with col2:
    Barras90min(df_concat, 'Assistências')
with col3:
    df_concat['Gols + Assistências'] = df_concat['Gols'] + df_concat['Assistências']
    Barras90min(df_concat, 'Gols + Assistências')

col1,col2,col3 = st.columns(3)
with col1:
    Barras90min(df_concat, 'Chutes a Gol')
with col2:
    Barras90min(df_concat, 'Ações de Criação de Finalização (SCA)')
with col3:
    Barras90min(df_concat, 'Ações de Criação de Gol (GCA)')

col1,col2,col3 = st.columns(3)
with col1:
    Barras90min(df_concat, 'Passes Completos')   
with col2:
    Barras90min(df_concat, 'Passes Progressivos')
with col3:
    Barras90min(df_concat, 'Carregada de Bola Progressiva')

col1,col2,col3 = st.columns(3)
with col1:
    Barras90min(df_concat, 'Toques na Bola')   
with col2:
    Barras90min(df_concat, 'Número de vezes que controlou a bola')    
with col3:
    Barras90min(df_concat, 'Tentativas de Drible')
