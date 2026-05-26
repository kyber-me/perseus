import sys
import os
import pygame
import numpy as np

# Adicionar a pasta src ao path para imports funcionarem corretamente de forma independente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from embedding.semantic_embedder import SemanticEmbedder
from encoder.encoder import SparseEncoder

# Conjunto de frases pré-configuradas para o laboratório visual (Dataset Temático 25 Frases)
TEST_FACTS = [
    # Theme 1: Astrophysics and Black Holes
    "Supermassive black holes warp space-time at the center of distant galaxies.",
    "Light cannot escape extreme gravity after crossing the event horizon.",
    "Astronomers use radio telescopes to capture the shadow of a singularity horizon.",
    "Hawking radiation describes the slow thermal evaporation of black holes in deep space.",
    "Colossal gravitational distortions in the galactic core prevent the escape of electromagnetic radiation.",
    
    # Theme 2: Culinary Arts and Baking
    "A traditional recipe for homemade bread requires slow fermentation and wheat flour.",
    "The pastry chef prepares a moist chocolate cake using pure cocoa.",
    "Baking sourdough bread in a wood-fired oven creates a golden, crispy crust.",
    "Preparing fresh artisanal pasta requires free-range eggs and vigorous kneading.",
    "Artisanal baking involves mixing simple ingredients and fermenting the dough under controlled temperature.",
    
    # Theme 3: Quantum Mechanics
    "Wave-particle duality shows that electrons behave like waves under specific conditions.",
    "Quantum entanglement links particle states instantaneously across infinite distances.",
    "Heisenberg's uncertainty principle prevents determining both position and momentum precisely.",
    "Superposition allows a qubit to represent multiple logical states simultaneously.",
    "Subatomic particles exist in multiple states until a measurement collapses their wave function.",
    
    # Theme 4: Artificial Intelligence and Deep Learning
    "Deep neural networks adjust their synaptic weights using the backpropagation algorithm.",
    "Large language models utilize the transformer architecture with multi-directional attention.",
    "Reinforcement learning trains autonomous agents by maximizing cumulative rewards in the environment.",
    "Dropout regularization prevents overfitting by randomly deactivating neurons during training.",
    "Deep learning algorithms learn hierarchical representations from massive amounts of data.",
    
    # Theme 5: Domestic Cat Behavior
    "Domestic cats purr to express contentment or to alleviate stress.",
    "Feline predatory behavior is triggered by fast-moving visual stimuli.",
    "Felines groom their fur daily by licking themselves to remove loose hair.",
    "A cat demonstrates affection by rubbing its scent glands against its owner's legs.",
    "Domestic felines spend a large part of the day sleeping in high, warm places."
]

