# Perseus — Log de Conversa

> Uma demonstração de como colaborar com uma IA para construir software de pesquisa, do zero à arquitetura completa.
> Cobre três sessões: **13 de maio de 2026** (fundação do projeto), **14 de maio de 2026** (episodic memory & routing), e **18 de maio de 2026** (Hopfield Net & alinhamento).

---

## Sessão 1 — 13 de maio de 2026

### Revisão do BeeBrain

**Tiago:** Faça uma revisão geral na base de código pra entender o projeto, identificar inconsistências e capturar o objetivo de cada componente.

**AI:** Analisou o código e identificou que o BeeBrain usava um grid 128x128 com Brian's Brain como substrato de memória, mas a granularidade era baixa — um único embedding para todo o texto. Propôs evoluir para uma abordagem por sintagmas.

---

### Redesign da Arquitetura

**Tiago:** Texto de entrada é dividido em sintagmas. Cada embedding é transformado em um ponto no grid do neocortex (Indexador Semântico Topológico). PS. Não implemente nenhum código, apenas elabore comigo.

**AI:** Reconheceu a mudança de "texto inteiro como constelação" para "sintagmas como pontos". A palavra **Topológico** é a chave: proximidade no grid deve refletir proximidade semântica.

---

**Tiago:** Os sintagmas quase sempre serão criados em áreas diferentes. Cada região de contexto do neocortex vai criar um autômato dedicado. Um sintagma será representado como um vetor esparso correspondente no autômato.

**AI:** "Isso escala o projeto de uma simulação de laboratório para um sistema multi-agente de processos." Identificou o Neocórtex como um **Atlas Semântico** com autômatos dedicados por região.

---

**Tiago:** Os pontos no neocortex devem estar conectados, respeitando a sequência dos sintagmas. A direção deve ser mantida. Sobre gestão de recursos: Reflexão do agente é onde o autômato faz mais sentido — roda em baixa frequência.

**AI:** Formalizou o Neocórtex como um **Grafo Direcionado**. Identificou dois modos: **Interativo** (alta frequência) e **Reflexivo** (baixa frequência).

---

### Propriedades do Ponto e LTP

**Tiago:** Já enxergo 4 propriedades para um ponto no neocortex: 1-Sintagma, 2-Timestamp, 3-Força da memória, 4-Pontos conectados. Logaritmos são bons pra lidar com potenciação e decaimento.

**AI:** "O uso de logaritmos é perfeito para mimetizar processos biológicos." Formalizou:
- Potenciação: `Ms = Ms + log(Energia_CA)`
- Decaimento: `Ms = Ms · e^(-λ·Δt)`

---

### Mecanismo de Ressonância Passiva

**Tiago:** Para efeito de simplificação, configurações com correspondentes no neocortex podem servir apenas como um "opa, passei perto de uma memória" ao invés de funcionarem como atratores diretos. 2 fatores: 1-quão pequeno é o erro, 2-a força da memória.

**AI:** Formalizou o **Sinal de Ressonância**: `Intensidade = Ms / Erro`. Alta Ms + Erro baixo = lembrança clara. Ms baixo + Erro baixo = déjà vu.

---

### Recuperação Ativa e Entropia

**Tiago:** Sobre entropia, não sei se ficou claro pra mim. Entropia alta é quando temos poucos estados mapeados, certo? Neste caso, não faz mais sentido tornar o sistema MAIS sensível?

**AI:** Confirmou: sistema "vazio" (alta entropia) → limiar **baixo** (mais sensível). Sistema "cheio" → limiar **alto** (mais seletivo). Corrigiu a lógica anterior que estava invertida.

---

### Momentum como Critério de Parada

**Tiago:** O momentum deve ser calculado como o custo de transição de estados do autômato. Se a configuração corresponde a uma memória, o custo é aplicado apenas para células diferentes da configuração recuperada.

**AI:** "Memórias servem como âncoras de custo zero. Cognição familiar gasta menos energia." Adicionou custo ponderado por Ms e múltiplas ressonâncias simultâneas.

---

### Criação do Projeto Perseus

**Tiago:** Crie uma pasta chamada perseus. Este será o nome do novo projeto.

**AI:** Criou estrutura `perseus/docs/`, `perseus/src/perseus/`, `ARCHITECTURE.md` inicial.

---

