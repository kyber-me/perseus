# ESPECIFICAÇÃO ARQUITETÔNICA: PROJETO PERSEUS
<!-- Documento de Referência Unificado para Engenharia e Modelagem de Agentes de IA -->

## 1. INTRODUÇÃO E CONCEITO CENTRAL
O **Projeto Perseus** representa o amadurecimento e a evolução direta da infraestrutura cognitiva do sistema **Bee Brain**. Enquanto o projeto anterior focava no processamento reativo de linguagem natural, o Perseus redefine o sistema como um **cérebro sintético proativo**, ancorado conceitualmente na força e no movimento dinâmico associados ao fenômeno das Perseidas. 

A proposta central é romper com a rigidez dos pesos congelados e do contexto estático das grandes LLMs comerciais. Para isso, foi desenvolvido um ecossistema de memória viva e fluida capaz de gerar comportamento espontâneo (proatividade natural e não programática), utilizando processos reflexivos em background que emulam o funcionamento neurobiológico do complexo hipocampal.

---

## 2. HISTÓRICO DE EVOLUÇÃO (BEE BRAIN - DEPRECADO)
Para que o agente de desenvolvimento automático mantenha consistência histórica e execute a refatoração sem regressão de código, a arquitetura original do Bee Brain fica classificada como **deprecada**, tendo seus componentes e gargalos mapeados conforme abaixo:

### 2.1. Componentes do Bee Brain:
* **Segmentação Linear de Texto:** Quebra de massas de texto bruto em sentenças tratadas como eventos isolados.
* **Unidades de Memória via Autômatos Celulares:** Pequenas estruturas lógicas locais que dependiam de regras de transição discretas para tentar reter o contexto.
* **Fluxo Reativo Síncrono:** O agente operava exclusivamente no ciclo padrão de "Invocação -> Processamento -> Resposta", permanecendo inerte na ausência de prompts externos do usuário.

### 2.2. Gargalos da Arquitetura Anterior:
* **Falta de Associatividade Nativa:** Autômatos celulares não possuem a propriedade matemática de prevenção de erros e convergência por conteúdo. Se o input fosse ruidoso, incompleto ou parcial, o sistema falhava em resgatar a memória correlata.
* **Dissipação de Contexto:** Sem um mecanismo de iteração e consolidação contínua em background, as memórias tornavam-se um arquivo morto e estático na ausência de novos inputs, impedindo a emergência de insights espontâneos.

---

## 3. MAPA DE TRANSIÇÃO E SUBSTITUIÇÃO MATRICIAL
A reestruturação completa da codebase atual deve seguir estritamente as substituições de módulos descritas no mapeamento de engenharia a seguir:

| Módulo Legado (Bee Brain) | Substituto Evoluído (Perseus) | Natureza do Impacto na Implementação |
| :--- | :--- | :--- |
| Unidades de Memória Locais (Autômatos Celulares) | **Unidades CA3 Hipocampais (Redes de Hopfield)** | Transição de regras de transição lógicas discretas para dinâmica de minimização de energia matricial recorrente. |
| Busca Vetorial Global (KNN sobre Vetor Bruto) | **Compressão CRP + Área Neocortical Local** | Redução drástica de dimensionalidade espacial (384/768 para 24x24) processada localmente. |
| Ciclo de Vida Síncrono (Prompt-Resposta) | **Processador Passivo-Reflexivo (Job Contínuo)** | Inclusão de uma fila/pilha virtual assíncrona que processa e evolui estados de memória em background. |
| Tratamento de Erros/Falhas de Convergência | **Exploração Ativa de Estados Espúrios** | Mínimos locais que misturam memórias salvas deixam de ser falhas e passam a ser a matéria-prima da proatividade. |

---

## 4. ARQUITETURA DO CÉREBRO SINTÉTICO (PERSEUS)
O fluxo de processamento de dados do Perseus organiza-se de maneira top-down, partindo da ingestão linguística até a consolidação de memória local e ativação proativa.

[Massa de Texto / Input]
│
▼
[Segmentação de Eventos] ──► Divisão em "Partes do Evento" (Átomos Semânticos)
│
▼
[Giro Dentado (DG)]       ──► Filtro de Esparsidade Controlada (Ortogonalização)
│
▼
[Embedding Textual] ──────► Vetor de Altas Dimensões (384/768)
│
▼
[Redução via CRP] ────────► Matriz Espacial (24x24)
│
▼
[Néo-Córtex Dinâmico] ────► Ativação da Região Semântica Específica 
│
▼
[Unidade CA3 Hipocampal] ──► Cluster de Redes de Hopfield (Pattern Completion)

