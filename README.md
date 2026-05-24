# Sprint 4 IoT - OracleLearn IA de Predicao de Evasao

## Descricao

Este projeto implementa uma solucao de Inteligencia Artificial para prever o risco de evasao de alunos na plataforma OracleLearn.

A solucao utiliza um modelo de classificacao treinado com indicadores de engajamento academico. O resultado da predicao informa o nivel de risco do aluno, a probabilidade de evasao e uma recomendacao de intervencao.

## Objetivo

Identificar alunos com maior probabilidade de abandono para apoiar a tomada de decisao de tutores e coordenadores.

Variaveis utilizadas pelo modelo:

- `horas_estudadas`
- `exercicios_concluidos`
- `media_notas`
- `dias_inativos`

## Funcionalidades

- Geracao de base sintetica de alunos.
- Treinamento de modelo de classificacao.
- Salvamento do modelo treinado em arquivo `.pkl`.
- Exposicao do modelo por API REST.
- Cadastro de alunos.
- Listagem e remocao de alunos cadastrados.
- Processamento individual e em lote.
- Exibicao de risco, probabilidade de evasao e recomendacao.
- Painel demonstrativo em Streamlit.

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest Classifier
- Flask
- Flask-CORS
- Streamlit

## Modelo de IA

O modelo utilizado foi o `RandomForestClassifier`, adequado para problemas de classificacao supervisionada. A saida do modelo indica se o aluno apresenta ou nao risco de evasao.

O treinamento gera:

- dataset sintetico em `data/alunos_evasao_sintetico.csv`
- modelo treinado em `models/modelo_evasao.pkl`
- metricas em `metrics/model_metrics.json`

Metricas obtidas no treinamento:

- Acuracia: 90.8%
- Variavel mais relevante: `dias_inativos`
- Matriz de confusao e relatorio de classificacao salvos em JSON

## Estrutura do Projeto

```text
Sprint4Iot/
  ai_core.py
  api.py
  app.py
  train_model.py
  requirements.txt
  README.md
  LinkGithubVideo.txt
  data/
    alunos_evasao_sintetico.csv
    alunos_cadastrados.json
  metrics/
    model_metrics.json
  models/
    modelo_evasao.pkl
```

## Como Executar

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Treinar o modelo:

```bash
python train_model.py
```

Iniciar a API:

```bash
python api.py
```

Executar o painel:

```bash
streamlit run app.py
```

Apos iniciar o painel, acessar:

```text
http://localhost:8501
```

## Endpoints da API

### GET `/health`

Verifica se a API esta disponivel.

### GET `/model-info`

Retorna informacoes do modelo, variaveis utilizadas e metricas de treinamento.

### POST `/predict`

Realiza a predicao individual de um aluno.

Exemplo de entrada:

```json
{
  "horas_estudadas": 8,
  "exercicios_concluidos": 2,
  "media_notas": 3.9,
  "dias_inativos": 35
}
```

Exemplo de saida:

```json
{
  "classe": 1,
  "risco": "alto",
  "probabilidade_evasao": 83.33,
  "recomendacao": "Acionar tutor, oferecer monitoria e enviar mensagem personalizada ainda hoje."
}
```

### POST `/predict-batch`

Recebe uma lista de alunos e retorna as predicoes em lote.

### GET `/students`

Lista os alunos cadastrados.

### POST `/students`

Cadastra um aluno e salva os dados em `data/alunos_cadastrados.json`.

Exemplo de entrada:

```json
{
  "nome": "Joao Silva",
  "horas_estudadas": 15,
  "exercicios_concluidos": 5,
  "media_notas": 5.5,
  "dias_inativos": 18
}
```

### DELETE `/students/{id}`

Remove um aluno cadastrado.

### DELETE `/students`

Remove todos os alunos cadastrados.

### POST `/students/predict`

Processa todos os alunos cadastrados e retorna o risco de evasao de cada um.

## Fluxo de Uso

1. Treinar o modelo com `train_model.py`.
2. Iniciar a API com `api.py`.
3. Abrir o painel Streamlit.
4. Cadastrar alunos com seus indicadores academicos.
5. Visualizar a turma cadastrada.
6. Processar a turma com o modelo de IA.
7. Analisar risco, probabilidade e recomendacao para cada aluno.

## Resultado

A aplicacao permite que uma turma seja cadastrada e analisada por um modelo de IA. O sistema retorna uma classificacao de risco para cada aluno, permitindo identificar casos prioritarios para acompanhamento.
