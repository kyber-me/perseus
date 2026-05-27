# Perseus — Backlog

## ✅ Concluído

- **Arquitetura base**:
    - `Point` (sintagma + embedding + memory_strength) — sem seed
    - `Event` (sequência de Points + seed + trajetória + quorum) — container episódico unificado
    - `EventSchema` (UUID, concept, centroid, autômato)
    - `Neocortex` (roteamento automático + registro duplo por nome e UUID)
    - `SparseEncoder` (dual-projection: seed 16×16 + posição 2D)
- **Roteamento**:
    - `Neocortex.route(event)` com max-similarity (DTW) e threshold dinâmico
    - DTW implementado como `similarity()` default em `Event`
    - `similarity_direction()` mantido como alternativa rápida O(1)
- **Threshold τ(H)**:
    - Sigmoide invertida: alta entropia → permissivo, baixa → estrito
    - Parâmetros: `tau_min=0.40`, `tau_max=0.80`, `center=0.75`, `k=8.0`
- **Limpeza arquitetural**:
    - Classe `Episode` deletada — `Event` é o container unificado
    - `schema_id` (UUID) adicionado ao `Event` e ao `EventSchema`
- **Documentação**:
    - `ARCHITECTURE.md` — referência técnica com fórmulas e tabelas
    - `HOW_IT_WORKS.md` — explicação narrativa acessível
    - `BACKLOG.md` — este arquivo
- **Estudos e Preservação Métrica (Inglês Nativo & Centramento de Bacia)**:
    - Transição do pipeline de embeddings e do visualizador interativo para o modelo `BAAI/bge-base-en-v1.5` sob premissa em inglês nativo.
    - Implementação de **Centramento Semântico (Contrastive Centering)** no pipeline experimental para eliminar o "efeito cone" de similaridade típico de transformers de linguagem.
    - Alcance de **$11.17\%$** de SDR Overlap inter-tema (abaixo do piso estatístico de $15.00\%$) e uma razão de contraste físico de **$2.70\times$** (prevenindo vazamentos cruzados em CA3).
    - Criação da **Skill Agêntica local (`semantic-granularity-experiment`)** e do **Livro de Registro Histórico Central (ledger dinâmico em `results/report.md`)** para conduzir e documentar as execuções de forma puramente qualitativa e dinâmica.
- **Laboratório de Distribuição de Embeddings e Componentes de Alto Sinal**:
    - Criação do laboratório `labs/embedding_distribution/` para analisar matematicamente a distribuição de probabilidade Gaussiana de embeddings BGE de 768 dimensões.
    - Implementação da extração parametrizável por CLI de outliers de alto sinal (extremas caudas $>3\sigma$ e zona de transição $2\sigma$-$3\sigma$).
    - Renderização de histograma científico de alta fidelidade com Matplotlib (Neon Dark Mode) para visualizar a aderência à curva de densidade de probabilidade (PDF) de Gauss.
    - Criação de skill agêntica local (`embedding-distribution-analysis`) para conduzir e mapear spikes semânticos em novas frases de forma automatizada.

---

## 🟢 Próximos Passos (Prioridade Alta)

- [ ] **Pipeline LLM — Segmentação de Eventos**:
    - [ ] Prompt de detecção de fronteiras de eventos (EST) via LLM
    - [ ] Receber lista de sintagmas segmentados e construir `Points` com embeddings reais
    - [ ] Lógica de "High-Res Sampling" disparada por fronteira de evento

- [ ] **Pipeline LLM — Evolução de Conceito**:
    - [ ] Integrar LLM ao `EventSchema.absorb()` para atualizar `concept` após cada novo evento
    - [ ] Definir prompt: recebe eventos anteriores + novo evento, retorna descrição textual do schema

- [ ] **Ressonância Episódica**:
    - [ ] Implementar `resonance_check()` em `Event`: detectar co-ocorrência passiva de `quorum` Points nos autômatos em modo `PASSIVE_REFLEXIVE` dentro de `time_window_ticks`
    - [ ] Integrar ao loop principal de ticks do sistema

- [ ] **Documentação & README**:
    - [ ] Criar um `README.md` descritivo detalhando a nova camada de memória associativa inspirada no hipocampo (utilizando Redes de Hopfield 3D) e como ela se integra às projeções esparsas e ao Neocórtex.

---

## 🟡 Médio Prazo

- [ ] **LTP (Long-Term Potentiation)**:
    - [ ] Lógica de acúmulo de `memory_strength` nos Points após ressonâncias
    - [ ] Decaimento temporal de `memory_strength` (curva exponencial)

- [ ] **Calibração empírica de τ**:
    - [ ] Calcular distâncias pairwise entre embeddings dos sintagmas de um Event
    - [ ] Usar desvio padrão como retroalimentação para calibrar `tau_min`/`tau_max`

- [ ] **Algoritmos de busca para roteamento**:
    - [ ] Estudar Ball Tree (O(log N), suporta métricas customizadas)
    - [ ] Avaliar HNSW (estado da arte, usado em FAISS/hnswlib)
    - [ ] Implementar `SchemaIndex` plugável no `Neocortex`

- [ ] **Visualizador**:
    - [ ] Adaptar visualizador existente para nova estrutura (Event, schema_id)
    - [ ] Mostrar trajetória DTW na visualização 2D

- [ ] **Bitpacking na Matriz de Pesos (Hopfield)**:
    - [ ] Binarização das sinapses unificadas pós-treino ($w_{ij} \in \{-1, 1\}$)
    - [ ] Compactar a matriz unificada final de 16 MB para 2 MB usando `np.packbits` (redução de 8x para grids $16\times 16\times 16$)

- [x] **Pesquisa de Embeddings e Isotropização**:
    - [ ] Avaliar **Model Routing**: usar modelos distribuídos estáticos (ex: GloVe, fastText) para sintagmas atômicos isolados (que sofrem colapso de contexto) e Transformers (BGE) para macro-eventos.
    - [ ] Avaliar estratégias de projeção de dimensionalidade mista no `SparseEncoder` caso o Roteamento de Modelos seja implementado.
    - [x] Testar normalização de pós-processamento (Isotropização / Mean Centering) para alongar o "Cone Semântico" e aumentar a variância das similaridades de Cosseno (implementado no pipeline experimental).

---

## 🔴 Longo Prazo / Pesquisa

- [ ] **Regionalização do Neocórtex (Grids Heterogêneos)**: Avaliar a geração de SDRs de tamanhos diferentes (ex: 16x16 para conceitos, 27x27 para eventos macro). Isso exigiria criar sub-regiões hipocampais independentes para cada escala, simulando a especialização topológica das colunas corticais biológicas.
- [ ] **Custo direcional no autômato**: diferenciar pesos de transição OFF→ON vs DYING→OFF
- [ ] **Mecanismo de atração (bias espacial)**: campos de probabilidade para guiar o CA
- [ ] **Modulação de temperatura**: integrar estado de atenção global ao roteamento
- [ ] **Comunicação inter-autômatos**: sincronia de fase entre schemas
- [ ] **Índice ANN plugável**: Ball Tree → NSW/HNSW → LSH → IVF

---

*Última atualização: 2026-05-26*
