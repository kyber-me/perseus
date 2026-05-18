import numpy as np
import hashlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from encoder.encoder import SparseEncoder
from neural_nets.hopfield_net import HopfieldNet

def string_to_dense_embedding(text: str, dim: int = 384) -> np.ndarray:
    """
    Simula um modelo de linguagem determinístico gerando um embedding denso
    único e estável para cada frase baseando-se no hash do texto.
    """
    seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(dim).astype(np.float32)
    return v / np.linalg.norm(v)

def calculate_hamming_similarity(p1: np.ndarray, p2: np.ndarray) -> float:
    """
    Calcula a similaridade (0.0 a 1.0) entre dois volumes 3D.
    """
    p1_flat = p1.ravel()
    p2_flat = p2.ravel()
    
    # Normaliza as representações para binário caso existam misturas com bipolar
    b1 = np.where(p1_flat <= 0, 0, 1)
    b2 = np.where(p2_flat <= 0, 0, 1)
    
    matches = np.sum(b1 == b2)
    return float(matches / len(b1))

def run_experiment():
    print("="*65)
    print("🧠 EXPERIMENTO IN-VITRO: RECUPERAÇÃO SEMÂNTICA (HOPFIELD 3D)")
    print("="*65)

    # 1. Configurando o Ambiente
    h_dim = (16, 16, 16)
    input_dim = 384
    # Hopfield clássico requer padrões balanceados (alta entropia) ~ 50% ativos
    encoder = SparseEncoder(input_dim=input_dim, grid_shape=h_dim, density=0.50, seed=123)
    hopnet = HopfieldNet(h_dim)

    # 2. Definindo Fatos Semânticos
    facts = [
        "A rápida raposa marrom salta sobre o cão preguiçoso.",
        "A mecânica quântica descreve o universo em escalas subatômicas.",
        "Uma receita de bolo de chocolate exige farinha, açúcar e cacau."
    ]

    print("\n[+] GERANDO VOLUMES DE MEMÓRIA (SPARSE ENCODER)...")
    memory_volumes = []
    for fact in facts:
        emb = string_to_dense_embedding(fact, input_dim)
        volume = encoder.encode_seed(emb) # Retorna volume 3D {0, 1}
        memory_volumes.append(volume)
        print(f"    - Fato: '{fact[:45]}...' -> Volume (Ativos: {np.sum(volume)}/4096)")

    # 3. Consolidação (Hebbian Learning)
    print("\n[+] CONSOLIDANDO MEMÓRIAS (HEBBIAN LEARNING)...")
    for vol in memory_volumes:
        hopnet.learn(vol)
    print("    - Todas as memórias gravadas na matriz de pesos cumulativa.")

    # 4. Criando um gatilho de evocação corrompido (ruído)
    print("\n[+] PREPARANDO GATILHO DE EVOCAÇÃO (RUÍDO INJETADO)...")
    target_idx = 1 # Vamos tentar resgatar o fato quântico
    target_volume = memory_volumes[target_idx]
    
    # Corrompendo 20% do volume da memória alvo
    noise_level = 0.20
    N = int(np.prod(h_dim))
    num_flips = int(N * noise_level)
    
    noisy_cue = target_volume.copy().ravel()
    flip_indices = np.random.choice(N, size=num_flips, replace=False)
    
    # Flip bits (0->1, 1->0)
    for idx in flip_indices:
        noisy_cue[idx] = 1 if noisy_cue[idx] == 0 else 0
        
    noisy_cue = noisy_cue.reshape(h_dim)
    
    initial_similarity = calculate_hamming_similarity(noisy_cue, target_volume)
    print(f"    - Alvo Original: '{facts[target_idx]}'")
    print(f"    - Ruído Injetado: {noise_level*100}% ({num_flips} bits foram invertidos aleatoriamente)")
    print(f"    - Similaridade Inicial (Gatilho vs Alvo): {initial_similarity:.2%}")

    # 5. Inferência (Dinâmica de Atratores) - Teste A
    print("\n[+] EVOCANDO MEMÓRIA (INFERÊNCIA DA FRASE CORROMPIDA)...")
    recovered_volume = hopnet.infer(noisy_cue, steps=10, mode='asynchronous')

    # 6. Avaliando Resultados do Teste A
    print("\n[+] RESULTADOS (TESTE A - MEMÓRIA CORROMPIDA):")
    for i, original_vol in enumerate(memory_volumes):
        sim = calculate_hamming_similarity(recovered_volume, original_vol)
        marker = " <=== RECUPERAÇÃO PERFEITA!" if sim == 1.0 else (" <=== ATRAÍDO!" if sim > 0.90 else "")
        print(f"    - Similaridade com o Fato {i+1}: {sim:.2%}{marker}")

    # =========================================================
    # TESTE B: FRASE COMPLETAMENTE INÉDITA
    # =========================================================
    print("\n" + "="*65)
    print("🧪 TESTE B: INJEÇÃO DE CONCEITO ALIENÍGENA (NÃO APRENDIDO)")
    
    alien_fact = "A inteligência artificial é baseada em redes neurais profundas."
    emb_alien = string_to_dense_embedding(alien_fact, input_dim)
    alien_volume = encoder.encode_seed(emb_alien)
    
    print(f"    - Injetando frase inédita: '{alien_fact}'")
    
    alien_recovered = hopnet.infer(alien_volume, steps=10, mode='asynchronous')
    
    print("\n[+] RESULTADOS (TESTE B - FRASE ALIENÍGENA):")
    for i, original_vol in enumerate(memory_volumes):
        sim = calculate_hamming_similarity(alien_recovered, original_vol)
        marker = " <=== FALSO POSITIVO (ALUCINAÇÃO)!" if sim > 0.90 else ""
        print(f"    - Similaridade com o Fato {i+1}: {sim:.2%}{marker}")
    
    alien_self_sim = calculate_hamming_similarity(alien_recovered, alien_volume)
    print(f"    - Similaridade da saída com a própria entrada inédita: {alien_self_sim:.2%}")

if __name__ == "__main__":
    run_experiment()
