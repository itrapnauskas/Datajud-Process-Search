from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import time
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Substitua por uma chave secreta segura

# Chave de API fornecida - disponível em https://datajud-wiki.cnj.jus.br/api-publica/acesso
API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

# Cabeçalhos padrão para as requisições
HEADERS = {
    "Authorization": f"APIKey {API_KEY}",
    "Content-Type": "application/json"
}

# Base URL da API Pública do Datajud
BASE_URL = "https://api-publica.datajud.cnj.jus.br/"

# Dicionário de tribunais com seus respectivos aliases
TRIBUNAIS = {
    "TST": "api_publica_tst/_search",
    "TSE": "api_publica_tse/_search",
    "STJ": "api_publica_stj/_search",
    "STM": "api_publica_stm/_search",
    "TRF1": "api_publica_trf1/_search",
    "TRF2": "api_publica_trf2/_search",
    "TRF3": "api_publica_trf3/_search",
    "TRF4": "api_publica_trf4/_search",
    "TRF5": "api_publica_trf5/_search",
    "TRF6": "api_publica_trf6/_search",
    "TJDFT": "api_publica_tjdft/_search",
    # Adicione outros tribunais conforme necessário
}

# Carregar Classes Processuais e Assuntos Processuais
def carregar_dados():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    classes_path = os.path.join(base_dir, 'data', 'classes_processuais.json')
    assuntos_path = os.path.join(base_dir, 'data', 'assuntos_processuais.json')

    # Verificar se os arquivos existem
    if not os.path.exists(classes_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {classes_path}")
    if not os.path.exists(assuntos_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {assuntos_path}")

    with open(classes_path, 'r', encoding='utf-8') as f:
        classes_processuais = json.load(f)

    with open(assuntos_path, 'r', encoding='utf-8') as f:
        assuntos_processuais = json.load(f)

    return classes_processuais, assuntos_processuais

CLASSES_PROCESSUAIS, ASSUNTOS_PROCESSUAIS = carregar_dados()

# Função para buscar processos com paginação
def buscar_processos_com_paginacao(tribunal, consulta_dsl, tamanho_pagina=100, max_paginas=10):
    """
    Busca processos com uma consulta DSL personalizada e paginação.
    
    :param tribunal: Sigla do tribunal (ex: 'TRF1')
    :param consulta_dsl: Dicionário com a consulta DSL
    :param tamanho_pagina: Número de registros por página
    :param max_paginas: Número máximo de páginas a serem buscadas
    :return: Lista de processos
    """
    endpoint = TRIBUNAIS.get(tribunal.upper())
    if not endpoint:
        raise ValueError(f"Tribunal '{tribunal}' não está configurado.")
    
    url = f"{BASE_URL}{endpoint}"
    
    query = consulta_dsl.copy()
    query["size"] = tamanho_pagina
    query["sort"] = [
        {
            "@timestamp": {
                "order": "asc"
            }
        }
    ]
    
    todos_processos = []
    ultimo_sort = None
    paginas = 0

    while paginas < max_paginas:
        if ultimo_sort:
            query["search_after"] = ultimo_sort

        try:
            response = requests.post(url, headers=HEADERS, data=json.dumps(query))
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            break
        
        dados = response.json()
        hits = dados.get("hits", {}).get("hits", [])
        
        if not hits:
            print("Nenhum mais processo encontrado.")
            break
        
        todos_processos.extend([hit["_source"] for hit in hits])
        ultimo_sort = hits[-1].get("sort")
        paginas += 1

        print(f"Página {paginas} processada. Total de processos coletados: {len(todos_processos)}")
        
        # Respeitar limites de taxa da API
        time.sleep(1)  # Ajuste conforme a política da API

    return todos_processos

# Rota principal para exibir o formulário de pesquisa
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Coleta os dados do formulário
        tribunal = request.form.get('tribunal')
        numero_processo = request.form.get('numero_processo')
        data_ajuizamento = request.form.get('data_ajuizamento')
        grau = request.form.get('grau')
        classe_codigo = request.form.get('classe_codigo')
        orgao_julgador_codigo = request.form.get('orgao_julgador_codigo')
        assunto_codigo = request.form.get('assunto_codigo')
        
        # Construção da consulta DSL com base nos campos preenchidos
        must_clauses = []
        
        if numero_processo:
            must_clauses.append({"match": {"numeroProcesso": numero_processo}})
        if data_ajuizamento:
            must_clauses.append({"match": {"dataAjuizamento": data_ajuizamento}})
        if grau and grau != "":
            must_clauses.append({"match": {"grau": grau}})
        if classe_codigo and classe_codigo != "":
            try:
                classe_codigo_int = int(classe_codigo)
                must_clauses.append({"match": {"classe.codigo": classe_codigo_int}})
            except ValueError:
                pass  # Ignorar se não for um número válido
        if orgao_julgador_codigo and orgao_julgador_codigo != "":
            try:
                orgao_julgador_codigo_int = int(orgao_julgador_codigo)
                must_clauses.append({"match": {"orgaoJulgador.codigo": orgao_julgador_codigo_int}})
            except ValueError:
                pass
        if assunto_codigo and assunto_codigo != "":
            try:
                assunto_codigo_int = int(assunto_codigo)
                must_clauses.append({"match": {"assuntos.codigo": assunto_codigo_int}})
            except ValueError:
                pass

        # Apenas adicionar a consulta se houver cláusulas
        if must_clauses:
            consulta_dsl = {
                "query": {
                    "bool": {
                        "must": must_clauses
                    }
                }
            }
        else:
            # Caso nenhum filtro seja selecionado, retornar todos (cuidado com grandes volumes)
            consulta_dsl = {
                "query": {
                    "match_all": {}
                }
            }

        # Realiza a busca com paginação (limitando a 5 páginas para evitar sobrecarga)
        try:
            processos = buscar_processos_com_paginacao(
                tribunal=tribunal,
                consulta_dsl=consulta_dsl,
                tamanho_pagina=100,
                max_paginas=5
            )
            return render_template('results.html', processos=processos)
        except Exception as e:
            # Capturar exceções e passar a mensagem de erro para o template
            error_message = f"Erro ao buscar processos: {str(e)}"
            return render_template('results.html', processos=[], error=error_message)
    
    # Para o método GET, passar as classes e assuntos
    return render_template('search.html', 
                           tribunais=TRIBUNAIS.keys(),
                           classes_processuais=CLASSES_PROCESSUAIS,
                           assuntos_processuais=ASSUNTOS_PROCESSUAIS)

# Rota para exibir os resultados da pesquisa
@app.route('/results')
def results():
    return redirect(url_for('search'))  # Redireciona para a página de pesquisa

# Rota para obter assuntos com base na classe selecionada
@app.route('/get_assuntos/<classe>')
def get_assuntos(classe):
    """
    Retorna os assuntos correspondentes à classe processual selecionada.
    
    :param classe: Nome da classe processual
    :return: JSON com os assuntos
    """
    # Navegar na estrutura de assuntos_processuais para encontrar os correspondentes à classe
    assuntos = ASSUNTOS_PROCESSUAIS.get(classe, {})
    return jsonify(assuntos)

# Função opcional para salvar os resultados em CSV
def salvar_processos_em_csv(processos, nome_arquivo):
    """
    Salva a lista de processos em um arquivo CSV.
    
    :param processos: Lista de dicionários com os dados dos processos
    :param nome_arquivo: Nome do arquivo CSV de saída
    """
    df = pd.json_normalize(processos)
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f"Dados salvos em {nome_arquivo}")

if __name__ == '__main__':
    app.run(debug=True)
