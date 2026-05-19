### 📌 Sessão 3 — 18 de maio de 2026 (Atual)
> **Registro de desafios e observações pessoais da Sessão 3.**
>
> **Implementação de uma rede de Hopfield simples e integração com o sistema**
> 1 - Atualizar pesos (sinapses) somando os valores índice por índice
> 2 - Uma matriz de pesos com `shape` (4096, 4096) ocupa 16_777_216 bytes (cada valor é lido como um byte 00000000 ou 00000001) ou 16mb. O ideal é fazer um bitpack para comprimir 8 valores sequenciais em 1 byte, tirando proveito do máximo de memória do sistema. Desta forma, teríamos 2_097_152 bytes ou 2mb, uma redução de 8x. 
>
> **Reflexão sobre Abstração do NumPy (Linha 74 - `np.dot`)**:
> O NumPy é realmente fantástico, mas a abstração esconde muita coisa e às vezes fica difícil entender o que está acontecendo por debaixo dos panos. Por exemplo, na linha 74 (`activation = np.dot(self.weights[i], state)`), interpreto que uma linha específica do vetor de pesos está sendo multiplicada por todos os neurônios. Cada peso está ligado a um neurônio específico para aquela linha da matriz de pesos, que representa os pesos para um determinado neurônio do sistema em relação a todos os outros.
>
> **Reflexão sobre Dualidade de Densidade (SparseEncoder)**:
> O papel do `SparseEncoder` muda drasticamente dependendo do alvo. Para o Autômato Celular (Neocórtex), a esparsidade (poda severa de 95%, `density=0.05`) é vital para evitar explosão caótica e manter a propagação dos gliders. Contudo, para a memória associativa da Rede de Hopfield (Hipocampo), a poda severa destrói o balanço energético Hebbiano. Hopfield exige alta entropia (padrões densos com `density=0.50`, 50% ativos e 50% inativos) para que a matriz não crie buracos negros atratores que causam amnésia. Usamos o mesmo encoder, mas com parametrizações de entropia opostas dependendo da estrutura biológica.
>
> **O Erro como Veículo para o Orgânico (Atratores Espúrios)**:
> O comportamento imperfeito da rede — falhando em reconhecer uma memória inédita e, em vez disso, colapsando para um estado espúrio (uma mistura fantasmal de memórias existentes) — não é um bug sistêmico, mas um simulacro da própria biologia. O cérebro humano também confabula, mistura traços e "alucina" memórias ao tentar encaixar algo totalmente novo em seus atratores pré-existentes. O "erro" matemático da máquina é exatamente o que a torna organicamente plausível e criativa.

---

## 🤖 Status Geral & Objetivos Técnicos da Sessão

Esta sessão marca a inicialização de uma nova fase no desenvolvimento do **Perseus**. Nossos focos principais são:
1. **Verificação do Estado Atual**: Mapear as classes implementadas no Neocórtex, Autômatos, e Encoders.
2. **Refinamento do HopfieldNet**: Consolidar a implementação da rede de Hopfield (`perseus/src/neural_nets/hopfield_net.py`), corrigindo verificações de array do NumPy e estruturando o armazenamento de padrões.
3. **Pilar de Ressonância Episódica e LLM**: Preparar o terreno para a integração de fronteiras de eventos, ressonância e LTP (Long-Term Potentiation).

---

## Status do Projeto (Perseus)

### 1. Neocórtex & Roteamento (Concluído)
- **`Point`** ([point.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/neocortex/point.py)): Representação de sintagmas atômicos com embeddings densos e força de memória (`memory_strength`) incrementada via LTP.
- **`Event`** ([event.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/neocortex/event.py)): Sequência ordenada de `Points`, contendo trajetória semântica (vetor de deslocamento e magnitude) e seed binária 16x16.
    - **DTW (Dynamic Time Warping)** implementado como a métrica de similaridade padrão (`similarity(other)`) para comparar trajetórias completas.
    - **`similarity_direction()`** mantido como alternativa rápida O(1).
