# import pandas as pd
# import streamlit as st
# import openpyxl

# # Configuração da página do Streamlit
# st.set_page_config(page_title="Mobilidade Urbana", layout="wide", page_icon="🚌")

# # Leitura da tabela Excel
# df = pd.read_excel("Tabela_13_Meio_de_transporte.xlsx")

# # Exibir as primeiras linhas da tabela para verificar os dados
# st.write("Visualização inicial dos dados:")
# st.dataframe(df.head())

# # Ajustar os nomes das colunas com base no número de colunas no arquivo
# nomes_colunas = [
#     "Cidade",
#     "Branca_Transporte1", "Branca_Transporte2", "Branca_Transporte3", "Branca_Transporte4", "Branca_Transporte5", "Branca_Transporte6",
#     "Preta_Transporte1", "Preta_Transporte2", "Preta_Transporte3", "Preta_Transporte4", "Preta_Transporte5", "Preta_Transporte6",
#     "Indigena_Transporte1", "Indigena_Transporte2", "Indigena_Transporte3", "Indigena_Transporte4", "Indigena_Transporte5", "Indigena_Transporte6",
#     "Categoria_Renda"
# ]
# df.columns = nomes_colunas[:len(df.columns)]

# # Sidebar para filtros
# st.sidebar.header("Filtros")

# # Filtro por Região Metropolitana/UF
# regioes_disponiveis = df["Cidade"].unique()
# regiao_selecionada = st.sidebar.multiselect("Selecione a Região Metropolitana/UF:", regioes_disponiveis, default=regioes_disponiveis)

# # Filtro por Meio de Transporte
# meios_transporte = [
#     "Branca_Transporte1", "Branca_Transporte2", "Branca_Transporte3", "Branca_Transporte4", "Branca_Transporte5", "Branca_Transporte6",
#     "Preta_Transporte1", "Preta_Transporte2", "Preta_Transporte3", "Preta_Transporte4", "Preta_Transporte5", "Preta_Transporte6",
#     "Indigena_Transporte1", "Indigena_Transporte2", "Indigena_Transporte3", "Indigena_Transporte4", "Indigena_Transporte5", "Indigena_Transporte6"
# ]
# transporte_selecionado = st.sidebar.multiselect("Selecione o Meio de Transporte:", meios_transporte, default=meios_transporte)

# # Filtro por Categoria de Renda
# categorias_renda = df["Categoria_Renda"].unique() if "Categoria_Renda" in df.columns else []
# renda_selecionada = st.sidebar.multiselect("Selecione a Categoria de Renda:", categorias_renda, default=categorias_renda)

# # Aplicar os filtros
# df_filtrado = df[
#     (df["Cidade"].isin(regiao_selecionada)) &
#     (df["Categoria_Renda"].isin(renda_selecionada) if "Categoria_Renda" in df.columns else True)
# ]

# # Filtrar apenas as colunas selecionadas para transporte
# colunas_selecionadas = ["Cidade"] + transporte_selecionado
# if "Categoria_Renda" in df.columns:
#     colunas_selecionadas.append("Categoria_Renda")
# df_filtrado = df_filtrado[colunas_selecionadas]

# # Exibir os dados filtrados no Streamlit
# st.write("Dados filtrados:")
# st.dataframe(df_filtrado)


import streamlit as st
import pandas as pd
import plotly.express as px


# Configuração da Página
st.set_page_config(
    page_title="Dashboard - Personas de Mobilidade Urbana",
    page_icon="🏙️",
    layout="wide"
)


st.title("🏙️ Dashboard de Transporte e Mobilidade Urbana")
st.markdown("""
**Personas envolvidas no projeto:**
**Pedrinho** (Prefeito de Belo Horizonte - MG)
**Luciene** (Prefeita de Vitória - ES)
**Ana** (Gestora de Goiânia - GO)
**Lucas** (Especialista de Brasília - DF)
""")
st.markdown("---")


# Carregamento e Tratamento dos Dados
@st.cache_data
def load_data():
    df_raw = pd.read_excel('Tabela_13_Meio_de_transporte.xlsx', sheet_name='BR GR UF MU')
    
    cols = ['Localidade']
    raca_list = ['Branca', 'Preta ou Parda', 'Indígena']
    meios = ['A pé', 'Bicicleta', 'Motocicleta ou Mototaxi', 'Automóvel, taxi ou assemelhados', 'Transporte coletivo', 'Outros']
    
    for raca in raca_list:
        for meio in meios:
            cols.append(f"{raca} - {meio}")
            
    df_clean = df_raw.iloc[2:].copy()
    df_clean.columns = cols
    df_clean['Localidade'] = df_clean['Localidade'].astype(str).str.strip()
    
    for col in cols[1:]:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
    return df_clean


df = load_data()


# Cidades das Personas do Item 5
cidades_personas = ['Belo Horizonte (MG)', 'Vitória (ES)', 'Goiânia (GO)', 'Brasília (DF)']


# ==============================================================================
# BARRA LATERAL
# ==============================================================================
st.sidebar.header("🔍 Filtros de Análise")
modo_visualizacao = st.sidebar.radio(
    "Escolha o modo de visualização:",
    ["Comparativo entre as Cidades das Personas", "Análise Individual por Cidade"]
)


if modo_visualizacao == "Análise Individual por Cidade":
    cidade_selecionada = st.sidebar.selectbox("Selecione a Cidade da Persona:", cidades_personas)
else:
    cidade_selecionada = None


racas = ['Branca', 'Preta ou Parda', 'Indígena']
meios = ['A pé', 'Bicicleta', 'Motocicleta ou Mototaxi', 'Automóvel, taxi ou assemelhados', 'Transporte coletivo', 'Outros']


