### 📌 Sessão 4 — 19 de maio de 2026 (Manhã) (Atual)
> **Registro de desafios e observações da Sessão 4 (Sessão da Manhã).**
>
> **Faseamento e Estruturação Semântica (Fase 1 e 2)**:
> Formalizamos o pipeline do Perseus em camadas claras no `docs/ARCHITECTURE.md`. A Fase 1 (Segmentação de Fronteiras de Eventos via LLM) alimenta a Fase 2 (Vetorização via `semantic_embedder`). A execução do runner simulou sinteticamente a Fase 1 usando sintagmas em inglês de 4 níveis de granularidade semântica (Eventos Macro, Sub-eventos, Entidades e Conceitos Atômicos).
>
> **A Mágica do Grid 27x27 e a Anisotropia dos Embeddings**:
> * O grid $27 \times 27$ (729 células) provou-se ideal para projetar os embeddings de 768 dimensões com perda geométrica quase nula no `SparseEncoder`, visto que o up/down-sampling espacial é virtualmente nulo.
> * Identificamos um fenômeno clássico de **Anisotropia (Cone Semântico)** nos embeddings do `bge-base-en-v1.5`, onde palavras muito relacionadas (como "cat" e "fox") atingem no máximo 61% de similaridade de cosseno, enquanto conceitos totalmente distintos não caem abaixo de 45-50%. Isso se deve ao espalhamento cônico natural em altas dimensões e ao colapso de contexto que modelos de sentenças sofrem ao receber termos isolados (a média ponderada de infinitos contextos para uma só palavra esmaga a identidade particular).
>
> **Soluções Estruturadas no Backlog**:
> 1. *Isotropização (Mean Centering)*: Pós-processamento para alongar a variância e esticar os Cossenos no espaço denso.
> 2. *Model Routing*: Roteamento dinâmico baseado no token count (ex: enviar conceitos pequenos ao `GloVe`/`Word2Vec` para manter pureza identitária, e frases complexas ao `BGE`).
> 3. *Grids Heterogêneos (Regionalização)*: Estudo para suportar sub-regiões corticais de tamanhos diferentes (ex: 16x16 para conceitos e 27x27 para eventos).
>
> **Motor de Experimentação e Organização**:
> O `granularity_runner.py` foi implementado em inglês nativo e agora separa cada bateria de testes em pastas nomeadas por timestamp legível em `results/`. Os relatórios JSON agora registram as 5 comparações mais próximas (`top_5_closest`), as 5 mais distantes (`top_5_farthest`) e a matriz completa.