- **`EventSchema`** ([event_schema.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/neocortex/event_schema.py)): Região estável da memória que acumula eventos, mantém um `centroid` e gerencia seu próprio `EventModelAutomaton`.
- **`Neocortex`** ([neocortex.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/neocortex/neocortex.py)): Orquestrador central que realiza o roteamento de eventos.
    - **Threshold Dinâmico $\tau(H)$**: Implementado como uma função sigmoide centrada em $H=0.75$ com inclinação $k=8$.
    - **Semântica de Escassez**: Sistemas virgens/vazios (alta entropia) possuem $\tau \approx 0.40$ (altamente permissivo), enquanto sistemas maduros (baixa entropia) exigem $\tau \approx 0.80$ (altamente estritos).

### 2. Autômatos & Encoders (Concluído)
- **`SparseEncoder`** ([encoder.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/encoder/encoder.py)): Dual-projection determinística a partir de embeddings densos. Gera a seed 16x16 e a posição 2D no Neocórtex.
- **`Automaton`** ([grid.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/automaton/grid.py)): Motor Brian's Brain 3-state (OFF $\rightarrow$ ON $\rightarrow$ DYING $\rightarrow$ OFF) operando sob uma grade toroidal.
- **`EventModelAutomaton`** ([event_model_automaton.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/perseus/automaton/event_model_automaton.py)):
    - Modos `PASSIVE_REFLEXIVE` (repouso, baixa frequência) e `HIGH_RES_ACTIVE` (ativado por eventos).
    - Cálculo de ressonância via distância de Hamming sobre seeds salvas.

### 3. Redes Neurais / Hopfield Network (Concluído)
- **`HopfieldNet`** ([hopfield_net.py](file:///Users/tiagocuri/Documents/Repos/beebrain/perseus/src/neural_nets/hopfield_net.py)):
    - Matriz de pesos Hebbiana cumulativa e auto-conexões zeradas na diagonal (`np.fill_diagonal`).
    - Implementação de inferência/evocação (`infer`) com modos **asíncrono** (neurônio-por-neurônio com ordenação aleatória por época) e **síncrono** (paralelo via multiplicação de matrizes).
    - Otimização e prevenção de overflow: acumulação interna com upcast para `int32` enquanto armazena pesos em `int8` (alta eficiência de RAM).
    - Suporte a volumes 3D genéricos (ex: $16 \times 16 \times 16$).

### 4. Validação In-Vitro & Laboratório (Concluído)
- **`semantic_retrieval.py` (Depreciado/Deletado):**
    - Script de simulação inicial deletado para manter a simplicidade arquitetural do projeto. Sua lógica de simulação foi integralmente migrada para a skill dinâmica de testes.
- **`hopfield_runner.py`** ([hopfield_runner.py](file:///Users/tiagocuri/Documents/Repos/perseus/labs/hopfield_experiments/hopfield_runner.py)):
    - Skill agêntica encapsulada para orquestrar novos experimentos de forma parametrizável e dinâmica, gerando relatórios de validação científica detalhados em formato JSON na pasta `/results`.
    - **Evocação com Ruído (Teste A)**: Injeção de 20% de ruído (819 bits invertidos) no padrão associado a *"A mecânica quântica descreve o universo em escalas subatômicas"*. Convergência assíncrona em apenas 2 épocas, obtendo **100.00% de similaridade (recuperação perfeita)**.
    - **Injeção de Conceito Inédito (Teste B)**: Apresentação de frase alienígena não aprendida. A rede rejeitou o padrão (51.9% de similaridade própria) e colapsou organicamente em um **Estado Espúrio** (atração mista e confabulação entre memórias conhecidas com ~75% de similaridade).

---

## Próximos Passos Imediatos
1. **Pipeline de Fronteiras de Eventos (EST)**: Conectar o fluxo para receber sintagmas reais e segmentar via prompts de LLM (Claude).
2. **Ressonância Episódica Passiva**: Implementar o `resonance_check()` em eventos e a janela temporal.
3. **LTP & Decaimento Exponencial**: Implementar potenciação de longo prazo e enfraquecimento de memória temporal.
4. **Bitpacking na Matriz de Pesos (Opcional - Médio Prazo)**: Compactar as sinapses da rede de Hopfield usando `np.packbits` para compressão de 8x (de 16 MB para 2 MB).
