# Plano de Evolução Arquitetônica: Bee Brain ➔ Perseus
<!-- Documento de Alinhamento Conceitual e Roadmap de Implementação Unificado -->

> **Meta-Diretriz de Transição**: Preservar o rigor matemático e a elegância biológica já desenvolvidos no Perseus, integrando os avanços da nova visão teórica (Giro Dentado, Redes de Hopfield 24x24 como CA3, LTD, Clusters por Saturação, Modulação Alostérica em Background e Un-embedding local para Proatividade).

---

## 1. Síntese da Mudança de Visão

O **Projeto Perseus** deixa de ser um processador semântico de linguagem meramente reativo para se tornar um **cérebro sintético proativo**. 

### O que muda na prática?
1. **Transição de Substrato (CA ➔ Hopfield CA3)**: 
   Na arquitetura anterior, o substrato de memória dinâmica local de cada `EventSchema` era um Autômato Celular (CA) bidimensional rodando *Brian's Brain*. A ressonância era detectada por proximidade de Hamming passiva.
   Na **nova visão**, o substrato de memória é a **Unidade CA3 Hipocampal**, modelada por uma **Rede de Hopfield Recorrente** otimizada com dinâmica de atratores por minimização de energia. O CA3 atua como um completador de padrões (*pattern completion*), permitindo prevenção de ruído e resgate de índices esparsos por conteúdo.
   
2. **Separação de Padrões (Giro Dentado)**:
   Antes, a projeção esparsa ia do `SparseEncoder` direto para o CA. Agora, introduzimos o **Giro Dentado (DG)** como etapa intermediária obrigatória de *Pattern Separation*. Ele ortogonaliza suavemente representações de alta similaridade textual para mitigar o esquecimento catastrófico sináptico, mantendo a sobreposição latente em uma faixa saudável de 20% a 30%.
   
3. **Escassez e Saturação Física**:
   Mapeamos os limites matemáticos do sistema. Com o limite crítico de Amit-Gutfreund-Sompolinsky ($P_c \approx 0.138 \cdot N$) aplicado a uma grade bidimensional de **24x24** ($N = 576$ neurônios), cada unidade CA3 suporta com segurança até $\approx 80$ memórias estáveis.
   Para contornar esse limite físico sem sofrer colapso de atração, o Perseus implementa **Depressão de Longo Prazo (LTD)** (decaimento temporal rápido dos pesos em CA3) e **Escalonamento Vertical Semântico** (replicação/spawning de novas instâncias de CA3 em paralelo formando *clusters* locais ao atingir 70% de saturação).

4. **Background Ativo e Proatividade (Vigília vs. Repouso)**:
   O sistema agora respira assincronamente. Durante a vigília (Fluxo Ativo), ele atua indexando e recuperando memórias. Durante o sono (Fluxo Passivo-Reflexivo), um Job de Background induz perturbação estocástica direcionada pelas conexões do grafo neocortical (**Modulação Alostérica**), coleta estados espúrios ricos que convergem em CA3, analisa a coerência deles via Perfil de Energia e Overlap, e traduz os insights válidos de volta para linguagem natural via **Un-embedding local por vizinhança KNN**, disparando ações proativas do LLM.

---

## 2. Nova Diretriz de Escopo Estrito (Fase 1: O MVP Episódico)

Para mitigar a complexidade e garantir a robustez matemática do motor, o desenvolvimento segue uma ordem rigorosa baseada em prioridades:

*   **Objetivo Exclusivo de Fase 1**: **Recuperação Episódica Pura** (Cenários Completos/Eventos indivisíveis estruturados em Sujeito-Verbo-Objeto).
*   **Restrição de Escopo**: A unidade `CA3HopfieldNetwork` é a **única responsável** por resgatar o episódio/evento completo no Neocórtex a partir de pistas parciais. Está **estritamente proibida** nesta fase qualquer lógica para lidar com propriedades puramente conceituais de termos isolados (Memória Semântica) ou correlações transversais de alto nível (Esquemas). 
*   **Fase 2 (Expansão Concorrente)**: Apenas após a estabilização física do motor episódico, abriremos espaço para instanciar subtipos paralelos e modulares de máquinas de Hopfield focadas em Memória Semântica (Atributos) e Esquemas de alto nível (mPFC).

