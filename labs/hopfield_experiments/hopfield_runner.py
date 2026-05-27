import numpy as np
import json
import os
from datetime import datetime
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from encoder.encoder import SparseEncoder
from neural_nets.hopfield_net import HopfieldNet

class HopfieldExperimentSkill:
    """
    Skill encapsulada para rodar simulações In-Vitro na HopfieldNet.
    Gera automaticamente logs detalhados em JSON para cada experimento iterativo.
    """
    def __init__(self, h_dim=(16, 16, 16), input_dim=768, density=0.50, seed=123):
        self.h_dim = h_dim
        self.input_dim = input_dim
        self.encoder = SparseEncoder(input_dim=input_dim, grid_shape=h_dim, density=density, seed=seed)
        
        from embedding.semantic_embedder import SemanticEmbedder
        self.embedder = SemanticEmbedder(input_dim)
        
        self.hopnet = HopfieldNet(h_dim)
        self.memory_volumes = []
        self.facts = []


    def _calculate_hamming_similarity(self, p1: np.ndarray, p2: np.ndarray) -> float:
        b1 = np.where(p1.ravel() <= 0, 0, 1)
        b2 = np.where(p2.ravel() <= 0, 0, 1)
        
        overlap = np.sum((b1 == 1) & (b2 == 1))
        active = np.sum(b1)
        if active == 0: return 0.0
        
        return float(overlap / active)

    def run_semantic_retrieval(
        self, 
        experiment_name: str, 
        description: str, 
        learning_facts: list[str], 
        test_fact: str, 
        noise_level: float = 0.0
    ) -> str:
        
        # 1. Aprender as Memórias Base
        self.facts = learning_facts
        self.memory_volumes = []
        for fact in self.facts:
            emb = self.embedder.embed(fact)
            vol = self.encoder.encode_seed(emb)
            self.memory_volumes.append(vol)
            self.hopnet.learn(vol)

        # 2. Gerar Gatilho (Cue) de Teste
        emb_test = self.embedder.embed(test_fact)
        test_volume = self.encoder.encode_seed(emb_test)
        original_test_volume = test_volume.copy()
        
        # Injetar Ruído (se requisitado)
        if noise_level > 0:
            N = int(np.prod(self.h_dim))
            num_flips = int(N * noise_level)
            noisy_cue = test_volume.ravel()
            flip_indices = np.random.choice(N, size=num_flips, replace=False)
            for idx in flip_indices:
                noisy_cue[idx] = 1 if noisy_cue[idx] == 0 else 0
            test_volume = noisy_cue.reshape(self.h_dim)

        # 3. Rodar Dinâmica do Atrator (Inferência)
        recovered_volume = self.hopnet.infer(test_volume, steps=10, mode='asynchronous')

        # 4. Avaliar Similaridades com Memórias
        results = []
        for i, original_vol in enumerate(self.memory_volumes):
            sim = self._calculate_hamming_similarity(recovered_volume, original_vol)
            
            # Análise qualitativa baseada na força de recuperação
            status = "PERFECT_RECOVERY" if sim == 1.0 else (
                "ATTRACTED" if sim > 0.9 else (
                    "SPURIOUS_BLEND" if sim > 0.6 else "NOISE"
                )
            )
            
            results.append({
                "fact_id": i + 1,
                "fact_text": self.facts[i],
                "similarity_percentage": round(sim * 100, 2),
                "status": status
            })

        # Similaridade final do padrão recuperado com o próprio padrão que iniciou o teste
        self_sim = self._calculate_hamming_similarity(recovered_volume, original_test_volume)

        # 5. Construir Relatório JSON
        report = {
            "experiment_name": experiment_name,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "parameters": {
                "grid_shape": self.h_dim,
                "entropy_density": self.encoder.density,
                "noise_injected_percentage": noise_level * 100
            },
            "learning_phase": {
                "facts_learned": len(self.facts)
            },
            "test_phase": {
                "test_fact": test_fact,
                "is_novel_concept": test_fact not in self.facts,
                "final_similarity_to_itself_percentage": round(self_sim * 100, 2),
                "similarities_to_learned_facts": results
            }
        }

        # 6. Salvar em Disco
        output_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(output_dir, exist_ok=True)
        
        clean_name = experiment_name.replace(' ', '_').lower()
        filename = f"{clean_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        # Geração dinâmica do report.md conforme solicitado pelo usuário
        report_md_filename = filename.replace('.json', '.md')
        report_md_filepath = os.path.join(output_dir, report_md_filename)
        
        target_results = ""
        for res in results:
            marker = " <=== RECUPERAÇÃO PERFEITA!" if res["similarity_percentage"] == 100.0 else (
                " <=== FALSO POSITIVO (ALUCINAÇÃO)!" if res["similarity_percentage"] > 90.0 and test_fact not in self.facts else ""
            )
            target_results += f"    - Similaridade com o Fato {res['fact_id']}: {res['similarity_percentage']:.2f}% ({res['status']}){marker}\n"
            
        report_md_content = f"""# Relatório Experimental: Recuperação Semântica (Hopfield 3D)
<!-- Relatório de Validação da Unidade de Memória Associativa de CA3 -->

## 1. Objetivo do Experimento
Validar a capacidade da **Unidade CA3 Hipocampal**, modelada por uma **Rede de Hopfield Recorrente 3D** (escala {self.h_dim[0]}x{self.h_dim[1]}x{self.h_dim[2]} correspondendo a $N={int(np.prod(self.h_dim))}$ neurônios virtuais), de realizar:
1.  **Pattern Completion**: Recuperar com precisão um engrama estável original a partir de um gatilho de evocação corrompido com ruído severo.
2.  **Rejeição e Spurious States**: Avaliar o comportamento dinâmico da rede quando exposta a um estímulo inédito (conceito alienígena não aprendido).

---

## 2. Configurações e Massa de Dados
*   **Grid de Resolução**: Volume 3D de {self.h_dim[0]}x{self.h_dim[1]}x{self.h_dim[2]} ({int(np.prod(self.h_dim))} neurônios).
*   **Projeção Esparsa**: `SparseEncoder` com densidade {self.encoder.density:.2f} (ativação de {int(np.prod(self.h_dim)*self.encoder.density)} neurônios).
*   **Nome do Experimento**: {experiment_name}
*   **Descrição**: {description}

---

## 3. Resultados Obtidos (Teste: '{test_fact}')
*   **Ruído Injetado**: {noise_level * 100:.1f}%
*   **É Conceito Alienígena (Inédito)?**: {'SIM' if test_fact not in self.facts else 'NÃO'}
*   **Similaridade de Saída com a Própria Entrada Inédita**: {self_sim * 100:.2f}%

### Similaridades Finais por Fato Consolidador:
{target_results}
"""
        with open(report_md_filepath, 'w', encoding='utf-8') as f:
            f.write(report_md_content)
            
        return filepath

# Teste embutido para validar a Skill
if __name__ == "__main__":
    skill = HopfieldExperimentSkill()
    
    # Executando o experimento do Alien Concept (Teste B anterior)
    path = skill.run_semantic_retrieval(
        experiment_name="Amnesia_Confabulatoria_Alien",
        description="Testa a capacidade da rede de rejeitar frases totalmente inéditas. Avalia se ela colapsa em um Falso Positivo ou em um Estado Espúrio Misto.",
        learning_facts=[
            "A rápida raposa marrom salta sobre o cão preguiçoso.",
            "A mecânica quântica descreve o universo em escalas subatômicas.",
            "Uma receita de bolo de chocolate exige farinha, açúcar e cacau."
        ],
        test_fact="A inteligência artificial é baseada em redes neurais profundas.",
        noise_level=0.0
    )
    print(f"[!] Relatório de Experimento exportado para: {path}")
