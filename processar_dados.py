import pandas as pd

# Dicionário com o nome dos times e os arquivos CSV correspondentes
arquivos_csv = {
    "Athletico Paranaense": "Athletico Paranaense_videos_and_comments.csv",
    "Atletico Goianiense": "Atlético Goianiense_videos_and_comments.csv",
    "Atletico Mineiro": "GaloTV_videos_and_comments.csv",
    "Bahia": "Bahia_videos_and_comments.csv",
    "Botafogo": "Botafogo Tv_videos_and_comments.csv",
    "Bragantino": "Bragantino_videos_and_comments.csv",
    "Corinthians": "Corinthians_videos_and_comments.csv",
    "Criciuma": "Criciuma_videos_and_comments.csv",
    "Cruzeiro": "Cruzeiro Tv_videos_and_comments.csv",
    "Flamengo": "FlamengoTV_videos_and_comments.csv",
    "Fluminense": "Fluminense Tv_videos_and_comments.csv",
    "Fortaleza": "Fortaleza_videos_and_comments.csv",
    "Gremio": "Gremio_videos_and_comments.csv",
    "Internacional": "Internacional_videos_and_comments.csv",
    "Juventude": "Juventude_videos_and_comments.csv",
    "Palmeiras": "PalmeirasTV_videos_and_comments.csv",
    "Sao Paulo": "São Paulo_videos_and_comments.csv",
    "Vasco": "Vasco TV_videos_and_comments.csv",
    "Vitoria": "Vitoria_videos_and_comments.csv"
    
    
}

# Inicializar uma lista para armazenar os dados
dados = []

# Ler cada arquivo CSV e adicionar a coluna "time"
for time, arquivo in arquivos_csv.items():
    # Lê o arquivo CSV
    df = pd.read_csv(arquivo, names=["video_title", "video_id", "comment_author", "comment_text", "comment_likes"])
    
    # Adiciona o nome do time como uma nova coluna no DataFrame
    df["time"] = time
    
    # Adiciona o DataFrame à lista
    dados.append(df)

# Concatenar todos os DataFrames da lista em um único DataFrame
dados_completos = pd.concat(dados, ignore_index=True)

# Salvar o DataFrame completo em um novo arquivo CSV (opcional)
dados_completos.to_csv("dados_completos.csv", index=False)

# Exibir uma amostra dos dados para verificar se tudo está correto
print(dados_completos.head())

#criacao da rede

import networkx as nx

# Criar o grafo (rede)
G = nx.Graph()

# Adicionar arestas entre usuários e vídeos
for _, row in dados_completos.iterrows():
    usuario = row["comment_author"]  # Nome do usuário
    video = row["video_id"]          # ID do vídeo
    time = row["time"]               # Time associado ao vídeo

    # Adicionar o vídeo como nó, com atributo "time"
    if not G.has_node(video):
        G.add_node(video, tipo="video", time=time)  # Nó do vídeo com atributo de tipo e time
    
    # Adicionar o usuário como nó, com atributo "tipo"
    if not G.has_node(usuario):
        G.add_node(usuario, tipo="usuario")  # Nó do usuário com atributo de tipo

    # Adicionar uma aresta entre o usuário e o vídeo
    if G.has_edge(usuario, video):
        G[usuario][video]["weight"] += 1  # Incrementar o peso se já existe uma interação
    else:
        G.add_edge(usuario, video, weight=1)  # Criar uma aresta nova com peso 1

print(f"Número de nós na rede: {G.number_of_nodes()}")

# Verificando o número de arestas
print(f"Número de arestas na rede: {G.number_of_edges()}")

# Salvar o grafo em formato GraphML
nx.write_graphml(G, "rede_completa.graphml")
print("Grafo salvo em formato GraphML como 'rede_completa.graphml'.")

# Salvar o grafo em formato GEXF (opcional, para uso em ferramentas como Gephi)
nx.write_gexf(G, "rede_completa.gexf")
print("Grafo salvo em formato GEXF como 'rede_completa.gexf'.")

import matplotlib
matplotlib.use('Agg')  # Usa um backend não interativo
import matplotlib.pyplot as plt


# 2)
# Calcular o grau de cada nó
graus = dict(G.degree())

# Criar um DataFrame para análise
graus_df = pd.DataFrame(list(graus.items()), columns=["Nodo", "Grau"])

# Plotar a distribuição dos graus
plt.figure(figsize=(10, 6))
graus_df["Grau"].hist(bins=50, color="skyblue", edgecolor="black")
plt.title("Distribuição do Grau dos Nodos")
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.yscale("log")  # Escala logarítmica no eixo Y
plt.savefig("distribuicao_grau_nodos.png")  # Salvar o gráfico
plt.show()

