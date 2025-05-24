import streamlit as st
from db import conectar, criar_tabelas

criar_tabelas()

st.title("Gestão de Atribuição de Disciplinas")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Professor", "Cadastrar Curso", "Cadastrar Disciplina", "Atribuir", "Carga Horária"])

if menu == "Cadastrar Professor":
    nome = st.text_input("Nome")
    titulacao = st.selectbox("Titulação", ["Licenciado", "Mestre", "Doutor"])
    if st.button("Salvar"):
        carga_max = 28 if titulacao in ["Licenciado", "Mestre"] else 24
        conn = conectar()
        conn.execute("INSERT INTO professores (nome, titulacao, carga_max) VALUES (?, ?, ?)", (nome, titulacao, carga_max))
        conn.commit()
        conn.close()
        st.success(f"Professor {nome} cadastrado.")
