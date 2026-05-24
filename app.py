import pandas as pd
import requests
import streamlit as st


API_URL = "http://localhost:8000"
RISK_ORDER = {"alto": 0, "medio": 1, "baixo": 2}


st.set_page_config(page_title="OracleLearn IA - Evasao", page_icon="IA", layout="wide")

st.title("OracleLearn IA - Predicao de Evasao")
st.write(
    "Painel demonstrativo para validar o modelo de IA da Sprint 4. "
    "O painel consome uma API REST em Python responsavel pelas predicoes do modelo."
)


def request_json(method, path, **kwargs):
    response = requests.request(method, f"{API_URL}{path}", timeout=10, **kwargs)
    if response.ok:
        return response.json()

    try:
        detail = response.json().get("error", response.text)
    except ValueError:
        detail = response.text
    raise RuntimeError(detail)


@st.cache_data(ttl=30)
def get_model_info():
    return request_json("GET", "/model-info")


def get_students():
    return request_json("GET", "/students")["alunos"]


def create_student(payload):
    return request_json("POST", "/students", json=payload)


def delete_student(student_id):
    return request_json("DELETE", f"/students/{student_id}")


def clear_students():
    return request_json("DELETE", "/students")


def predict(payload):
    return request_json("POST", "/predict", json=payload)


def predict_registered_students():
    return request_json("POST", "/students/predict")["resultados"]


def student_table(alunos):
    return pd.DataFrame(
        [
            {
                "Aluno": aluno["nome"],
                "Horas estudadas": aluno["horas_estudadas"],
                "Exercicios": aluno["exercicios_concluidos"],
                "Media": aluno["media_notas"],
                "Dias inativo": aluno["dias_inativos"],
            }
            for aluno in alunos
        ]
    )


def result_table(resultados):
    rows = []
    for item in resultados:
        rows.append(
            {
                "Aluno": item["nome"],
                "Risco": item["risco"],
                "Probabilidade": f"{item['probabilidade_evasao']:.1f}%",
                "Recomendacao": item["recomendacao"],
                "Ordem": RISK_ORDER.get(item["risco"], 9),
            }
        )

    table = pd.DataFrame(rows).sort_values(["Ordem", "Aluno"])
    return table.drop(columns=["Ordem"])


try:
    info = get_model_info()
    alunos = get_students()
except Exception as error:
    st.error(f"API de IA indisponivel. Rode `python api.py` em outro terminal. Detalhe: {error}")
    st.stop()

metrics = info.get("metricas") or {}

col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Modelo", info["modelo"])
col_b.metric("Acuracia", f"{metrics.get('accuracy', 0) * 100:.1f}%")
col_c.metric("Alunos cadastrados", len(alunos))
col_d.metric("Features", len(info["features"]))

st.divider()

cadastro_col, turma_col = st.columns([1, 2])

with cadastro_col:
    st.subheader("Cadastro de aluno")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome do aluno")
        horas_estudadas = st.slider("Horas estudadas", 0, 120, 20, key="cad_horas")
        exercicios_concluidos = st.slider("Exercicios concluidos", 0, 80, 10, key="cad_exercicios")
        media_notas = st.slider("Media de notas", 0.0, 10.0, 7.5, 0.1, key="cad_media")
        dias_inativos = st.slider("Dias consecutivos inativo", 0, 90, 5, key="cad_dias")
        cadastrar_btn = st.form_submit_button("Salvar aluno")

    if cadastrar_btn:
        try:
            create_student(
                {
                    "nome": nome,
                    "horas_estudadas": horas_estudadas,
                    "exercicios_concluidos": exercicios_concluidos,
                    "media_notas": media_notas,
                    "dias_inativos": dias_inativos,
                }
            )
            st.success("Aluno cadastrado.")
            st.rerun()
        except Exception as error:
            st.error(str(error))

    turma_exemplo = [
        {
            "nome": "Joao Silva",
            "horas_estudadas": 15,
            "exercicios_concluidos": 5,
            "media_notas": 5.5,
            "dias_inativos": 18,
        },
        {
            "nome": "Maria Souza",
            "horas_estudadas": 80,
            "exercicios_concluidos": 45,
            "media_notas": 9.2,
            "dias_inativos": 1,
        },
        {
            "nome": "Carlos Eduardo",
            "horas_estudadas": 6,
            "exercicios_concluidos": 2,
            "media_notas": 3.8,
            "dias_inativos": 35,
        },
    ]

    if st.button("Carregar turma exemplo"):
        for aluno in turma_exemplo:
            create_student(aluno)
        st.success("Turma exemplo cadastrada.")
        st.rerun()

