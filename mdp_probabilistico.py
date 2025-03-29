import streamlit as st
import numpy as np
import time
import random

# Configuração da página
st.title("Simulador de Sorteio de Caminhos")

# Inicialização do estado
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.estados = ['s0', 's1', 's2', 's3', 's4','s5', 's6', 's7', 's8', 's9', 's10']
    st.session_state.estado_atual = 's0'
    st.session_state.caminho = ['s0']
    st.session_state.rodando = False
    st.session_state.sorteando = False
    st.session_state.resultado_sorteio = None
    st.session_state.numero_sorteado = None
    
    st.session_state.probabilidades = {
        's0': {'s1': 0.3, 's2': 0.2, 's3': 0.4, 's4': 0.1},
        's1': {'s5': 0.3, 's6': 0.7},
        's2': {'s7': 0.8, 's8': 0.2},
        's3': {'s9': 0.1, 's10': 0.9},
        's4': {'s1': 0.6, 's2': 0.4},
        's5': {'s3': 0.7, 's4': 0.3},
        's6': {'s5': 0.5, 's6': 0.5},
        's7': {'s7': 0.9, 's8': 0.1},
        's8': {'s9': 0.2, 's10': 0.8},
        's9': {'s1': 0.6, 's2': 0.4},
        's10': {'s3': 0.7, 's4': 0.3},
    }

# Função para escolher o próximo estado baseado no número sorteado
def proximo_estado():
    estado = st.session_state.estado_atual
    probabilidades = st.session_state.probabilidades[estado]
    estados = list(probabilidades.keys())
    probs = list(probabilidades.values())
    
    # Gerar número aleatório entre 0 e 1
    numero_sorteado = random.uniform(0, 1)
    st.session_state.numero_sorteado = numero_sorteado
    
    # Encontrar a probabilidade mais próxima do número sorteado
    melhor_estado = estados[0]
    menor_diferenca = abs(probs[0] - numero_sorteado)
    
    for i in range(1, len(estados)):
        diferenca = abs(probs[i] - numero_sorteado)
        if diferenca < menor_diferenca:
            melhor_estado = estados[i]
            menor_diferenca = diferenca
    
    st.session_state.estado_atual = melhor_estado
    st.session_state.caminho.append(melhor_estado)
    st.session_state.resultado_sorteio = melhor_estado

# Função para iniciar/parar a simulação
def toggle_simulacao():
    st.session_state.rodando = not st.session_state.rodando

# Função para resetar
def resetar():
    st.session_state.estado_atual = 's0'
    st.session_state.caminho = ['s0']
    st.session_state.rodando = False
    st.session_state.resultado_sorteio = None
    st.session_state.numero_sorteado = None

# Interface simples
col1, col2 = st.columns([1, 1])

with col1:
    if st.button('Sortear Caminhos'):
        toggle_simulacao()

with col2:
    if st.button('Voltar ao inicio'):
        resetar()

# Mostrar estado atual
st.header(f"Estado Atual: {st.session_state.estado_atual}")

# Mostrar as probabilidades do estado atual
st.subheader("Probabilidades a partir do estado atual:")
estado = st.session_state.estado_atual
probabilidades = st.session_state.probabilidades[estado]

# Criar uma tabela de probabilidades
prob_data = []
for destino, prob in probabilidades.items():
    prob_data.append({"Destino": destino, "Probabilidade": f"{prob*100:.1f}%"})

st.table(prob_data)

# Realizar sorteio
if st.session_state.rodando:
    time.sleep(1)
    proximo_estado()

# Mostrar resultado do sorteio
st.subheader("Resultado do Sorteio:")
if st.session_state.numero_sorteado is not None:
    st.write(f"Número sorteado: {st.session_state.numero_sorteado:.4f}")
    st.write(f"Estado escolhido: {st.session_state.resultado_sorteio}")

# Mostrar o caminho percorrido
st.subheader("Caminho Percorrido:")
st.write(" → ".join(st.session_state.caminho))