### Primeiro Código: Visualizador 16x16

**Tiago:** Crie um autômato 16x16 aplicando o Brian's Brain. Quero visualizar apenas o autômato.

**AI:** Criou `grid.py` (motor CA puro) e `automaton_viz.py` (visualizador pygame com paleta dark premium, sidebar com métricas).

---

### HippocampalAutomaton → EventModel

**Tiago:** Precisamos criar uma classe que abstraia um autômato hipocampal. Deve conter: nome da região, array com configurações mapeadas, valor de entropia.

**AI:** Criou `HippocampalAutomaton`. Definiu `mapped` como catálogo de **condições iniciais** (seeds de sintagmas), não snapshots automáticos.

---

**Tiago:** Estado mapeado não é um estado que o autômato gerou e sim, um estado que uma representação de vetor esparsa criou como condição inicial. Um estado mapeado é uma informação que já foi traduzida para o autômato em algum momento.

**AI:** Separou `register()` (API explícita para novos sintagmas) de `step()` (avança o CA sem registrar nada).

---

### Combinatória e Entropia Corrigida

**Tiago:** Lembra que a condição inicial usa apenas FIRING ou INACTIVE, portanto não tenho certeza se devemos fazer 3^256. Porquê a entropia cresce com o número de estados mapeados? Entropia não é a medida da incerteza?

**AI:** Corrigiu dois problemas:
- Espaço correto: `2^256` (seeds são binárias: ON/OFF)
- Entropia = `1 - occupancy` → **decresce** conforme o sistema aprende

---

### Event Perception e EST

**Tiago:** Para chunking: a partir do momento que enxergamos as frases como eventos, os chunks passam a ser autocontidos. A própria LLM vai identificar as fronteiras de eventos.

**AI:** "Essa mudança eleva o nível de abstração do Neocórtex. Se usarmos chunking gramatical puro, o Neocórtex vira um dicionário de fragmentos. Se usarmos Fronteiras de Eventos, vira um diário de significados."

---

**Tiago:** Podemos adotar termos da literatura científica. Ao invés de contexto, teremos **schemas de eventos** no neocortex. Para schemas instanciados, **event models**.

**AI:** Mapeou: EventSchema = molde genérico de conhecimento (permanente). EventModel = representação dinâmica do "agora" (instância ativa).

---

### Refatoração para EST

**Tiago:** Acho que já temos o necessário para começar a implementar. Crie também um enum para definir o estado do EventModelAutomaton.

**AI:** Criou `event_model.py` com enum `EventModelMode` (`PASSIVE_REFLEXIVE` / `HIGH_RES_ACTIVE`). Deletou `hippocampal.py` (obsoleto).

---

**Tiago:** Talvez fique mais intuitivo juntar conceito + funcionalidade no nome. Ex. `event_model_automaton.py`.

**AI:** Renomeou para `EventModelAutomaton`.

---

## Sessão 2 — 14 de maio de 2026

*(A sessão inicia com o projeto já em transição para arquitetura orientada a eventos. `Episode` havia sido eliminado e `Event` era o container unificado.)*

---

### Trajetória Geométrica

**Tiago:** Eu estava tentando imaginar uma trajetória de forma geométrica ou numa função que transforma as partes (sintagmas) no resultado final visualizado como trajetória e não como um ponto.

**AI:** Explicou curvas paramétricas no espaço semântico:
- Piecewise linear: conecta embeddings dos sintagmas em sequência
- Bézier: curva suave atraída pelos pontos intermediários
- DTW como métrica de comparação entre trajetórias completas

---

### DTW: Experimento Headless

**Tiago:** Aplique DTW headless e compare os resultados com direction atual.

**AI:** Criou `scratch_dtw_compare.py` com três cenários:

| Cenário | direction_sim | dtw_sim |
|---|---|---|
| A — trajetórias iguais | 0.987 | 0.970 |
| B — mesmo início/fim, meio diferente | **0.929** | **0.707** |
| C — padrão estrutural similar | 0.378 | 0.441 |

O Cenário B expôs a limitação do `direction`: jura que dois eventos são idênticos (0.93) quando na verdade têm trajetórias distintas no meio.

---

### DTW como Default

**Tiago:** Na verdade quero que você já implemente como default. Mantenha o método anterior como função separada.