class EmbeddingVisualizer:
    def __init__(self, cell_size=16, grid_dim=27):
        pygame.init()
        self.cell_size = cell_size
        self.grid_dim = grid_dim
        self.grid_shape = (grid_dim, grid_dim)
        
        # Dimensões e Layout
        self.margin = 40
        self.panel_width = self.grid_dim * self.cell_size
        self.panel_height = self.grid_dim * self.cell_size
        
        self.width = self.panel_width * 2 + self.margin * 3
        self.height = self.panel_height + self.margin * 3 + 120 
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Perseus: Sparse Embedding Visualizer (27x27)")
        
        # Estilo Editorial e Geométrico
        self.font_large = pygame.font.SysFont("Courier", 18, bold=True)
        self.font_small = pygame.font.SysFont("Courier", 14)
        self.font_metrics = pygame.font.SysFont("Courier", 16, bold=True)
        
        self.BG_COLOR = (12, 12, 14)
        self.TEXT_COLOR = (200, 200, 200)
        self.CELL_OFF = (25, 25, 28)
        self.CELL_A_ON = (0, 255, 200)     # Neon Cyan
        self.CELL_B_ON = (255, 0, 150)     # Neon Magenta
        self.METRIC_COLOR = (240, 200, 50) # Dourado Estético
        
        # Subsistemas Perseus
        print("[*] Initializing SemanticEmbedder and SparseEncoder (27x27)...")
        self.embedder = SemanticEmbedder(input_dim=768)
        self.encoder = SparseEncoder(
            input_dim=768, 
            grid_shape=self.grid_shape, 
            density=0.15, # 15% de ativação
            seed=42
        )
        
        self.idx_a = 0
        self.idx_b = 1
        self.facts = TEST_FACTS
        
        self._compute_current()

    def _compute_current(self):
        self.text_a = self.facts[self.idx_a]
        self.text_b = self.facts[self.idx_b]
        
        # 1. Gerar representações densas (384D)
        self.emb_a = self.embedder.embed(self.text_a)
        self.emb_b = self.embedder.embed(self.text_b)
        
        # 2. Projetar para grades binárias esparsas (27x27)
        self.grid_a = self.encoder.encode_seed(self.emb_a)
        self.grid_b = self.encoder.encode_seed(self.emb_b)
        
        # 3. Calcular métricas
        # Cosine Similarity (Continuous space)
        self.cos_sim = np.dot(self.emb_a, self.emb_b) / (np.linalg.norm(self.emb_a) * np.linalg.norm(self.emb_b))
        
        # Hamming / SDR Overlap Ratio (Binary space)
        # O Hamming clássico conta zeros (infla similaridade em matrizes esparsas).
        # Para SDRs, medimos o Overlap de intersecção ativa (Active Intersection / k).
        b1 = np.where(self.grid_a.ravel() <= 0, 0, 1)
        b2 = np.where(self.grid_b.ravel() <= 0, 0, 1)
        
        overlap = np.sum((b1 == 1) & (b2 == 1))
        active_cells = np.sum(b1)
        self.hamming_sim = overlap / active_cells if active_cells > 0 else 0.0

    def _generate_report(self):
        print("\n" + "="*80)
        print("🧠 MEMORY DISTANCE REPORT (ALL PAIRS)")
        print("="*80)
        
        n = len(self.facts)
        results = []
        for i in range(n):
            emb_i = self.embedder.embed(self.facts[i])
            grid_i = self.encoder.encode_seed(emb_i)
            b_i = np.where(grid_i.ravel() <= 0, 0, 1)
            
            for j in range(i + 1, n):
                emb_j = self.embedder.embed(self.facts[j])
                grid_j = self.encoder.encode_seed(emb_j)
                b_j = np.where(grid_j.ravel() <= 0, 0, 1)
                
                cos_sim = np.dot(emb_i, emb_j) / (np.linalg.norm(emb_i) * np.linalg.norm(emb_j))
                
                overlap = np.sum((b_i == 1) & (b_j == 1))
                active = np.sum(b_i)
                hamming_sim = overlap / active if active > 0 else 0.0
                
                results.append({
                    'pair': (i, j),
                    'text_a': self.facts[i],
                    'text_b': self.facts[j],
                    'cos_sim': float(cos_sim),
                    'hamming_sim': float(hamming_sim)
                })
                
        results_cos = sorted(results, key=lambda x: x['cos_sim'])
        results_ham = sorted(results, key=lambda x: x['hamming_sim'])
        
        def print_top3(title, sorted_list, metric_key, reverse=False):
            print(f"\n🔹 {title}")
            lst = sorted_list[::-1] if reverse else sorted_list
            for idx, res in enumerate(lst[:3]):
                print(f"  {idx+1}. {res[metric_key]:.2%} | {res['text_a'][:30]:<30} <-> {res['text_b'][:30]:<30}")
 
        print_top3("HIGHEST Similarities (Cosine - Dense 768D)", results_cos, 'cos_sim', reverse=True)
        print_top3("LOWEST Similarities (Cosine - Dense 768D)", results_cos, 'cos_sim', reverse=False)
        
        print_top3("HIGHEST Similarities (SDR Overlap Ratio - Sparse 27x27)", results_ham, 'hamming_sim', reverse=True)
        print_top3("LOWEST Similarities (SDR Overlap Ratio - Sparse 27x27)", results_ham, 'hamming_sim', reverse=False)
        print("\n" + "="*80 + "\n")

    def draw_grid(self, surface, grid, x_offset, y_offset, color_on):
        # Fundo do painel
        pygame.draw.rect(
            surface, 
            (20, 20, 25), 
            (x_offset - 5, y_offset - 5, self.panel_width + 10, self.panel_height + 10)
        )
        # Células
        for y in range(self.grid_dim):
            for x in range(self.grid_dim):
                rect = pygame.Rect(
                    x_offset + x * self.cell_size + 1, 
                    y_offset + y * self.cell_size + 1, 
                    self.cell_size - 2, 
                    self.cell_size - 2
                )
                if grid[y, x] > 0:
                    pygame.draw.rect(surface, color_on, rect)
                else:
                    pygame.draw.rect(surface, self.CELL_OFF, rect)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(self.BG_COLOR)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.idx_a = (self.idx_a - 1) % len(self.facts)
                        self._compute_current()
                    elif event.key == pygame.K_RIGHT:
                        self.idx_a = (self.idx_a + 1) % len(self.facts)
                        self._compute_current()
                    elif event.key == pygame.K_UP:
                        self.idx_b = (self.idx_b - 1) % len(self.facts)
                        self._compute_current()
                    elif event.key == pygame.K_DOWN:
                        self.idx_b = (self.idx_b + 1) % len(self.facts)
                        self._compute_current()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # --- Grid Rendering ---
            y_grids = self.margin + 80
            
            # Grid A
            x_grid_a = self.margin
            self.draw_grid(self.screen, self.grid_a, x_grid_a, y_grids, self.CELL_A_ON)
            
            # Grid B
            x_grid_b = self.margin * 2 + self.panel_width
            self.draw_grid(self.screen, self.grid_b, x_grid_b, y_grids, self.CELL_B_ON)
            
            # --- Text Overlay ---
            def render_text(txt, x, y, font, color=self.TEXT_COLOR):
                if len(txt) > 42:
                    txt = txt[:39] + "..."
                surf = font.render(txt, True, color)
                self.screen.blit(surf, (x, y))
            
            # Title Headers
            render_text("Pattern A (Arrows ⬅ ➡)", x_grid_a, self.margin, self.font_large, self.CELL_A_ON)
            render_text(self.text_a, x_grid_a, self.margin + 30, self.font_small)
            
            render_text("Pattern B (Arrows ⬆ ⬇)", x_grid_b, self.margin, self.font_large, self.CELL_B_ON)
            render_text(self.text_b, x_grid_b, self.margin + 30, self.font_small)
            
            # --- Distances HUD ---
            y_metrics = y_grids + self.panel_height + self.margin
            
            # Fundo das métricas
            pygame.draw.rect(
                self.screen, 
                (20, 20, 25), 
                (self.margin, y_metrics - 15, self.width - self.margin*2, 60),
                border_radius=4
            )
            
            metrics_txt_1 = f"Cosine Sim (Dense 768D)      : {self.cos_sim:+.2%}"
            metrics_txt_2 = f"SDR Overlap (Sparse 27x27)    : {self.hamming_sim:+.2%}"
            
            render_text(metrics_txt_1, self.margin + 20, y_metrics, self.font_metrics, self.METRIC_COLOR)
            render_text(metrics_txt_2, self.margin + 20, y_metrics + 20, self.font_metrics, self.METRIC_COLOR)
            
            pygame.display.flip()
            clock.tick(30)
            
        pygame.quit()
        self._generate_report()

if __name__ == "__main__":
    app = EmbeddingVisualizer()
    app.run()
