# Datajud Process Search

## Descrição

**Datajud Process Search** é uma aplicação web desenvolvida em Flask que permite pesquisar processos jurídicos utilizando a API pública do Datajud. Através de uma interface simples, os usuários podem filtrar processos por tribunal, número do processo, data de ajuizamento, grau, classe processual, assunto processual e órgão julgador.

> **Nota:** Este é um projeto inicial desenvolvido em uma tarde, com *muitas* oportunidades para melhorias. Contribuições são bem-vindas!

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask**
- **Requests**
- **Pandas**
- **HTML/CSS**
- **JavaScript**
- **JSON**

## Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/itrapnauskas/Datajud-Process-Search.git
cd Datajud-Process-Search
```

### 2. Criar e Ativar um Ambiente Virtual (Opcional, mas Recomendado)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a Chave de API

A API Pública do Datajud é uma ferramenta que disponibiliza ao público o acesso aos metadados dos processos públicos dos tribunais do judiciário brasileiro. Os dados disponibilizados pela API são de origem da Base Nacional de Dados do Poder Judiciário – Datajud e atendem aos critérios estabelecidos pela Portaria Nº 160 de 09/09/2020.

**API Key**

# Start of Selection
A autenticação da API Pública do Datajud é realizada através de uma Chave Pública, gerada e disponibilizada pelo DPJ/CNJ. A chave vigente estará sempre acessível na **[Wiki](https://datajud-wiki.cnj.jus.br/api-publica/acesso)**, garantindo transparência e facilitando o acesso. Importante ressaltar que, por razões de segurança e gestão do sistema, a chave poderá ser alterada pelo CNJ a qualquer momento.

Para incorporar a API Key em suas requisições, utilize o formato `"Authorization: APIKey [Chave Pública]"` no cabeçalho da requisição.

**APIKey atual:**

```
Authorization: APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
```

Abra o arquivo `app.py` e substitua `'your_secret_key_here'` e o valor de `API_KEY` por suas próprias chaves seguras.

```python
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
API_KEY = "sua_api_key_aqui"
```

## Uso

### Rodar a Aplicação

```bash
python app.py
```

Abra seu navegador e vá para [http://127.0.0.1:5000/](http://127.0.0.1:5000/) para acessar a aplicação.

### Realizar uma Pesquisa

1. **Tribunal**: Selecione o tribunal desejado.
2. **Número do Processo**: Insira o número do processo (opcional).
3. **Data de Ajuizamento**: Selecione a data de ajuizamento (opcional).
4. **Grau**: Selecione o grau do processo (G1, G2, JE).
5. **Classe Processual**: Selecione a classe processual.
6. **Assunto Processual**: Selecione o assunto processual correspondente.
7. **Órgão Julgador**: Insira o código do órgão julgador (opcional).

Clique em **Pesquisar** para ver os resultados.

## Contribuindo

Este é um projeto inicial com muito a melhorar. Se você deseja contribuir, sinta-se à vontade para:

- **Abrir Issues**: Relate bugs ou sugira melhorias.
- **Enviar Pull Requests**: Proponha alterações no código.
- **Participar das Discussões**: Compartilhe ideias e feedback.

Toda contribuição é bem-vinda! Vamos juntos aprimorar esta ferramenta.

## Palavras-chave

Flask, Python, Datajud, Pesquisa de Processos, API, Aplicação Web, Jurídico, Desenvolvimento Web

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
