# Importando e carregando a base

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr,spearmanr

df = pd.read_csv('../data/desafio_nps_fase_1.csv')

"""# Exploração inicial da base - Sanity Check
#### Entendendo a "saúde" do dataset.
#### Antes de qualquer análise, precisamos garantir que a base está íntegra.
"""

print("Dimensão do dataset:\n")
print(df.shape)

print("Visão geral dos dados:\n")
print(df.head())

print("Tipos de dados:")
print(df.dtypes)

print("Informações gerais:\n")
df.info()

print("Estatísticas descritivas da base: \n")
print(df.describe())

# Verificando se há dados faltantes que possam comprometer a análise
print("Valores nulos:\n")
print(df.isnull().sum())

# Verificando duplicatas - registros duplicados podem inflar métricas
print("Valores duplicados:")
print(df.duplicated().sum())

"""# Verificando se há viéses no dataset

## Por variável única

### customer_id
#### Se houver clientes repetidos, pode indicar múltiplas compras no período
"""

print("Verificando se os identificadores dos clientes são únicos\n")
print(df['customer_id'].nunique() == len(df))

"""### order_id
#### Cada linha deve representar um pedido único - se não for, temos problema
"""

print("Verificando se os pedidos são únicos\n")
print(df['order_id'].nunique() == len(df))

"""### customer_age
#### Verificando se a base está concentrada em alguma faixa etária específica
#### (viés de amostragem)
"""

print("Concentração em faixa etária?\n")
sns.histplot(df['customer_age'], bins=20, kde=True)
plt.title('Distribuição de Idade dos Clientes')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.show()

sns.boxplot(x=df['customer_age'])
plt.title('Boxplot de Idade')
plt.show()

"""### customer_region
#### Verificando distribuição geográfica - se uma região domina a base,
#### os insights podem não ser generalizáveis
"""

print("Verificando se há inconsistências nos dados de região:\n")
print(df.describe(include='object'))

print(df['customer_region'].unique())

print("Existe viés de região na base?\n")
print(df['customer_region'].value_counts(normalize=True))

df['customer_region'].value_counts().plot(kind='bar')

"""### customer_tenure_months
#### Tempo de relacionamento pode influenciar a tolerância do cliente
"""

print(df['customer_tenure_months'].describe())

sns.histplot(df['customer_tenure_months'], bins=20)
plt.title("Tempo de Relacionamento")
plt.show()

"""### items_quantity
#### Pedidos com muitos itens podem ter mais chance de problemas logísticos
"""

sns.countplot(x=df['items_quantity'])
plt.title("Quantidade de Itens por Pedido")
plt.show()

"""### repeat_purchase_30d
#### Recompra é um indicador forte de satisfação real - cliente satisfeito volta
"""

counts = df['repeat_purchase_30d'].value_counts()