**AI:** Implementou em `event.py`:
- `similarity(other)` → **DEFAULT**, usa DTW sobre todos os Points
- `similarity_direction(other, alpha)` → alternativa rápida O(1)

Validação: Cenário B com DTW=0.75 vs direction=0.91 — DTW percebe o desvio no meio.

---

### Limiar τ e Semântica de Escassez

**Tiago:** Qual é mesmo o nosso limiar padrão para considerar um evento um "irmão"?

**AI:** `tau_max = 0.75`, aplicado como `τ(H) = 0.75 × H^1.0`. Alertou que com DTW, os scores são naturalmente mais baixos.

---

**Tiago:** Dar margem vc quer dizer permissividade para entropia alta, né?

**AI:** Reconheceu a imprecisão. A fórmula atual `τ(H) = τ_max × H^α` dava **alta entropia → τ alto → estrito** — o oposto da semântica de escassez biológica.

---

**Tiago:** Eu entendo, mas lembra que conversamos sobre a escassez de informação e como isso facilita a recuperação de memória, mesmo que não haja correlação forte?

**AI:** Identificou a incoerência: sistema virgem deveria ser **permissivo** (baixo τ), não estrito. Propôs inverter:
```
τ(H) = τ_min + (τ_max - τ_min) × (1 - H)^α
```

---

**Tiago:** Exato. Uma criança olha um balão e acha que pode voar. Sobre o threshold, ele está diretamente ligado na entropia ou está hardcoded?

**AI:** É **matematicamente ligado** via função contínua. Mostrou código: `_threshold()` usa `self.entropy` diretamente. Implementou a fórmula invertida com `tau_min=0.40` e `tau_max=0.80`.

---

**Tiago:** Só acho que a curva para a maturidade pode ser mais inflexiva.

**AI:** Mostrou tabela com `α=1,2,3,4`. Com α alto, a curva permanece plana (permissiva) por mais tempo, depois dispara perto de H=0.

---

**Tiago:** Estamos usando qual agora? / Vamos de 2.5.

**AI:** Estava em `α=1.0`. Alterou para `alpha=2.5`.

---

**Tiago:** Ainda está permissivo demais para entropia 0.5. / O sistema não deve permanecer permissivo por muito tempo.

**AI:** Power law com α alto mantinha τ baixo até H=0.5. Propôs **sigmoide** com centro deslocado:
```
τ(H) = τ_min + (τ_max - τ_min) / (1 + exp(k · (H - center)))
```

Mostrou opções com `center=0.5,0.75,0.80,0.85` e diferentes valores de `k`.

---

**Tiago:** Sim [center=0.75, k=8].

**AI:** Implementou. Ciclo de vida resultante:

| H | τ | Fase |
|---|---|---|
| 1.00 | 0.448 | Infância — a criança e o balão |
| 0.75 | 0.600 | Inflexão |
| 0.50 | 0.752 | Quase adulto |
| 0.00 | 0.799 | Maturidade plena |

---

### Documentação

**Tiago:** Atualize o arquivo de arquitetura com essa linda tabela.

**AI:** Atualizou `ARCHITECTURE.md` com fórmula sigmoide, tabela de parâmetros e tabela do ciclo de vida.

---

**Tiago:** Gostaria de criar um arquivo que explica o projeto de forma mais textual. Será que criamos um novo arquivo ou embedamos dentro do arquivo de arquitetura?

**AI:** Recomendou arquivo separado (audiências diferentes: técnica vs. narrativa).

**Tiago:** Sim.

**AI:** Criou `HOW_IT_WORKS.md` cobrindo o pipeline completo com analogias: sintagma → Point → Event → DTW → τ(H) → schema ou spawn.

---

### Memória Agêntica

**Tiago:** Precisamos atualizar algum arquivo de suporte a memória agêntica?

**AI:** Criou KI em `/knowledge/perseus-architecture/` com `metadata.json` e artifact completo da arquitetura.

**Tiago:** E os arquivos aqui dentro do projeto? Backlog, etc.

**AI:** Reescreveu `BACKLOG.md` do zero: removeu referências obsoletas (`Episode`, `EventPoint`), organizou em ✅ Concluído / 🟢 Próximos Passos / 🟡 Médio Prazo / 🔴 Longo Prazo.

---

**Tiago:** Você consegue criar um arquivo com toda esta thread de conversa?

**AI:** Criou este arquivo.