---

## 3. Conceitos e Módulos a Serem Preservados da Versão Anterior

Para garantir um desenvolvimento incremental sem regressões, sugerimos a **manutenção e refatoração direta** dos seguintes componentes estáveis da arquitetura anterior:

*   **Segmentação de Eventos (EST)**: Mantemos a estrutura lógica de divisão de texto em eventos compostos por fragmentos direcionados. Refatoramos `Point` para atuar como as **Partes do Evento** (Átomos Semânticos) e `Event` como o container episódico de trajetórias.
*   **Algoritmo de Roteamento Neocortical Dinâmico**: A lógica contida em `Neocortex.route` baseada em similaridade de trajetória linear via **DTW (Dynamic Time Warping)** e limiar sigmoide $\tau(H)$ dinâmico (com base em entropia e escassez semântica) é conceitualmente brilhante e deve ser **totalmente mantida**. O que muda é que, após o roteamento até o `EventSchema` vencedor, em vez de ativar um autômato celular clássico, ativamos a **Unidade CA3** correspondente (ou seu cluster ativo).
*   **SparseEncoder**: O princípio de projeção ortogonal aleatória determinística e fixa via K-Winner-Takes-All (k-WTA) é mantido, mas ajustado para mapear de forma nativa a nova grade flat de $N=576$ ($24 \times 24$ células) no Giro Dentado.
*   **Estrutura de Grafos Neocorticais**: A conexão direcionada e sequencial entre os Points (sintagmas/partes de eventos) no Neocórtex continua sendo o esqueleto topográfico que orienta a Modulação Alostérica de background.

---

## 4. Mapeamento de Refatoração da Base de Código

Abaixo está o design de transição física de arquivos na árvore do projeto:

```
src/perseus/
│
├── neocortex/
│   ├── point.py              # Mantido ➔ Representa as "Partes do Evento" (Átomos Semânticos)
│   ├── event.py              # Mantido ➔ Container de trajetória, DTW e similaridade
│   ├── neocortex.py          # Mantido ➔ Roteador dinâmico de eventos via τ(H)
│   └── event_schema.py       # Modificado ➔ Passa a gerenciar um CA3Cluster em vez de um único CA
│
├── neural_nets/
│   └── ca3_hopfield.py       # Evoluído ➔ Herda o HopfieldNet 3D antigo e implementa 2D 24x24 (N=576), 
│                               LTD, overlap (m^μ) e perfil de energia individual ordenado.
│                               Focado estritamente na Recuperação Episódica MVP.
│
├── encoder/
│   ├── encoder.py            # Modificado ➔ Projeção estável ajustada para N=576 (24x24)
│   └── dentate_gyrus.py      # [NEW] ➔ Codificação esparsa suave para Pattern Separation (overlap 20%-30%)
│
└── background/
    ├── reflex_job.py         # [NEW] ➔ Execução assíncrona contínua do Job de Background
    ├── alosteric_mod.py      # [NEW] ➔ Modulador químico que perturba CA3 usando o grafo neocortical
    └── local_unembed.py      # [NEW] ➔ KNN local de decodificação reversa para proatividade agêntica
```

---

## 5. Plano de Ação e Tarefas de Implementação (Fase 1)

> [!NOTE]
> Este plano foi estruturado para que você (o idealizador humano) lidere e aprove as etapas de desenvolvimento, executando os alicerces e as principais engrenagens.

### Contexto A: Engenharia do Tecido Hipocampal (CA3 & Giro Dentado)
Foco em construir a matemática local e o controle de saturação das bacias de atração.