plt.figure(figsize=(6,6))
plt.pie(
    counts,
    labels=['Não comprou novamente', 'Comprou novamente'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#ff9999','#66b3ff']
)

plt.title('Recompra em até 30 dias')
plt.show()

"""### nps_score
#### Variável alvo do desafio - é a nota de satisfação que queremos entender e prever
"""

sns.histplot(df['nps_score'], bins=11)
plt.title("Distribuição NPS")
plt.show()

# Classificação padrão do NPS:
# 9-10 = Promotor (ama a marca, recomenda)
# 7-8 = Neutro (satisfeito mas não engajado)
# 0-6 = Detrator (insatisfeito, pode falar mal)
def classificar_nps(score):
    if score >= 9:
        return 'Promotor'
    elif score >= 7:
        return 'Neutro'
    else:
        return 'Detrator'

df['nps_class'] = df['nps_score'].apply(classificar_nps)

proporcoes = df['nps_class'].value_counts(normalize=True)

# NPS da empresa = % Promotores - % Detratores (varia de -100 a +100)
nps_empresa = (proporcoes.get('Promotor', 0) - proporcoes.get('Detrator', 0)) * 100
print(f"NPS da empresa: {nps_empresa:.2f}")

print(f"\nNPS médio: {df['nps_score'].mean():.2f}")

print(df['nps_score'].describe())

print(df['nps_class'].value_counts())

proporcoes = df['nps_class'].value_counts(normalize=True)
print(proporcoes)

"""## Correlacionando variáveis

### Correlacionando NPS
#### Aqui queremos descobrir quais variáveis têm relação com a satisfação do cliente.
#### Usamos Pearson para medir a força da relação linear entre cada variável e o NPS.
"""

# Selecionar apenas colunas numéricas
numericas = df.select_dtypes(include=['int64', 'float64']).columns

resultados = []

for col in numericas:
    if col != 'nps_score':
        corr, p_value = pearsonr(df[col], df['nps_score'])

        resultados.append({
            'variavel': col,
            'correlacao': corr,
            'p_value': p_value
        })

# Criar dataframe final
df_resultado = pd.DataFrame(resultados)

# Ordenar por impacto (valor absoluto da correlação)
# Quanto maior o abs_corr, mais forte a relação com o NPS
df_resultado['abs_corr'] = df_resultado['correlacao'].abs()
df_resultado = df_resultado.sort_values(by='abs_corr', ascending=False)

print(df_resultado)

# Filtrando variáveis estatisticamente significativas
# abs_corr > 0.1 = correlação minimamente relevante
# p_value < 0.05 = resultado não é por acaso (95% de confiança)
df_resultado_filtrado = df_resultado[
    (df_resultado['abs_corr'] > 0.1) &
    (df_resultado['p_value'] < 0.05)
]

# Comparando Pearson (relação linear) vs Spearman (relação monotônica)
# Se Spearman > Pearson, a relação existe mas não é perfeitamente linear
for v in df_resultado_filtrado['variavel']:
    p_corr, _ = pearsonr(df[v], df['nps_score'])
    s_corr, _ = spearmanr(df[v], df['nps_score'])

    print(f"{v}")
    print(f"  Pearson:  {p_corr:.3f}")
    print(f"  Spearman: {s_corr:.3f}\n")

"""Quais fatores parecem mais críticos para a satisfação?
#### Visualizando de forma clara quais variáveis puxam o NPS pra cima ou pra baixo
"""

corr = df.corr(numeric_only=True)['nps_score'].drop('nps_score')
corr = corr.sort_values()

plt.figure(figsize=(8,6))

corr.plot(kind='barh', color='gray')

for i, v in enumerate(corr):
    color = 'red' if v < 0 else 'green'
    plt.barh(corr.index[i], v, color=color)

plt.title('Fatores que Impactam a Satisfação do Cliente (NPS)')
plt.xlabel('Correlação com NPS')
plt.ylabel('Variáveis')

plt.show()

"""O que mais gera detratores?
#### Focando nas variáveis que têm correlação negativa com o NPS
#### (quanto maior o valor da variável, pior a satisfação)
"""

# Selecionando variáveis com impacto negativo no NPS e estatisticamente significativas
# correlacao < -0.1 = relação inversa relevante (mais X = menos NPS)
drivers = df_resultado[
    (df_resultado['correlacao'] < -0.1) &
    (df_resultado['p_value'] < 0.05)
]['variavel']

for var in drivers:

    # cria a flag de detrator (NPS 0-6)
    is_detrator = df['nps_score'] <= 6

    # calcula % de detratores por valor da variável
    # impacto = diferença entre o pior e o melhor cenário
    taxa = is_detrator.groupby(df[var]).mean()

    print(f"\n{var}")
    print(f"Impacto: {taxa.max() - taxa.min():.2%}")

"""Base de detratores
#### Criando uma base específica para analisar o perfil de quem dá notas baixas
"""

df_detratores = df.copy()
df_detratores['is_detrator'] = df_detratores['nps_score'] <= 6

"""% de Detratores por delivery_delay_days
#### Quebrando o atraso em faixas para entender a partir de quantos dias o cliente fica insatisfeito
"""

#faixas de atraso
df_detratores['faixa_atraso'] = pd.cut(
    df_detratores['delivery_delay_days'],
    bins=[-10, 0, 2, 5, 100],
    labels=['Sem atraso', '1-2 dias', '3-5 dias', '5+ dias']
)

# % de detratores
detratores = df_detratores.groupby('faixa_atraso', observed=True)['is_detrator'].mean()

plt.figure(figsize=(8,5))

detratores.plot(kind='bar', color=['#d3d3d3', '#d3d3d3', '#ff4d4d', '#b30000'])

for i, v in enumerate(detratores):
    plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')

plt.title('% de Detratores por Atraso na Entrega')
plt.xlabel('Atraso na Entrega')
plt.ylabel('% de Detratores')
plt.ylim(0,1.05)
plt.xticks(rotation=0)

plt.show()

"""% de Detratores por complaints_count
#### Quantas reclamações são necessárias para o cliente virar detrator?
"""

df_detratores['faixa_reclamacoes'] = pd.cut(
    df_detratores['complaints_count'],
    bins=[-1, 0, 2, 5, 100],
    labels=['0', '1-2', '3-5', '5+']
)

detratores = df_detratores.groupby('faixa_reclamacoes', observed=True)['is_detrator'].mean()

plt.figure(figsize=(8,5))

detratores.plot(kind='bar', color=['#d3d3d3', '#d3d3d3', '#ff4d4d', '#b30000'])

for i, v in enumerate(detratores):
    plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')

plt.title('% de Detratores por Número de Reclamações')
plt.xlabel('Número de Reclamações')
plt.ylabel('% de Detratores')
plt.ylim(0,1.05)
plt.xticks(rotation=0)

plt.show()

"""% de Detratores por customer_service_contacts
#### Muitos contatos com atendimento = experiência ruim (cliente precisou insistir)
"""

df_detratores['faixa_contato'] = pd.cut(
    df_detratores['customer_service_contacts'],
    bins=[-1, 0, 2, 5, 100],
    labels=['0', '1-2', '3-5', '5+']
)

detratores = df_detratores.groupby('faixa_contato', observed=True)['is_detrator'].mean()

plt.figure(figsize=(8,5))

detratores.plot(kind='bar', color=['#d3d3d3', '#d3d3d3', '#ff4d4d', '#b30000'])

for i, v in enumerate(detratores):
    plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')

plt.title('% de Detratores por N.º de Contatos com Atendimento')
plt.xlabel('Contatos com Atendimento')
plt.ylabel('% de Detratores')
plt.ylim(0,1.05)
plt.xticks(rotation=0)

plt.show()

"""% de Detratores por resolution_time_days
#### Tempo de resolução longo = cliente esperando = frustração acumulada
"""

df_detratores['faixa_resolucao'] = pd.cut(
    df_detratores['resolution_time_days'],
    bins=[-1, 1, 3, 7, 100],
    labels=['Até 1 dia', '2-3 dias', '4-7 dias', '7+ dias']
)

detratores = df_detratores.groupby('faixa_resolucao', observed=True)['is_detrator'].mean()

plt.figure(figsize=(8,5))

detratores.plot(kind='bar', color=['#d3d3d3', '#d3d3d3', '#ff4d4d', '#b30000'])

for i, v in enumerate(detratores):
    plt.text(i, v + 0.01, f'{v:.1%}', ha='center')

plt.title('% de Detratores por Tempo de Resolução')
plt.xlabel('Tempo de Resolução (dias)')
plt.ylabel('% de Detratores')
plt.ylim(0,1.05)
plt.xticks(rotation=0)

plt.show()

"""### NPS vs Atraso de entrega
#### Atraso na entrega é o fator mais óbvio de insatisfação - vamos quantificar
"""

df_atraso = df.copy()
df_atraso['teve_atraso'] = df['delivery_delay_days'] > 0

print(df_atraso.groupby('teve_atraso')['nps_score'].mean())

df_atraso.groupby('teve_atraso')['nps_score'].mean().plot(kind='bar')

plt.xticks([0,1], ['Sem atraso', 'Com atraso'], rotation=0)
plt.ylabel('NPS médio')
plt.title('Impacto do atraso na entrega no NPS')
plt.show()

df_atraso['faixa_atraso'] = pd.cut(
    df_atraso['delivery_delay_days'],
    bins=[-10, 0, 2, 5, 100],
    labels=['Sem atraso', '1-2 dias', '3-5 dias', '5+ dias']
)

print(df_atraso.groupby('faixa_atraso')['nps_score'].mean())

df_atraso.groupby('faixa_atraso')['nps_score'].mean().plot(kind='bar')

plt.ylabel('Nota média de satisfação')
plt.title('Impacto do nível de atraso no NPS')
plt.xticks(rotation=0)
plt.show()

"""### NPS vs Número de Reclamações
#### Reclamações são sintoma de problemas acumulados - quanto mais reclama, pior a nota
"""

print(df[['complaints_count', 'nps_score']].corr())

sns.regplot(
    x='complaints_count',
    y='nps_score',
    data=df,
    scatter_kws={'alpha':0.3, 'color': 'gray'},
    line_kws={'color': 'red', 'linewidth': 2}
)

volume = df['complaints_count'].value_counts().sort_index()
media_nps = df.groupby('complaints_count')['nps_score'].mean()

# Criar figura
fig, ax1 = plt.subplots(figsize=(10,5))

# Barras (volume)
ax1.bar(volume.index, volume.values, color='lightgray')
ax1.set_xlabel('Número de Reclamações')
ax1.set_ylabel('Quantidade de Clientes', color='gray')

# Linha (NPS médio)
ax2 = ax1.twinx()
ax2.plot(media_nps.index, media_nps.values, color='red', marker='o', linewidth=2)
ax2.set_ylabel('Nota média de satisfação', color='red')

# Título
plt.title('Impacto das Reclamações na Satisfação do Cliente')

plt.show()

"""## Buscando o ponto de ruptura

Existe algum “ponto de ruptura” na experiência do cliente?
#### A ideia aqui é encontrar o valor exato onde a satisfação despenca.
#### Ex: a partir de X dias de atraso, o NPS cai drasticamente.
#### Isso é útil para definir SLAs e alertas operacionais.
"""

# Calculando o impacto total de cada variável (diferença entre melhor e pior cenário)
impactos = []

for var in drivers:
    is_detrator = df['nps_score'] <= 6
    taxa = is_detrator.groupby(df[var]).mean()
    impacto = taxa.max() - taxa.min()
    impactos.append((var, impacto))

df_impacto = pd.DataFrame(impactos, columns=['variavel', 'impacto'])
df_impacto = df_impacto.sort_values(by='impacto', ascending=False)
print(df_impacto)

# Função para encontrar o ponto de ruptura (o valor onde o NPS sofre a maior queda)
# Lógica: calcula a média de NPS por valor da variável, depois pega a maior queda entre valores consecutivos
def encontrar_ruptura(df, var):
    serie = df.groupby(var)['nps_score'].mean().sort_index()
    diff = serie.diff()
    return diff.idxmin()

# Plotando tabela com resultados dos pontos de ruptura por metrica
resultados = []

for var in df_impacto['variavel']:
    ruptura = encontrar_ruptura(df, var)

    resultados.append({
        'variavel': var,
        'ponto_ruptura': ruptura
    })

# Criar tabela
df_ruptura = pd.DataFrame(resultados)

# (Opcional) melhorar nomes para apresentação
df_ruptura['nome_variavel'] = df_ruptura['variavel'].replace({
    'complaints_count': 'Nº de Reclamações',
    'delivery_delay_days': 'Atraso na Entrega (dias)',
    'customer_service_contacts': 'Contatos com Atendimento',
    'resolution_time_days': 'Tempo de Resolução (dias)'
})

print(df_ruptura[['nome_variavel', 'ponto_ruptura']].sort_values(by='ponto_ruptura'))

"""## Analisando perfil dos clientes
#### Entendendo quem são os clientes da base para identificar se algum perfil
#### específico tende a ser mais ou menos satisfeito
"""

# distribuicao etaria
plt.figure(figsize=(8,5))
plt.hist(df['customer_age'], bins=50)
plt.xlabel('Idade')
plt.ylabel('Quantidade de clientes')
plt.title('Distribuição Etária')
plt.show()

#clientes por região
regiao_counts = df['customer_region'].value_counts()

plt.figure(figsize=(6,6))

plt.pie(
    regiao_counts,
    labels=regiao_counts.index,
    autopct='%1.1f%%',  # mostrar %
    startangle=90
)

plt.title('Distribuição de Clientes por Região')

plt.show()

# tempo como cliente
plt.figure(figsize=(8,5))
plt.hist(df['customer_tenure_months'], bins=50)
plt.xlabel('Tempo como cliente (meses)')
plt.ylabel('Quantidade de clientes')
plt.title('Distribuição de Tempo de Relacionamento')
plt.show()

"""Que tipo de cliente tende a ter NPS mais alto ou mais baixo?
#### Comparando o perfil médio de Promotores vs Detratores
#### Isso ajuda a entender o que diferencia um cliente satisfeito de um insatisfeito
"""

# Criando categorias de NPS para agrupar os clientes
df_grupo = df.copy()
df_grupo['grupo_nps'] = pd.cut(
    df_grupo['nps_score'],
    bins=[-1, 6, 8, 10],
    labels=['Detrator', 'Neutro', 'Promotor']
)

# Analisando perfil de cada grupo

metricas = df.select_dtypes(include='number').columns.tolist()

# Removendo NPS e IDs (não fazem sentido na comparação de perfil)
metricas = [
    col for col in metricas
    if col not in ['nps_score', 'customer_id', 'order_id']
]

# Perfil numérico por grupo de NPS
# Aqui conseguimos ver, por exemplo, que detratores têm mais atraso, mais reclamações etc.
perfil_numerico = df.groupby('grupo_nps', observed=True)[metricas].mean().round(2)

print("Perfil médio por grupo de NPS:\n")
print(perfil_numerico.T)


# Distribuição por região (em %)
# Verificando se alguma região concentra mais detratores ou promotores
perfil_regiao = (
      df.groupby(['grupo_nps', 'customer_region'], observed=True)
      .size()
      .unstack(fill_value=0)
)

perfil_regiao_pct = perfil_regiao.div(perfil_regiao.sum(axis=1), axis=0).round(2)

print("\nDistribuição percentual por região:\n")
print(perfil_regiao_pct.T)