---

## Estado Final do Sistema

```
Point → Event → EventSchema → Neocortex
```

| Componente | Decisão chave |
|---|---|
| `similarity()` | DTW sobre todos os Points (default) |
| `similarity_direction()` | O(1), só start/end (alternativa) |
| `τ(H)` | Sigmoide: `center=0.75, k=8` |
| Semântica | Alta entropia = permissivo (escassez) |
| `Episode` | Deletado — `Event` é o container unificado |
| Schemas | Emergem bottom-up via `route()` |

---

## Sessão 3 — 18 de maio de 2026

### Alinhamento e Inicialização de Sessão

**Tiago:** Vamos iniciar uma nova sessão. Atualize o status do projeto, foque principalmente no Perseus.

**AI:** Mapeou todo o ecossistema do Perseus (Point, Event, EventSchema, Neocortex, SparseEncoder e EventModelAutomaton) e identificou que o status atual das entregas da Sessão 2 está robusto e consistente. Apontou que o foco ativo de desenvolvimento da base de código está em `neural_nets/hopfield_net.py` (Rede de Hopfield). Criou o log da sessão em `docs/sessions/SESSION_003.md` detalhando as inconsistências do HopfieldNet e os próximos passos.

---

### Desenvolvimento e Refinamento do HopfieldNet 3D

**Tiago:** *(Solicitou a atualização do status do projeto)*

**AI:** Consolidou e refinou a implementação da classe `HopfieldNet` (`hopfield_net.py`):
1. **Representação Interna**: Transicionou de listas Python aninhadas para tensores nativos `numpy` eficientes (armazenamento das sinapses cumulativas em `np.int8` com prevenção de transbordo/overflow via upcast `int32` na acumulação de produtos escalares).
2. **Dinâmica de Atração**: Codificou o aprendizado Hebbiano com conversão bipolar automática, eliminação de auto-conexões na diagonal (`np.fill_diagonal`), e inferência de energia mínima nos modos **assíncrono** (atualização sequencial aleatória) e **síncrono** (atualização matricial paralela).
3. **Escala 3D**: Ajustou o `SparseEncoder` para suportar formatos genéricos de grid (`grid_shape`), viabilizando a injeção em volumes tridimensionais (como $16\times16\times16$ correspondendo a 4096 neurônios).

### Experimentos In-Vitro & Validação Cognitiva

**AI:** Desenvolveu um ambiente de simulação e suite de experimentos (`labs/hopfield_experiments/`):
- **`semantic_retrieval.py`**: Gera volumes semânticos densos, consolida memórias e roda dinâmicas de atrator.
    - **Teste A (Corrupção)**: Inseriu 20% de ruído aleatório em uma frase associada à mecânica quântica. O sistema convergiu em apenas 2 épocas no modo assíncrono para **100% de recuperação perfeita (Perfect Recovery)**.
    - **Teste B (Conceito Inédito)**: Injetou uma frase alienígena (inteligência artificial). A rede rejeitou com sucesso o padrão inédito (mantendo similaridade própria de ~51%) e colapsou para um **Estado Espúrio** (confabulação e mistura de atratores pré-existentes, registrando ~75% de similaridade com as memórias conhecidas), demonstrando fidelidade ao comportamento biológico/cognitivo orgânico.
- **`hopfield_runner.py`**: Orquestrador na forma de Skill agêntica que exporta automaticamente relatórios científicos detalhados em JSON.

---

## Estado Final do Sistema

```
Point → Event → EventSchema → Neocortex ──[SparseEncoder (3D)]──> HopfieldNet (Memory Substrate)
```

| Componente | Decisão chave |
|---|---|
| `similarity()` | DTW sobre todos os Points (default) |
| `similarity_direction()` | O(1), só start/end (alternativa) |
| `τ(H)` | Sigmoide: `center=0.75, k=8` |
| Semântica | Alta entropia = permissivo (escassez) |
| `Episode` | Deletado — `Event` é o container unificado |
| Schemas | Emergem bottom-up via `route()` |
| `HopfieldNet` | Tensores NumPy, dinâmicas síncronas/assíncronas, prevenção de overflow |
| `SparseEncoder` | Dual-projection compatível com 2D e 3D |

---

*Projeto: Perseus / BeeBrain — kyber57*
*Período: 13–18 maio de 2026*