#Discuta se a curva parece uma power law
# Plotar a distribuição em escala log-log
plt.figure(figsize=(10, 6))
plt.loglog(sorted(graus.values(), reverse=True), marker="o", linestyle="None")
plt.title("Distribuição do Grau (Log-Log)")
plt.xlabel("Rank do Nó (ordem decrescente de grau)")
plt.ylabel("Grau")
plt.savefig("distribuicao_grau_loglog.png")
plt.show()

# Grau medio do grafo
grau_medio = sum(graus.values()) / len(graus)
print(f"Grau médio do grafo: {grau_medio}")

# 3)
# Identificar componentes conectados
componentes = list(nx.connected_components(G))
numero_componentes = len(componentes)
print(f"Número de componentes conectados no grafo: {numero_componentes}")

# Tamanho de cada componente
tamanhos_componentes = [len(c) for c in componentes]

# Caso tenha mais de 1 componente, plote a distribuição
if numero_componentes > 1:
    plt.figure(figsize=(10, 6))
    plt.hist(tamanhos_componentes, bins=50, color="orange", edgecolor="black")
    plt.title("Distribuição do Tamanho dos Componentes")
    plt.xlabel("Tamanho do Componente")
    plt.ylabel("Frequência")
    plt.savefig("distribuicao_componentes.png")
    plt.show()

# 4) Coeficiente de clusterização
# Calcular o coeficiente de clusterização para cada nó
coeficientes_clusterizacao = nx.clustering(G)

# Criar um DataFrame para análise
cluster_df = pd.DataFrame(coeficientes_clusterizacao.items(), columns=["Nodo", "Coeficiente"])

# Plotar a distribuição
plt.figure(figsize=(10, 6))
cluster_df["Coeficiente"].hist(bins=50, color="purple", edgecolor="black")
plt.title("Distribuição do Coeficiente de Clusterização")
plt.xlabel("Coeficiente de Clusterização")
plt.ylabel("Frequência")
plt.savefig("distribuicao_clusterizacao.png")
plt.show()

# Calcular o coeficiente global
coeficiente_global = nx.average_clustering(G)
print(f"Coeficiente de clusterização global do grafo: {coeficiente_global}")



# 6) Centralidade
#Page Rank

pagerank = nx.pagerank(G)

# Mostrar os nós mais importantes
importantes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nós mais importantes pelo PageRank:")
for nodo, valor in importantes:
    print(f"Nó: {nodo}, PageRank: {valor}")
    
    
# 7) Assortividade
assortatividade = nx.degree_assortativity_coefficient(G)
print(f"Coeficiente de assortatividade (Pearson): {assortatividade}")


resumo = {
    "grau_medio": grau_medio,
    "num_componentes": numero_componentes,
    "clusterizacao_global": coeficiente_global,
    "assortatividade": assortatividade,
}

with open("resumo_analise.txt", "w") as arquivo:
    for chave, valor in resumo.items():
        arquivo.write(f"{chave}: {valor}\n")
print("Resumo salvo em 'resumo_analise.txt'.")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import itertools

# Agrupar os usuários por time
usuarios_por_time = {}
for time in dados_completos["time"].unique():
    usuarios = set(dados_completos[dados_completos["time"] == time]["comment_author"])
    usuarios_por_time[time] = usuarios

# Criar uma matriz de sobreposição
times = list(usuarios_por_time.keys())
matriz_sobreposicao = pd.DataFrame(0, index=times, columns=times)

# Calcular a sobreposição entre cada par de times
for time1, time2 in itertools.combinations(times, 2):
    sobreposicao = len(usuarios_por_time[time1] & usuarios_por_time[time2])  # Interseção dos conjuntos
    matriz_sobreposicao.loc[time1, time2] = sobreposicao
    matriz_sobreposicao.loc[time2, time1] = sobreposicao

# Preenchendo a diagonal principal (número de usuários únicos por time)
for time in times:
    matriz_sobreposicao.loc[time, time] = len(usuarios_por_time[time])

# Salvar a matriz em CSV para análise posterior (opcional)
matriz_sobreposicao.to_csv("matriz_sobreposicao.csv", index=True)

# Plotar a matriz de calor da sobreposição
plt.figure(figsize=(12, 10))
sns.heatmap(matriz_sobreposicao, annot=True, fmt="d", cmap="Blues", cbar=True)
plt.title("Sobreposição de Usuários entre os Times")
plt.xlabel("Time")
plt.ylabel("Time")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Salvar o gráfico
plt.savefig("matriz_sobreposicao.png")
plt.show()
