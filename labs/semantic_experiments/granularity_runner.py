import os
import json
import sys
import numpy as np


# Ajusta path para importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from embedding.semantic_embedder import SemanticEmbedder
from encoder.encoder import SparseEncoder

# =====================================================================
# DADOS SINTÉTICOS: 4 Níveis de Profundidade Semântica (Intra-Camada)
# =====================================================================

# Nível 1: Eventos Macro (Episódico/Contextual)
DEPTH_1_EVENTS = [
    "The small black cat sleeps peacefully on the living room sofa during the storm.",
    "The quick brown fox jumps swiftly over the lazy dog in the open field.",
    "A brilliant scientist studies the supermassive black hole at the center of the Andromeda galaxy.",
    "Quantum mechanics mathematically describes the universe at extremely small subatomic scales."
]

# Nível 2: Sub-eventos / Sintagmas Relacionais (Ação/Contexto reduzido)
DEPTH_2_SUBEVENTS = [
    "sleeps peacefully on the living room sofa",
    "jumps swiftly over the lazy dog",
    "studies the supermassive black hole at the center",
    "mathematically describes the universe at subatomic scales"
]

# Nível 3: Entidades Compostas / Fragmentos Estáticos
DEPTH_3_ENTITIES = [
    "the small black cat",
    "the quick brown fox",
    "a brilliant scientist",
    "quantum mechanics"
]

# Nível 4: Conceitos Atômicos (Alta especificidade)
DEPTH_4_CONCEPTS = [
    "cat",
    "fox",
    "scientist",
    "quantum",
    "black hole",
    "universe",
    "storm"
]

SYNTHETIC_DATASETS = {
    "depth_1_macro_events": DEPTH_1_EVENTS,
    "depth_2_sub_events": DEPTH_2_SUBEVENTS,
    "depth_3_entities": DEPTH_3_ENTITIES,
    "depth_4_atomic_concepts": DEPTH_4_CONCEPTS
}

# =====================================================================
# MOTOR DE EXPERIMENTAÇÃO
# =====================================================================

