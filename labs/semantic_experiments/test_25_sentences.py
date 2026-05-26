import os
import sys
import numpy as np

# Adicionar a pasta src ao path para poder importar neocortex/encoder etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from embedding.semantic_embedder import SemanticEmbedder
from encoder.encoder import SparseEncoder

# -------------------------------------------------------------------------
# O DATASET BENCHMARK DE 25 FRASES (5 Temas × 5 Frases: 4 Bases + 1 Query)
# -------------------------------------------------------------------------
BENCHMARK_DATASET = {
    "Astrofísica e Buracos Negros": [
        "Buracos negros supermassivos curvam o espaço-tempo no centro de galáxias distantes.",
        "A luz não consegue escapar da gravidade extrema após cruzar o horizonte de eventos.",
        "Astrônomos usam telescópios de rádio para capturar a sombra de um horizonte de singularidade.",
        "A radiação Hawking descreve a evaporação térmica lenta de buracos negros no espaço profundo.",
        "Colossais distorções gravitacionais no núcleo galáctico impedem a fuga da radiação luminosa."  # Query
    ],
    "Culinária e Panificação": [
        "Uma receita tradicional de pão caseiro exige fermentação lenta e farinha de trigo.",
        "O chefe de cozinha prepara um bolo de chocolate úmido com cacau puro.",
        "Assar pães em forno aquecido a lenha cria uma casca dourada e crocante.",
        "O preparo de massas frescas artesanais requer ovos caipiras e sova vigorosa.",
        "A panificação artesanal envolve misturar ingredientes simples e fermentar a massa sob calor controlado."  # Query
    ],
    "Mecânica Quântica": [
        "A dualidade onda-partícula mostra que elétrons se comportam como ondas sob certas condições.",
        "O emaranhamento quântico conecta estados de partículas instantaneamente a distâncias infinitas.",
        "O princípio da incerteza de Heisenberg impede determinar a posição e momento de forma precisa.",
        "A superposição permite que um qubit represente múltiplos estados lógicos simultaneamente.",
        "Partículas subatômicas existem em múltiplos estados até que uma medição colapse sua função de onda."  # Query
    ],
    "Inteligência Artificial e Deep Learning": [
        "Redes neurais profundas ajustam seus pesos sinápticos através do algoritmo de retropropagação.",
        "Modelos de linguagem de larga escala utilizam a arquitetura transformer com atenção multidirecional.",
        "O aprendizado por reforço treina agentes autônomos maximizando recompensas cumulativas no ambiente.",
        "A regularização por dropout previne o sobreajuste desligando neurônios aleatoriamente no treino.",
        "Algoritmos de deep learning aprendem representações hierárquicas a partir de grandes volumes de dados."  # Query
    ],
    "Comportamento de Gatos Domésticos": [
        "Gatos domésticos ronronam para expressar contentamento ou para aliviar o estresse.",
        "O comportamento caçador de felinos é ativado por estímulos visuais rápidos em movimento.",
        "Felinos limpam sua pelagem diariamente lambendo-se para remover pelos mortos.",
        "Um gato demonstra afeto esfregando suas glândulas odoríferas nas pernas do tutor.",
        "Animais felinos domésticos passam grande parte do dia dormindo em locais altos e aquecidos."  # Query
    ]
}

def main():
    print("="*75)
    print("🧪 LAB: GERAÇÃO DE EMBEDDINGS E REPRESENTAÇÃO 2D (GRID 27x27)")
    print("="*75)

    # 1. Inicialização dos Módulos Perseus na escala 27x27 (729 células)
    grid_shape = (27, 27)
    input_dim = 768  # Mantendo 768 dimensões de informação pura
    density = 0.15   # 15% de ativação ativa (SDR)
    
    print(f"[*] Inicializando SemanticEmbedder (Denso {input_dim}D)...")
    embedder = SemanticEmbedder(input_dim=input_dim)
    
    print(f"[*] Inicializando SparseEncoder (Esparso {grid_shape[0]}x{grid_shape[1]}, densidade {density*100}%)...")
    encoder = SparseEncoder(
        input_dim=input_dim,
        grid_shape=grid_shape,
        density=density,
        seed=42
    )

    print("\n[+] PROCESSANDO AS 25 FRASES DO DATASET:")
    all_processed = []

    for theme, sentences in BENCHMARK_DATASET.items():
        print(f"\n🔹 Tema: {theme}")
        for idx, sentence in enumerate(sentences):
            # Identifica se é frase base (0 a 3) ou query (4)
            is_query = (idx == 4)
            role = "Query" if is_query else f"Base {idx+1}"
            
            # A. Gerar o embedding contínuo denso 768D
            embedding = embedder.embed(sentence)
            
            # B. Projetar para o grid esparso binário 27x27 (729 células)
            grid_2d = encoder.encode_seed(embedding)
            
            # C. Métricas de integridade
            norm = np.linalg.norm(embedding)
            active_count = np.sum(grid_2d == 1)
            total_cells = grid_2d.size
            real_density = active_count / total_cells
            
            print(f"  [{role}] '{sentence[:45]}...'")
            print(f"     -> Embedding 768D: Norma L2 = {norm:.4f}")
            print(f"     -> Grid 27x27    : {active_count}/{total_cells} células ativas (Densidade real: {real_density:.2%})")
            
            all_processed.append({
                "theme": theme,
                "role": role,
                "text": sentence,
                "embedding": embedding,
                "grid_2d": grid_2d
            })

    # D. Exibir uma amostra visual do Grid 2D de um evento no console (ASCII)
    print("\n" + "="*75)
    print("🎨 AMOSTRA VISUAL EM CONSOLE (ASCII) — GRID 27x27 (Tema 1, Base 1)")
    print("="*75)
    
    sample_grid = all_processed[0]["grid_2d"]
    for row in range(sample_grid.shape[0]):
        row_str = ""
        for col in range(sample_grid.shape[1]):
            # Representação estética: ■ para células ativas (1), ∙ para inativas (0)
            row_str += "■ " if sample_grid[row, col] == 1 else "∙ "
        print(row_str)
        
    print("\n[+] Geração de representações 2D concluída com total integridade matemática!")
    print("="*75)

if __name__ == "__main__":
    main()