# ==============================================================================
# SEÇÃO 1: MODO COMPARATIVO ENTRE AS 4 CIDADES DAS PERSONAS
# ==============================================================================
if modo_visualizacao == "Comparativo entre as Cidades das Personas":
    st.header("📊 Comparativo Direto: Belo Horizonte vs. Vitória vs. Goiânia vs. Brasília")
    st.markdown("Este painel confronta diretamente os dados das cidades administradas/analisadas pelas personas do projeto.")


    # Extrair dados para as 4 cidades
    dados_comparativos = []
    for cid in cidades_personas:
        row = df[df['Localidade'] == cid]
        if not row.empty:
            r = row.iloc[0]
            for raca in racas:
                for meio in meios:
                    val = r[f"{raca} - {meio}"]
                    dados_comparativos.append({
                        'Cidade': cid,
                        'Cor/Raça': raca,
                        'Meio de Transporte': meio,
                        'Percentual (%)': val
                    })
    
    df_comp = pd.DataFrame(dados_comparativos)


    # GRÁFICO 1: Comparação Geral de Modais entre as Cidades das Personas
    fig_comp1 = px.bar(
        df_comp,
        x="Meio de Transporte",
        y="Percentual (%)",
        color="Cidade",
        barmode="group",
        title="Uso de Modais de Transporte por Cidade das Personas",
        text_auto='.1f'
    )
    fig_comp1.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig_comp1, use_container_width=True)


    st.markdown("---")


    # GRÁFICO 2: Boxplot da Dispersão de Tempos/Percentuais entre as Cidades
    fig_comp2 = px.box(
        df_comp,
        x="Cidade",
        y="Percentual (%)",
        color="Cidade",
        points="all",
        title="Distribuição Estatística dos Modais por Cidade das Personas"
    )
    st.plotly_chart(fig_comp2, use_container_width=True)


# ==============================================================================
# SEÇÃO 2: MODO ANÁLISE INDIVIDUAL POR CIDADE DA PERSONA
# ==============================================================================
else:
    st.header(f"📍 Análise Detalhada: **{cidade_selecionada}**")
    
    df_loc = df[df['Localidade'] == cidade_selecionada].iloc[0]
    
    meios_data = []
    for raca in racas:
        for meio in meios:
            val = df_loc[f"{raca} - {meio}"]
            meios_data.append({'Cor/Raça': raca, 'Meio de Transporte': meio, 'Percentual (%)': val})
            
    df_graficos = pd.DataFrame(meios_data)


    # Pergunta 1: Mediana por meio de transporte por raça (KPIs + Gráfico)
    st.subheader("1. Mediana e Distribuição por Raça e Modal")
    medianas_raca = df_graficos.groupby('Cor/Raça')['Percentual (%)'].median()
    
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Mediana (Branca)", value=f"{medianas_raca.get('Branca', 0):.1f}%")
    with col_kpi2:
        st.metric(label="Mediana (Preta ou Parda)", value=f"{medianas_raca.get('Preta ou Parda', 0):.1f}%")
    with col_kpi3:
        st.metric(label="Mediana (Indígena)", value=f"{medianas_raca.get('Indígena', 0):.1f}%")


    fig_ind1 = px.bar(
        df_graficos,
        x="Meio de Transporte",
        y="Percentual (%)",
        color="Cor/Raça",
        barmode="group",
        title=f"Modais de Transporte por Cor/Raça em {cidade_selecionada}",
        text_auto='.1f'
    )
    st.plotly_chart(fig_ind1, use_container_width=True)


    st.markdown("---")


    # Pergunta 2: Transporte Público vs Particular vs Ativo
    st.subheader("2. Proporção: Público vs. Particular vs. Ativo")
    def categorizar_modal(meio):
        if meio == 'Transporte coletivo':
            return 'Público (Ônibus/Metrô)'
        elif meio in ['Automóvel, taxi ou assemelhados', 'Motocicleta ou Mototaxi']:
            return 'Particular (Carro/Moto)'
        elif meio in ['A pé', 'Bicicleta']:
            return 'Ativo (Bicicleta/A pé)'
        return 'Outros'


    df_graficos['Categoria Modal'] = df_graficos['Meio de Transporte'].apply(categorizar_modal)
    df_cat = df_graficos.groupby('Categoria Modal')['Percentual (%)'].sum().reset_index()


    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_ind2 = px.pie(
            df_cat,
            values='Percentual (%)',
            names='Categoria Modal',
            title=f"Proporção de Modais em {cidade_selecionada}",
            hole=0.4
        )
        st.plotly_chart(fig_ind2, use_container_width=True)
    with col_g2:
        fig_ind3 = px.bar(
            df_graficos,
            x="Cor/Raça",
            y="Percentual (%)",
            color="Categoria Modal",
            title=f"Categorias de Transporte por Raça ({cidade_selecionada})",
            text_auto='.1f'
        )
        st.plotly_chart(fig_ind3, use_container_width=True)


st.markdown("---")


# ==============================================================================
# CONTEÚDO ADICIONAL DAS PERSONAS
# ==============================================================================
st.header("📰 Contexto e Notícias para as Rodas de Conversa das Personas")
st.markdown("""
 **Discussão Estratégica:** A gestão integrada entre Fernando (Nacional), Ana (Goiânia), Luciene (Vitória), Pedrinho (Belo Horizonte) e Lucas (Brasília) aponta para a necessidade urgente de investimentos em **mobilidade sustentável**, priorizando o transporte público coletivo de alta capacidade e a segurança nos modais ativos para todas as etnias.
""")