> **Meta-Diretriz de Evolução**: Identificar fronteiras entre novos registros e registros antigos. Em caso de conflito, o novo registro sobrepõe-se ao antigo. Em cenários de não-conflito e não-ambiguidade, as informações/sugestões anteriores devem ser reorganizadas e preservadas para utilidade futura.

## 1. Resumo do Consenso Atual
A memória no Perseus é um processo metabólico. Cada sintagma é um ponto no Neocórtex com quatro propriedades fundamentais (**Sintagma, Timestamp, $M_s$ e Conexões**). A Força da Memória ($M_s$) acumula energia logarítmica via autômatos (Potenciação) e sofre decaimento temporal. O Momentum do CA é o custo acumulado de transição de estados — ele dita o ritmo do LTP e o critério de parada da recuperação ativa.

## 2. Visão Geral
O Perseus é uma evolução do BeeBrain, focando em uma representação de memória mais granular, regionalizada e metabolicamente inspirada. O sistema transita de uma "constelação única por texto" para um "ecossistema de processos paralelos" baseados em sintagmas.

---

## 3. Fases do Pipeline de Memória (Fluxo de Processamento)

O processamento semântico do Perseus é estruturado em camadas (fases) claras, cada uma alinhada a uma mecânica biológica da memória (recuperação, criatividade, etc).

### Fase 1: Processamento e Segmentação de Eventos (EST / Lobo Frontal)
- **Objetivo**: Processamento da entrada de texto para identificação das fronteiras de eventos e criação dos sintagmas.
- **Mecânica**: Este processo é parametrizável para ajustar a granularidade do evento, podendo fatiar desde eventos macro inteiros até conceitos atômicos específicos.
- **Processamento Atual**: Em vez de chunking gramatical fixo, o sistema utiliza a **Teoria de Segmentação de Eventos (EST)** executada inicialmente por uma LLM (que atua como o Lobo Frontal). Cada fronteira de evento dispara um **Pico de Amostragem (High-Res)** no autômato correspondente.

### Fase 2: Geração de Embeddings Semânticos (`semantic_embedder`)
- **Objetivo**: Vetorização matemática contínua.
- **Mecânica**: O módulo `semantic_embedder` recebe um ou um conjunto de sintagmas gerados na Fase 1 e os converte em embeddings semânticos densos (ex: 768D). Estes vetores são a matéria-prima para a projeção espacial e esparsa nas próximas fases.

### Passo 3: Recuperação Ativa via Event Models
- O autômato instanciado funciona como um **Event Model** (representação dinâmica do evento atual).
- **Heurística de Recuperação**:
    1. **Acima do Limiar**: Apenas estados com ressonância superior ao limiar dinâmico são recuperados.
    2. **Influência de $M_s$**:
        - Memórias fracas: Recuperação isolada.
        - Memórias fortes: Trazem **Derivados** via Softmax.
- **Limiar Dinâmico (Sensibilidade)**:
    - O limiar é inversamente proporcional à **Entropia** (incerteza) do sistema.
    - **Ocupação**: $\frac{\log(\text{mapped} + 1)}{\log(2^N)}$.
    - **Entropia ($H$)**: $1 - \text{Ocupação}$.
- **Modos de Operação do Event Model**:
    1. **High-Res Active**: Ativado por uma fronteira de evento; o autômato "digere" a nova semente em alta frequência.
    2. **Passive-Reflexive (Repouso)**: Modo padrão onde o autômato mantém a coerência do schema sem entrada externa ativa.

### Hierarquia de Memória
O modelo adota três níveis de abstração, do mais atômico ao mais abstrato:

| Classe | Descrição | Analoçia biológica |
|---|---|---|
| `Point` | Sintagma individual com embedding. Não possui seed. | Neurônio / representação local |
| `Event` | Sequência ordenada de Points com embedding holístico, seed, trajetória e quorum. | Memória episódica |
| `EventSchema` | Padrão emergente de múltiplos Events. Possui UUID, concept e centroid. | Área neocortical especializada |

- **`Event` como unidade episódica**: O `Event` é simultaneamente a representação de um evento EST e o container episódico (substitui o `Episode` anterior). Ele guarda `resonance_threshold`, `time_window_ticks` e `quorum` para detecção passiva de memórias.
- **Schemas emergem bottom-up**: Um `EventSchema` não é pré-definido. Ele nasce quando um `Event` chega ao Neocórtex sem irmao suficientemente próximo. O conceito (`concept`) evolui via LLM a cada novo evento absorvido.

### Passo 3: Roteamento e Instanciação Dinâmica

#### Como um evento encontra seu schema ("irmão")

Quando um novo `Event` chega ao Neocórtex, o sistema precisa decidir:
> *"Este evento é suficientemente parecido com algum evento que já vi antes? Se sim, ele pertence ao mesmo schema. Se não, criamos um schema novo."*