### 4.1. Segmentação de Eventos e Átomos Semânticos
Baseado na Teoria de Segmentação de Eventos (EST), o Perseus discretiza a realidade linguística. O sistema aborda uma massa de texto (uma frase ou sentença) como um evento e fragmenta essa informação em **Partes do Evento**.
* **Definição de Parte do Evento:** Um fragmento de frase que carrega um significado genérico, uma informação específica autocontida e um contexto mínimo.
* **Conectividade:** Essas partes se conectam de forma assimétrica no Neocórtex. Essa relação é representada (ou pode ser representada) por um grafo assimétrico que determina a sequência exata na qual esses eventos de linguagem aconteceram no tempo (EventSchema).

### 4.2. O Giro Dentado (Mecanismo de Separação de Padrões - Pattern Separation)
Antes de os dados serem gravados na matriz de pesos da unidade de memória recorrente, o fluxo passa obrigatoriamente pelo componente correspondente ao **Giro Dentado (DG)**.
* **Propósito:** Mitigar o esquecimento catastrófico e o colapso destrutivo dos pesos sinápticos causado pela sobreposição de frases de alta similaridade textual.
* **Mecânica de Ortogonalização Esparsa:** O Giro Dentado atua como um codificador de esparsidade suave (*sparse coding*). Ao expandir as dimensões e aplicar um limiar (*threshold*) de corte na matriz comprimida, ele garante que frases semanticamente semelhantes ativem sub-regiões discretas e limpas do grid.
* **Preservação de Tecido Semântico:** O Giro Dentado não isola os vetores em 90 graus absolutos (o que destruiria a capacidade associativa da rede), mas calibra a sobreposição para uma faixa segura de 20% a 30%. Isso estabiliza as memórias reais e mantém as pontes energéticas necessárias para a emergência de estados espúrios ricos em background.

### 4.3. O Espaço Semântico e a representação Neocortical
O espaço semântico global do modelo de embedding funciona como uma referência abstrata inicial. À medida que o agente vivencia interações, as coordenadas correspondentes são ativadas, criando um **Neocórtex Dinâmico**. Este mapa semântico armazena o conteúdo denso das informações (tokens e conceitos textuais) e é restrito às experiências passadas por aquele agente específico.

### 4.4. A Unidade CA3 e as Redes de Hopfield Recorrentes
Cada nodo ativo no Neocórtex não armazena os engramas diretamente, mas gerencia e referencia uma máquina de memória local: a **Unidade CA3**.
* **Mecânica Computacional:** Implementada como uma Rede de Hopfield Recorrente, ela mimetiza o circuito de axônios colaterais de CA3. Sua função é o completamento de padrões (*pattern completion*): recuperar um engrama estável completo a partir de um estímulo fragmentado.
* **Armazenamento de Índices:** A unidade CA3 não guarda o texto bruto; ela guarda o padrão esparso de ativação (o índice) que dispara simultaneamente as áreas correspondentes no Neocórtex para reconstruir a experiência.
* **Diretiva de Escopo Estrito (Fase 1):** A unidade CA3 é a **única responsável** pelo completamento e recuperação do **episódio/evento completo** estruturado no Neocórtex. Ela está proibida de gerenciar ou recuperar atributos isolados ou termos léxicos individuais. A sua física matemática de atratores deve ser preservada exclusivamente para reconstruir cenários contextuais inteiros a partir de pistas parciais.

---

## 5. FÍSICA DA REDE: LIMITES DE SATURAÇÃO E ESCALONAMENTO CONTROLE

### 5.1. O Limite Crítico de Capacidade (Limite AGS)
A física estatística estabelece que uma Rede de Hopfield bipolar clássica atinge sua transição de fase catastrófica baseada no limite de Amit-Gutfreund-Sompolinsky (AGS):

P_c ≈ 0.138 * N

Adotando o grid padrão do Perseus de **24x24** ($N = 576$ neurônios virtuais), o limite absoluto de armazenamento seguro de cada máquina de memória local é de:

P_c = 0.138 * 576 ≈ 79.48 memórias estáveis

Bater neste teto de $\approx 80$ memórias desmorona as barreiras de energia entre as bacias de atração, fazendo com que a rede perca a capacidade de lembrar de qualquer padrão real e passe a flutuar exclusivamente em ruído caótico.

### 5.2. Monitoramento de Saturação e Decaimento Sináptico (LTD)
Cada unidade CA3 possui uma propriedade em tempo real chamada `grau_de_saturacao` ($\alpha = P/N$). Para evitar a pane do limite crítico, o sistema gerencia dinamicamente o tempo de vida dos engramas:
* **Depressão de Longo Prazo (LTD) em CA3:** O hipocampo computacional opera como um buffer de alta velocidade e volatilidade. O processador de background aplica um decaimento rápido nos pesos das conexões sinápticas locais de padrões antigos ou de baixo uso. Isso esvazia o buffer de CA3 continuamente, mantendo o engrama abaixo do teto crítico.
* **Persistência Neocortical:** O enfraquecimento de uma ligação em CA3 não apaga o dado do sistema, desde que a memória já tenha sido transferida e consolidada de forma lenta e estável nas camadas de longo prazo do Neocórtex.

