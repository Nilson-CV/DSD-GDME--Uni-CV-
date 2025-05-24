import streamlit as st
import pandas as pd

st.title("Gestão de Atribuições de Disciplinas")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Professor", "Cadastrar Curso", "Cadastrar Disciplina", "Atribuir Disciplina", "Carga Horária"])

if menu == "Cadastrar Professor":
    nome = st.text_input("Nome")
    titulacao = st.selectbox("Titulação", ["Licenciado", "Mestre", "Doutor"])
    
    if st.button("Salvar"):
        carga_max = 28 if titulacao in ["Licenciado", "Mestre"] else 24
        # salvar em csv ou dataframe
        st.success(f"Professor {nome} cadastrado com limite de {carga_max} horas.")

# Os demais menus seguem lógica similar