with turma_col:
    st.subheader("Turma cadastrada")
    if alunos:
        st.dataframe(student_table(alunos), use_container_width=True, hide_index=True)

        action_col_a, action_col_b = st.columns([2, 1])
        with action_col_a:
            aluno_selecionado = st.selectbox(
                "Aluno para remover",
                alunos,
                format_func=lambda aluno: aluno["nome"],
            )
        with action_col_b:
            st.write("")
            st.write("")
            if st.button("Remover"):
                delete_student(aluno_selecionado["id"])
                st.rerun()

        if st.button("Limpar turma"):
            clear_students()
            st.rerun()
    else:
        st.info("Cadastre alunos ou carregue a turma exemplo para processar o lote.")

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Analise individual")
    with st.form("form_analise"):
        horas_estudadas = st.slider("Horas estudadas", 0, 120, 20, key="ana_horas")
        exercicios_concluidos = st.slider("Exercicios concluidos", 0, 80, 10, key="ana_exercicios")
        media_notas = st.slider("Media de notas", 0.0, 10.0, 7.5, 0.1, key="ana_media")
        dias_inativos = st.slider("Dias consecutivos inativo", 0, 90, 5, key="ana_dias")
        analisar_btn = st.form_submit_button("Consultar IA")

with col2:
    st.subheader("Resultado individual")
    if analisar_btn:
        resultado = predict(
            {
                "horas_estudadas": horas_estudadas,
                "exercicios_concluidos": exercicios_concluidos,
                "media_notas": media_notas,
                "dias_inativos": dias_inativos,
            }
        )

        risco = resultado["risco"]
        prob = resultado["probabilidade_evasao"]
        if risco == "alto":
            st.error(f"Risco alto de evasao: {prob:.1f}%")
        elif risco == "medio":
            st.warning(f"Risco medio de evasao: {prob:.1f}%")
        else:
            st.success(f"Risco baixo de evasao: {prob:.1f}%")

        st.write(resultado["recomendacao"])
    else:
        st.info("Preencha os dados e clique em Consultar IA.")

st.divider()
st.subheader("Analise em lote da turma")

if not alunos:
    st.info("Nenhum aluno cadastrado para analisar em lote.")
elif st.button("Processar turma cadastrada"):
    resultados = predict_registered_students()
    tabela_resultados = result_table(resultados)
    st.dataframe(tabela_resultados, use_container_width=True, hide_index=True)

    total_alto = sum(1 for item in resultados if item["risco"] == "alto")
    total_medio = sum(1 for item in resultados if item["risco"] == "medio")
    total_baixo = sum(1 for item in resultados if item["risco"] == "baixo")
    risco_col_a, risco_col_b, risco_col_c = st.columns(3)
    risco_col_a.metric("Alto risco", total_alto)
    risco_col_b.metric("Medio risco", total_medio)
    risco_col_c.metric("Baixo risco", total_baixo)

st.divider()
st.subheader("Importancia das variaveis")
feature_importance = metrics.get("feature_importance") or {}
if feature_importance:
    st.bar_chart(pd.DataFrame.from_dict(feature_importance, orient="index", columns=["importancia"]))