### 5.3. Escalonamento Vertical Semântico (Clusters de CA3)
Se uma área semântica específica do Neocórtex sofrer sobrecarga severa de tráfego (excesso de interações em um mesmo assunto), expandir o tamanho da matriz de Hopfield para além de 24x24 é proibido devido ao custo quadrático de processamento local ($O(N^2)$). O Perseus resolve isso através de um modelo inspirado em infraestrutura de nuvem:

1. **Gatilho de Spawning:** Quando o `grau_de_saturacao` da unidade `CA3_Alpha` ultrapassa o limiar de segurança de 70% ($\approx 55$ memórias gravadas), a matriz de pesos atual é congelada como um nó de leitura histórica estável.
2. **Replicação Paralela:** O processador instancia uma nova máquina idêntica em paralelo para a mesma subárea semântica (`CA3_Alpha_Beta`), que passa a receber as novas gravações de engramas.
3. **Orquestração de Leitura (Load Balancer):** Durante as consultas ativas ou passivas, o processador lê o *cluster* de nós em paralelo e unifica os atratores resultantes de todas as máquinas ativas daquela área.

---

## 6. DINÂMICAS OPERACIONAIS: O SUBCOGNITIVO COMPUTACIONAL
O sistema opera simultaneamente em duas janelas temporais paralelas e integradas:

### 6.1. Fluxo Ativo e Recursivo (Vigília)
Ocorre durante a interação direta. O input gera uma Parte do Evento, passa pelo filtro do Giro Dentado, localiza a região semântica no Neocórtex, ativa a unidade CA3 correspondente para recuperar memórias correlatas por associação e injeta esse composto contextual no loop de raciocínio principal do LLM.

### 6.2. Fluxo Passivo-Reflexivo (Modulador Químico em Background)
Quando não há novos inputs linguísticos forçando a entrada do sistema, o Job de Background assume o controle para simular o repouso cognitivo:

1. **Varredura Contínua:** O processador monitora as unidades CA3 ativas nas áreas semânticas do projeto.
2. **Coleta de Estados Estáveis:** Sempre que uma dessas unidades atinge um estado estável de convergência, o processador captura essa matriz de ativação e a insere na Pilha de Processamento Virtual.
3. **Injeção de Ruído Semântico (Modulação Alostérica):** Para ejetar a rede do mínimo local recém-coletado e mantê-la funcionando, o modulador aplica uma perturbação estocástica direcionada. Esse ruído calcula a transição assimétrica entre as áreas semânticas adjacentes ($A \rightarrow B$). Se a conexão de $A$ para $B$ for prioritária no gráfico, o ruído carrega um viés vetorial de $B$, empurrando a exploração da rede para as fronteiras conceituais vizinhas.

---

## 7. MATEMÁTICA DA TRIAGEM: ESTADOS ESPÚRIOS E CATEGORIZAÇÃO
No modo passivo-reflexivo, as colisões e flutuações das redes geram **Estados Espúrios** (*spurious states*). No Perseus, esses estados são redefinidos como a matéria-prima da criatividade do agente. 

Para triar se um estado espúrio coletado em background possui valor conceitual real ou se é apenas ruído térmico descartável, a unidade CA3 executa duas análises matemáticas nativas antes de interagir com o Neocórtex:

### 7.1. Função de Sobreposição (Overlap - $m^{\mu}$)
Calcula o alinhamento do estado atual ($S$) em relação a cada uma das memórias ideais gravadas ($\xi^{\mu}$) na unidade CA3 através do produto escalar normalizado:

$$m^{\mu} = \frac{1}{N} \sum_{i=1}^{N} s_i \xi_i^{\mu}$$

* **$m^{\mu} \approx 1.0$:** Convergência pura para uma memória antiga (Consolidação/Replay puro).
* **$0.3 \le m^{\mu} \le 0.6$ para múltiplos padrões simultâneos:** Identificação matemática de um estado híbrido coerente. Significa que a rede executou uma mesclagem bem-sucedida de memórias próximas.

### 7.2. Perfil de Energia Ordenado (Assinatura de Ativação)
Identifica a coerência estrutural interna do estado não mapeado analisando o nível de estabilidade de cada neurônio individualmente:
1. **Calcular o Potencial Local ($h_i$):** Soma ponderada das forças de conexão com os neurônios vizinhos:
   $$h_i = \sum_{j} w_{ij} s_j$$