Isso envolve **dois parâmetros distintos** que é importante não confundir:

---

**Parâmetro 1 — Métrica de similaridade (`sim`)**

Mede o quão parecidos são dois Events. Combina:
- **Trajetória** (`direction`): para onde o evento "caminha" no espaço semântico (do primeiro ao último Point).
- **Posição** (`embedding`): onde o evento está no espaço semântico como um todo.

$$\text{sim}(E_1, E_2) = 0{,}5 \cdot \underbrace{\cos(\vec{dir}_1, \vec{dir}_2)}_{\text{trajetória}} + 0{,}5 \cdot \underbrace{\cos(\mathbf{emb}_1, \mathbf{emb}_2)}_{\text{posição}}$$

Resultado: número entre `0` (nada parecidos) e `1` (idênticos).

---

**Parâmetro 2 — Limiar de roteamento (`τ`)** ← *o "threshold de irmão"*

Define **a partir de qual similaridade** um evento é considerado "irmão" de um schema existente.
A curva é uma **sigmoide** — não linear, biologicamente inspirada:

$$\tau(H) = \tau_{min} + \frac{\tau_{max} - \tau_{min}}{1 + e^{\,k \cdot (H - \text{center})}}$$

| Parâmetro | Valor padrão | Significado |
|---|---|---|
| `τ_min` | `0.40` | Piso permissivo (sistema virgem) |
| `τ_max` | `0.80` | Teto estrito (sistema maduro) |
| `center` | `0.75` | Ponto de inflexão — onde τ = (τ_min + τ_max) / 2 |
| `k` | `8.0` | Inclinação — quanto maior, mais abrupta a transição |

**Ciclo de vida do Neocórtex:**

| H (entropia) | τ | Fase |
|---|---|---|
| 1.00 | 0.448 | Infância — aceita correlações fracas (a criança e o balão) |
| 0.75 | 0.600 | Inflexão — aprendizado acelerado |
| 0.50 | 0.752 | Quase adulto — já muito seletivo |
| 0.25 | 0.793 | Praticamente blindado |
| 0.00 | 0.799 | Maturidade plena |

A janela permissiva dura apenas até **H ≈ 0.85**. Depois a curva sobe rapidamente — o sistema aprende rápido.

> ⚠️ A `sim()` também usa um parâmetro interno `α=0.5` para ponderar trajetória vs. posição. Esse `α` é **independente** de `k` e `center` do threshold — não confundir.

---

**Algoritmo de roteamento (`Neocortex.route(event)`):**
1. Para cada schema $S_i$, encontrar o evento mais parecido: $\text{score}(S_i) = \max_{e_j \in S_i} \text{sim}(E_{new}, e_j)$
2. Pegar o schema vencedor: $\text{winner} = \arg\max \, \text{score}(S_i)$
3. Se $\text{score}(\text{winner}) \ge \tau(H)$ → absorver no schema vencedor.
4. Senão → criar novo schema e absorver lá.

- **O centroid** do schema é mantido para uso futuro em posicionamento 2D e pré-filtro de busca, **não** para roteamento.
- **Roadmap de busca** (a estudar): Ball Tree → NSW/HNSW → LSH → IVF.



### Memória Episódica e Ressonância Passiva
- Cada `Event` possui `quorum = round(size × resonance_threshold)` (default 35%).
- O episódio é "surfaceado" quando `quorum` Points ressoarem (Hamming < limiar) nos seus respectivos autômatos em modo `PASSIVE_REFLEXIVE` dentro de `time_window_ticks` ticks.
- Efeito criativo: análogo ao **Default Mode Network** biológico — memórias emergem sem estímulo direto.

### Passo 4: Conectividade, Metabolismo e Momentum (LTP)
- **Grafo Semântico**: Os pontos no Neocórtex são conectados de forma direcionada para preservar a sequência dos sintagmas ($P_1 \rightarrow P_2 \rightarrow P_3 \dots$).
- **Propriedades do Point**:
    1. **Sintagma**: Conteúdo textual/semântico original.
    2. **Embedding**: Vetor denso do sintagma (sem seed — seeds pertencem ao Event).
    3. **Timestamp**: Registro da última ativação.
    4. **memory_strength**: Força da memória, acumulada via LTP.
    5. **Conexões**: Lista de adjacência (próximos Points na sequência do Event).

- **Propriedades adicionais do Event**:
    1. **embedding**: Vetor holístico do texto completo do evento.
    2. **seed**: Grid binário 16×16 (input do EventModelAutomaton).
    3. **direction / magnitude**: Trajetória semântica (do primeiro ao último Point).
    4. **schema_id / schema_name**: Referência ao schema de destino.
    5. **quorum / resonance_threshold / time_window_ticks**: Parâmetros de ressonância episódica.

