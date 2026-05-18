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

---

## 🔴 Longo Prazo / Pesquisa

- [ ] **Custo direcional no autômato**: diferenciar pesos de transição OFF→ON vs DYING→OFF
- [ ] **Mecanismo de atração (bias espacial)**: campos de probabilidade para guiar o CA
- [ ] **Modulação de temperatura**: integrar estado de atenção global ao roteamento
- [ ] **Comunicação inter-autômatos**: sincronia de fase entre schemas
- [ ] **Índice ANN plugável**: Ball Tree → NSW/HNSW → LSH → IVF

---

*Última atualização: 2026-05-14*
