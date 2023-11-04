import pandas as pd


def tratar(df):
    df = df.dropna(subset=['Date'])
    df['Resultado'] = df['Result'].str[0]
    df['Gols Time'] = df['Result'].str[2]
    df['Gols Adversário'] = df['Result'].str[4]
    dropar = ['Result', 'Match Report']

    df.insert(6, 'Resultado', df.pop('Resultado'))
    df.insert(8, 'Gols Time', df.pop('Gols Time'))
    df.insert(10, 'Gols Adversário', df.pop('Gols Adversário'))

    df = df.drop(dropar, axis=1)
    df = df.rename(columns={'Date': 'Dia', 'Day':'Dia da Semana', 'Comp': 'Campeonato', 'Round': 'Rodada',
                            'Venue': 'Local', 'Squad': 'Time Jogador', 'Opponent': 'Time Adversário', 'Start': 'Titular',
                            'Pos':'Posição', 'Min':'Minutos','Gls':'Gols','Ast':'Assistências','PK':'Pênaltis Marcados',
                            'PKatt':'Pênaltis Cobrados','Sh':'Chutes Totais','SoT':'Chutes a Gol','CrdY':'Cartões Amarelos',
                            'CrdR':'Cartões Vermelhos','Touches':'Toques na Bola','Tkl':'Cabeceios','Int':'Interceptions',
                            'Blocks':'Bloqueios','xG':'Gols Esperados (xG)','npxG':'Gols Esperados sem pênaltis (npxG)',
                            'xAG':'Assistências Esperadas (xAG)','SCA':'Ações de Criação de Finalização (SCA)','GCA':'Ações de Criação de Gol (GCA)',
                            'Cmp':'Passes Completos','Att':'Tentativas de Passe','Cmp%':'Passes Completos(%)','PrgP':'Passes Progressivos',
                            'Carries':'Número de vezes que controlou a bola','PrgC':'Carregada de Bola Progressiva','Att.1':'Tentativas de Drible',
                            'Succ':'Dribles Sucedidos'})
    return df

def calculos(df):
    soma_gols = df['Gols'].sum()
    soma_minutos = df['Minutos'].sum()
    media_gols_por_jogo = ((soma_gols / soma_minutos) * 90)
    mediagols = "{:.2f}".format(media_gols_por_jogo)

    soma_gols_pen = df['Gols'].sum() - df['Pênaltis Marcados'].sum() 
    media_golspen_por_jogo = ((soma_gols_pen / soma_minutos) * 90)
    soma_gols_pen = "{:.2f}".format(media_golspen_por_jogo)

    soma_assists = df['Assistências'].sum()
    media_ass_por_jogo = ((soma_assists / soma_minutos) * 90)
    mediaass = "{:.2f}".format(media_ass_por_jogo)

    GmA = media_gols_por_jogo + media_ass_por_jogo
    mediaGmA = "{:.2f}".format(GmA)

    soma_toques = df['Toques na Bola'].sum()
    media_toques_por_jogo = ((soma_toques / soma_minutos) * 90)
    mediatoq = "{:.2f}".format(media_toques_por_jogo)

    passcompletos = df['Passes Completos'].sum()
    media_passcompletos_por_jogo = ((passcompletos / soma_minutos) * 90)
    passcompletos = "{:.2f}".format(media_passcompletos_por_jogo)

    soma_passes = df['Passes Completos(%)'].mean()
    mediapass = "{:.2f}".format(soma_passes)

    chutesgol = df['Chutes a Gol'].sum()
    media_chutesgols_por_jogo = ((chutesgol / soma_minutos) * 90)
    mediachutes = "{:.2f}".format(media_chutesgols_por_jogo)   

    cria = df['Ações de Criação de Finalização (SCA)'].sum()
    media_cria_por_jogo = ((cria / soma_minutos) * 90)
    criaf = "{:.2f}".format(media_cria_por_jogo)

    cria2 = df['Ações de Criação de Gol (GCA)'].sum()
    media_cria_por_jogo = ((cria2 / soma_minutos) * 90)
    criaf2 = "{:.2f}".format(media_cria_por_jogo)

    passesprog = df['Passes Progressivos'].sum()
    media_passesprog_por_jogo = ((passesprog / soma_minutos) * 90)
    passesprog = "{:.2f}".format(media_passesprog_por_jogo)

    carryprog = df['Carregada de Bola Progressiva'].sum()
    media_carryprog_por_jogo = ((carryprog / soma_minutos) * 90)
    carryprog = "{:.2f}".format(media_carryprog_por_jogo)

    controle = df['Número de vezes que controlou a bola'].sum()
    media_controle_por_jogo = ((controle / soma_minutos) * 90)
    controle = "{:.2f}".format(media_controle_por_jogo)
    
    tdrible = df['Tentativas de Drible'].sum()
    media_tdrible_por_jogo = ((tdrible / soma_minutos) * 90)
    tdrible = "{:.2f}".format(media_tdrible_por_jogo)

    cdrible = df['Dribles Sucedidos'].sum()
    media_cdrible_por_jogo = ((cdrible / soma_minutos) * 90)
    cdrible = "{:.2f}".format(media_cdrible_por_jogo)

    percdrible = (df['Dribles Sucedidos'].sum() / df['Tentativas de Drible'].sum()) * 100
    percdrible = "{:.2f}".format(percdrible)

    mapeamento_resultados = {"W": 3, "D": 1, "L": 0}
    pontos_totais = df['Resultado'].apply(lambda resultado: mapeamento_resultados.get(resultado, 0)).sum()
    total_partidas = len(df)
    aproveitamento = (pontos_totais / (total_partidas * 3) * 100)
    aproveitamento = '{:.2f}'.format(aproveitamento)


    return df, mediagols, soma_gols_pen, mediaass, mediatoq, mediapass, mediaGmA, mediachutes, criaf, criaf2, passesprog, carryprog, controle, passcompletos, tdrible, cdrible, percdrible, soma_minutos, aproveitamento