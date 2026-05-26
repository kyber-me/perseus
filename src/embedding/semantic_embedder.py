import numpy as np
# import hashlib

class SemanticEmbedder:
    """
    Módulo unificado para geração de embeddings densos semânticos.
    Integra a biblioteca fastembed como provedor nativo,
    mantendo um fallback determinístico para robustez do sistema.
    """
    def __init__(self, input_dim: int = 768):
        self.input_dim = input_dim
        self._embed_model = None
        self._try_init_fastembed()

    def _try_init_fastembed(self):
        try:
            from fastembed import TextEmbedding
            # Apenas inicializa silenciosamente; os prints detalhados ficam para o script chamador se necessário.
            self._embed_model = TextEmbedding(model_name="BAAI/bge-base-en-v1.5")
        except ImportError:
            self._embed_model = None

    def embed(self, text: str) -> np.ndarray:
        """
        Retorna o vetor de embedding denso normalizado (l2) correspondente ao texto.
        """
        if self._embed_model is None:
            raise RuntimeError("Falha na geração do embedding: o modelo fastembed não está carregado.")

        vectors = list(self._embed_model.embed([text]))
        v = np.array(vectors[0], dtype=np.float32)
        return v / np.linalg.norm(v)