- **Momentum — Custo de Transição de Estados**:
    - O Momentum é calculado tick-a-tick como o custo de transição do CA.
    - **Algoritmo**:
        1. **Sem Ressonância**: Custo = número total de neurônios que mudaram de estado em relação ao tick anterior (custo bruto).
        2. **Com Ressonância (1 memória)**: Custo = apenas os neurônios que diferem da configuração da memória evocada. O desconto é proporcional ao $M_s$ da memória (memórias mais fortes absorvem mais custo).
        3. **Com Múltiplas Memórias**: Custo residual = neurônios que diferem de **todas** as configurações evocadas simultaneamente (intersecção dos resíduos), com desconto ponderado pela média de $M_s$ de cada memória evocada.
    - **Custo Direcional (Em Análise)**: Distinguir o peso de transições OFF→ON (novas ativações) vs. ON→DYING vs. DYING→OFF, pois diferentes fases têm valores cognitivos distintos.
    - **Critério de Parada**: O autômato encerra a fase de Recuperação Ativa quando o custo acumulado atinge o threshold de LTP. A energia total é então consolidada no $M_s$ do ponto.

- **Mecanismo de LTP e Decaimento**:
    - **Potenciação**: O acúmulo de custo de transição é processado logaritmicamente ao ser transferido para $M_s$.
    - **Decaimento**: $M_s$ diminui ao longo do tempo com base no `Timestamp` (função exponencial).

- **Modo Reflexivo e Ressonância**:
    - O autômato opera de forma independente e "livre".
    - O Neocórtex atua como um observador passivo que compara a configuração atual do grid com as configurações mapeadas (seeds).
    - **Sinal de Ressonância**: Um indicador de reconhecimento gerado quando a configuração do CA se aproxima de uma memória existente.
    - O sinal é calculado com base em dois fatores:
        1. **Proximidade**: O resultado da função de erro (distância entre a configuração atual e a mapeada).
        2. **Força da Memória ($M_s$)**: O quão consolidada aquela memória está no Neocórtex.

---

## 3. Notas de Design e Sugestões (Antigravity)

### Sugestões Técnicas
- **Grids Reduzidos**: Utilizar grades menores (ex: 16x16 ou 32x32) para que os autômatos alcancem estados de estabilidade (atratores) e ressonância mais rapidamente.
- **Função de Erro**: Implementar uma comparação holística da configuração total do grid (Hamming distance normalizada) para detectar ressonância com as sementes registradas.
- **Métricas Logarítmicas**: Utilizar escalas logarítmicas para normalizar a ocupação e a entropia contra o espaço combinatorial massivo ($2^N$), permitindo que o sistema responda a novos registros de forma granular.
- **Estrutura de Dados**: Utilizar um banco de grafos para gerenciar os pontos do Neocórtex e suas conexões direcionadas.
- **Dinâmica de Decaimento**: Implementar o decaimento em "background ticks" ou sob demanda no momento da recuperação para otimizar performance.
- **Escalabilidade de Contexto**: Implementar o "Atlas Semântico" de forma que novas áreas de contexto só sejam criadas se a distância para a área mais próxima for maior que o limiar $\tau$.
- **Gestão de Processos**: Como os autômatos rodam *ad infinitum*, implementar um sistema de "Lazy Execution" ou "Sleep Mode" para autômatos cujos pontos não foram estimulados recentemente, preservando CPU.

### Desafios e Questões em Aberto
- **Materialização Matemática (Próxima Prioridade)**: Definir escalas e valores concretos: o que é o "custo" em unidades, qual a escala de $M_s$, quais os valores dos thresholds de LTP e de limiar de ressonância.
- **Custo Direcional**: Avaliar se transições OFF→ON devem ter peso maior que DYING→OFF, dado que representam "pensamentos novos" vs. decaimento natural.
- **Heurística de Recuperação**: A estratégia atual (limiar + $M_s$) é um ponto de partida. Será necessária uma heurística mais sofisticada para escalar, especialmente para controlar a saturação do prompt.
- **Mecanismo de Atração**: Implementar um campo de probabilidade onde células próximas a memórias existentes têm maior chance de ativação (Bias Espacial).
- **Comunicação Inter-Autômatos**: Como a relação entre sintagmas em autômatos diferentes é processada além da conexão no grafo?
    - *Sugestão*: Explorar sincronia de fase (oscilações) entre autômatos que compartilham uma "thread of thought".
- **Modulação de Temperatura (Atenção)**: Explorar o uso da "Temperatura" no Softmax de recuperação para controlar o foco (T baixo) vs. pensamento lateral (T alto), possivelmente regulado pelo estado global de atenção.
- **Enriquecimento Semântico (Input)**: Como o sistema "acorda" memórias relacionadas antes de enviar o prompt final ao Agente?

---

## 4. Estrutura do Projeto (Em construção)
- `perseus/src/` : Código fonte.
- `perseus/docs/` : Documentação técnica.
- `perseus/lab/`  : Experimentos de calibração de energia e LTP.