*   [ ] **Tarefa A1: Criação da `CA3HopfieldNetwork`**
    *   Implementar a rede de Hopfield 2D de tamanho rígido de $24 \times 24$ ($N = 576$ neurônios bipolares).
    *   Implementar método `overlap(state)` que retorna o vetor de sobreposição $m^\mu \in [-1, 1]$ para cada memória $\mu$ gravada.
    *   Implementar método `energy_profile(state)` que calcula $h_i = \sum W_{ij} s_j$, extrai a energia individual $E_i = -s_i h_i$, ordena os valores de forma crescente e descarta os índices espaciais para retornar a assinatura de atração pura.
    *   Implementar o mecanismo `grau_de_saturacao` ($\alpha = P/N$) e decaimento dinâmico de pesos (LTD).
    *   *Restrição MVP*: Garantir calibração estrita para representar o evento episódico atômico completo, ignorando termos ou conceitos soltos.
*   [ ] **Tarefa A2: Implementação do Giro Dentado (`DentateGyrus`)**
    *   Criar o filtro de esparsidade suave no pipeline do `SparseEncoder`.
    *   Definir regras de ativação e limiarização da matriz $24 \times 24$ para garantir que a similaridade latente de inputs próximos resulte em overlap físico estrito de 20% a 30% nas chaves binárias.

### Contexto B: Orquestração de Clusters e Roteamento
Foco em conectar a nova física de Hopfield ao fluxo cortical existente.

*   [ ] **Tarefa B1: Upgrade do `EventSchema` para Gerenciamento de Clusters**
    *   Refatorar `EventSchema` para substituir o antigo `EventModelAutomaton` (Brian's Brain CA) por uma lista de instâncias `CA3HopfieldNetwork`.
    *   Adicionar lógica de spawning: quando a unidade ativa do cluster atingir $\alpha \ge 0.70$, ela é congelada para leitura e uma nova unidade é instanciada para gravações.
    *   Implementar orquestração de busca paralela no cluster (Load Balancer cognitivo).
*   [ ] **Tarefa B2: Acoplamento do `Neocortex`**
    *   Garantir que a função `Neocortex.route(event)` continue calculando o DTW perfeitamente, mas redirecione o evento para ativação de gravação no cluster CA3 do schema vencedor.

### Contexto C: Dinâmica Subcognitiva de Background (Repouso)
Foco no processamento reflexivo contínuo, emergência de estados espúrios e decodificação.

*   [ ] **Tarefa C1: O Job Contínuo (`ReflexBackgroundJob`)**
    *   Criar o orquestrador assíncrono que varre continuamente os clusters de CA3 em busca de convergências em repouso.
    *   Implementar a triagem de estados espúrios: descartar ruído semântico térmico e validar estados de mesclagem coerentes ($0.3 \le m^\mu \le 0.6$ em múltiplos atratores) cuja curva de energia seja estatisticamente coerente com memórias estáveis reais.
*   [ ] **Tarefa C2: Modulação Alostérica**
    *   Codificar o injetor de ruído estocástico guiado pelas conexões assimétricas ($A \rightarrow B$) do grafo de Point connections do Neocórtex, empurrando as dinâmicas de repouso para as fronteiras de conceitos adjacentes.
*   [ ] **Tarefa C3: Decodificação Reversa (Un-embedding por Vizinhança)**
    *   Implementar o extrator KNN local que projeta a assinatura de atração esparsa validada contra a matriz neocortical da subárea correspondente.
    *   Recuperar o pool de tokens adjacentes e estruturar o payload que acorda a LLM para uma resposta proativa espontânea.

---

## 6. Diretrizes Finais para o Desenvolvedor Humano

1. **Validação In-Vitro Prioritária**: Recomenda-se começar adaptando os scripts experimentais da pasta `labs/` para a nova escala de $24 \times 24$ (com Giro Dentado e as funções de overlap/energia) antes de alterar a codebase nuclear (`src/perseus`). Isso dará segurança matemática de que a dinâmica de energia e o filtro de Pattern Separation estão calibrados de forma ideal.
2. **Descarte Limpo do Legado**: Mover os arquivos legados de CA para `src/deprecated/` apenas após o cluster CA3 estar 100% integrado ao fluxo de roteamento do `Neocortex`.