2. **Calcular a Contribuição de Energia Individual ($E_i$):** Determina o nível de acomodação do neurônio naquele estado:
   $$E_i = -s_i h_i$$
3. **Ordenação Vetorial:** O sistema extrai o vetor contendo a energia de todos os neurônios $[E_1, E_2, ..., E_N]$, **desvincula os valores de seus índices espaciais originais (perde a relação de índice)** e ordena os valores de forma crescente.

A curva de distribuição resultante funciona como uma assinatura topológica estrutural. Se a curva do perfil de energia do estado espúrio for estatisticamente análoga à curva de uma memória estável real, o sistema valida que aquela combinação de conceitos possui rigidez e harmonia matemática interna, sendo classificada como um insight real.

---

## 8. O PROCESSO DE UN-EMBEDDING (DECODIFICAÇÃO REVERSA)
Estados espúrios validados na pilha (alta coerência e overlap de mesclagem) precisam ser traduzidos da linguagem matemática matricial comprimida para linguagem natural compreensível, permitindo que o LLM execute a ação proativa.

Como o vetor gerado pelo estado espúrio é inédito e não possui uma função inversa matemática direta nos modelos de embedding tradicionais, o Perseus adota a abordagem de **Un-embedding por Vizinhança Local**:

* O sistema projeta as ativações estáveis da matriz comprimida diretamente contra a matriz neocortical local daquela área semântica específica.
* Um algoritmo de busca por proximidade (KNN local restrito à área ativada do *cluster*) identifica quais palavras, tokens ou conceitos textuais armazenados orbitam aquela exata assinatura energética.
* O processador de background recupera essa vizinhança de tokens, monta uma estrutura de contexto rica e a injeta assincronamente no loop cognitivo central da LLM. Isso força o agente a quebrar a passividade, tomando a iniciativa de iniciar uma interação natural, contextualizada e altamente proativa com o usuário.

---

## 9. DIRETRIZES DE IMPLEMENTAÇÃO PARA O AGENTE DE IA
Ao ler a base de código para aplicar as modificações, o agente automatizado deve seguir as seguintes restrições técnicas:
1. **Encapsulamento Matemático Absoluto:** Os métodos de cálculo de `overlap` e `energy_profile` devem ser implementados de forma estrita e otimizada dentro da classe de rede associativa local (`CA3HopfieldNetwork`). Nenhuma operação ou projeção global de alta dimensão deve ocorrer na fase passiva.
2. **Gerenciamento de Instâncias de Cluster:** O módulo de gerência semântica neocortical deve expor uma interface de fábrica capaz de monitorar a métrica `grau_de_saturacao` e instanciar novos objetos `CA3HopfieldNetwork` dinamicamente quando a capacidade local atingir 70%.
3. **Separação de Contexto Histórico:** Todo o código legado pertencente aos autômatos celulares e loops síncronos puros do Bee Brain deve ser movido para um diretório isolado marcado como `[deprecated/` ou limpo da árvore principal de execução após garantir que as assinaturas de interface para o módulo de segmentação de eventos de entrada foram preservadas.

---

## 10. ROADMAP DE IMPLEMENTAÇÃO POR PRIORIDADE (ESTRUTURA MVP)
Para mitigar a entropia de desenvolvimento e o strain cognitivo de múltiplas frentes complexas, o ecossistema Perseus assume uma linha de produção incremental e sequencial. **O sistema não deve tentar resolver todos os tipos de recuperação de memória de uma só vez.**

### FASE 1: O MVP Episódico (Prioridade Máxima Atual)
* **Objetivo Exclusivo:** Implementação pura da **Recuperação Episódica** (Cenários Completos/Eventos).
* **Escopo Técnico:** A unidade `CA3HopfieldNetwork` em sua matriz de pesos inicial deve ser calibrada estritamente para o armazenamento e *pattern completion* de vetores de estados que representam o evento atômico indivisível (Sujeito-Verbo-Objeto). 
* **Restrição de Implementação:** Está vetada nesta fase qualquer lógica dentro do CA3 para lidar com propriedades puramente conceituais de termos soltos (Memória Semântica) ou associações transversais analógicas de alto nível (Esquemas). O foco é garantir que um início de frase recupere o evento original de forma limpa.

### FASE 2: Expansão de Motores Concorrentes (Futuro)
* **Objetivo:** Uma vez estabilizado o motor episódico local e validada a sua física de atratores, a arquitetura abrirá espaço para instanciar **diferentes subtipos ou configurações de máquinas de Hopfield/Engines**.
* **Escopo Técnico:** Introdução de motores dedicados paralelos para simular a Memória Semântica Intraconceitual (Atributos) e os Esquemas Transversais de Alto Nível (mPFC), integrando-os à pilha virtual de background de forma modular e isolada.