class GranularityExperimentRunner:
    """
    Laboratório Semântico Intra-Camada (Grid 27x27).
    Avalia a similaridade (Cosseno e SDR Overlap) entre sintagmas pertencentes ao mesmo nível de profundidade.
    """
    
    def __init__(self, grid_shape=(27, 27), input_dim=768, density=0.15, seed=42):
        self.grid_shape = grid_shape
        self.input_dim = input_dim
        self.density = density
        
        print(f"[*] Inicializando SemanticEmbedder (Denso {input_dim}D)...")
        self.embedder = SemanticEmbedder(input_dim=input_dim)
        
        print(f"[*] Inicializando SparseEncoder (Esparso {grid_shape[0]}x{grid_shape[1]}, densidade {density*100}%)...")
        self.encoder = SparseEncoder(
            input_dim=input_dim, 
            grid_shape=self.grid_shape, 
            density=self.density, 
            seed=seed
        )

    def _generate_heuristic_interpretation(self, dataset_name: str, avg_cosine: float, avg_hamming: float) -> str:
        """
        Gera um texto interpretativo heurístico com base no nome do conjunto e nos valores médios computados.
        """
        if "depth_1" in dataset_name:
            if avg_hamming > 0.4:
                return f"Os eventos macro apresentam uma sobreposição SDR surpreendentemente alta ({avg_hamming:.2%}), indicando que a malha de 27x27 consegue aglutinar o amplo contexto semântico sem perder o ruído estrutural."
            else:
                return f"Os eventos macro são suficientemente distintos para gerar matrizes esparsas únicas (overlap médio de {avg_hamming:.2%}). O espaço semântico global dos eventos é mapeado com forte dispersão espacial, validando a capacidade de isolamento episódico."
        elif "depth_4" in dataset_name:
            if avg_hamming < 0.2:
                return f"Os conceitos atômicos geraram sobreposição SDR extremamente baixa ({avg_hamming:.2%}), demonstrando a severa seletividade da projeção ortogonal 27x27 para separar núcleos semânticos isolados."
            else:
                return f"Os conceitos atômicos apresentam uma sobreposição considerável ({avg_hamming:.2%}), sugerindo que a proximidade latente desses termos no espaço denso contínuo forçou a ativação de sub-regiões similares no espaço esparso."
        else:
            return f"Em níveis intermediários de abstração semântica (sub-eventos e entidades), a similaridade contínua (Cosseno) de {avg_cosine:.2%} resulta em uma sobreposição de memória esparsa (SDR) de {avg_hamming:.2%}. O sistema exibe um comportamento balanceado entre generalização e distinção."

    def run_all_depths(self):
        """
        Itera sobre todos os datasets sintéticos, calcula as similaridades intra-conjunto,
        e salva um relatório JSON detalhado para cada nível de profundidade.
        """
        import datetime
        
        # Formatação Amigável da Data para a Pasta
        pt_months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        now = datetime.datetime.now()
        readable_ts = f"{now.day} de {pt_months[now.month-1]} de {now.year}, {now.strftime('%H:%M:%S')}"
        folder_name = f"Experimento_{now.day}_{pt_months[now.month-1]}_{now.year}_{now.strftime('%Hh%Mm%Ss')}"
        
        experiment_dir = os.path.join(os.path.dirname(__file__), "results", folder_name)
        os.makedirs(experiment_dir, exist_ok=True)
        
        for name, sentences in SYNTHETIC_DATASETS.items():
            comparisons = []
            cosines = []
            hammings = []
            
            n = len(sentences)
            for i in range(n):
                text_a = sentences[i]
                emb_a = self.embedder.embed(text_a)
                grid_a = self.encoder.encode_seed(emb_a)
                b1 = np.where(grid_a.ravel() <= 0, 0, 1)
                
                for j in range(i + 1, n):
                    text_b = sentences[j]
                    emb_b = self.embedder.embed(text_b)
                    grid_b = self.encoder.encode_seed(emb_b)
                    b2 = np.where(grid_b.ravel() <= 0, 0, 1)
                    
                    # Similaridade de Cosseno (Denso)
                    cos_sim = float(np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b)))
                    cosines.append(cos_sim)
                    
                    # Overlap de Hamming SDR (Esparso)
                    overlap = np.sum((b1 == 1) & (b2 == 1))
                    active = np.sum(b1)
                    hamming_sim = float(overlap / active) if active > 0 else 0.0
                    hammings.append(hamming_sim)
                    
                    comparisons.append({
                        "text_a": text_a,
                        "text_b": text_b,
                        "cosine_similarity": round(cos_sim, 4),
                        "sdr_overlap": round(hamming_sim, 4)
                    })
            
            # Estatísticas Agregadas
            avg_cos = float(np.mean(cosines)) if cosines else 0.0
            avg_ham = float(np.mean(hammings)) if hammings else 0.0
            
            # Interpretação Automática
            interpretation = self._generate_heuristic_interpretation(name, avg_cos, avg_ham)
            
            # Ordenar comparações por SDR Overlap para extrair os extremos
            sorted_comparisons = sorted(comparisons, key=lambda x: x["sdr_overlap"], reverse=True)
            top_5_closest = sorted_comparisons[:5]
            top_5_farthest = sorted_comparisons[-5:][::-1] if len(sorted_comparisons) >= 5 else sorted_comparisons[::-1]
            
            # Estrutura JSON Final
            report = {
                "experiment_set": name,
                "readable_timestamp": readable_ts,
                "timestamp_iso": now.isoformat(),
                "interpretation": interpretation,
                "parameters": {
                    "grid_shape": list(self.grid_shape),
                    "density": self.density,
                    "model_dimensions": self.input_dim
                },
                "metrics_summary": {
                    "average_cosine_similarity": round(avg_cos, 4),
                    "average_sdr_overlap": round(avg_ham, 4)
                },
                "top_5_closest": top_5_closest,
                "top_5_farthest": top_5_farthest,
                "all_comparisons": comparisons
            }
            
            filename = f"semantic_{name}.json"
            filepath = os.path.join(experiment_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4, ensure_ascii=False)
                
            print(f"[+] Relatório {name} salvo em: {filepath}")

if __name__ == "__main__":
    runner = GranularityExperimentRunner()
    runner.run_all_depths()
