# Como o Perseus Funciona

> Uma explicação acessível do pipeline de memória episódica — sem fórmulas, sem código.

---

## A ideia central

O Perseus é um sistema de memória inspirado no funcionamento do cérebro humano. Ele não apenas armazena informações — ele **aprende a organizá-las**, agrupando experiências parecidas e separando as distintas, exatamente como fazemos naturalmente.

Para entender como ele faz isso, pense na seguinte analogia:

> Imagine que você está ouvindo uma história. Seu cérebro não grava a história palavra por palavra — ele extrai os **momentos significativos**, entende a **progressão** entre eles, e depois verifica: *"já vivi algo assim antes?"*. Se sim, conecta à memória existente. Se não, abre uma gaveta nova.

O Perseus faz exatamente isso. Só que com texto, embeddings e autômatos celulares.

---

## O pipeline passo a passo

### 1. O texto chega → ele é quebrado em sintagmas

Um sintagma é a menor unidade de sentido — um fragmento de frase com significado próprio. Por exemplo:

> *"O paciente chegou ao hospital, foi triado pela enfermeira e recebeu o diagnóstico."*

Vira três sintagmas:
- *"O paciente chegou ao hospital"*
- *"foi triado pela enfermeira"*
- *"recebeu o diagnóstico"*

Cada sintagma é transformado num vetor matemático (embedding) — um ponto num espaço de centenas de dimensões onde **proximidade = semelhança semântica**. Esse vetor + o texto original formam um **`Point`**.

---

### 2. Os Points são conectados → nasce um Event

Os sintagmas não existem isoladamente. Eles formam uma **sequência com direção**: a história começa em algum lugar e caminha para algum outro. Essa sequência é um **`Event`**.

Um `Event` não é apenas uma lista de sintagmas — ele captura:

- **Trajetória**: para onde a história "caminhou" no espaço semântico (do primeiro ao último sintagma).
- **Magnitude**: o quão longa foi essa jornada semântica.
- **Embedding holístico**: uma representação do evento como um todo (não apenas das partes).
- **Seed**: uma "impressão digital" binária 16×16 usada para ativar o autômato celular.

Pense no `Event` como uma **memória episódica completa** — não um fato isolado, mas uma experiência com começo, meio e fim.

---

### 3. O Event busca um "irmão" no Neocórtex

Quando um novo `Event` chega, o **Neocórtex** (o orquestrador central) pergunta:

> *"Algum evento que já conhecemos tem uma trajetória parecida com essa?"*

Para responder, ele compara o novo evento com **todos os eventos já armazenados** nos schemas existentes, usando o algoritmo **DTW (Dynamic Time Warping)**.

O DTW não olha apenas para o início e o fim da trajetória — ele compara o **caminho inteiro**, sintagma por sintagma. Dois eventos que começam e terminam no mesmo lugar, mas passam por lugares completamente diferentes no meio, recebem scores distintos.

O evento existente mais similar é o "irmão candidato". Se o score de similaridade ultrapassar o **limiar τ**, o novo evento é absorvido pelo mesmo schema. Se não, nasce um schema novo.

---

### 4. O limiar τ cresce com a experiência

O τ não é fixo. Ele segue uma **curva sigmoide** inversamente proporcional à entropia do sistema:

| Fase do sistema | Comportamento |
|---|---|
| **Infância** (poucos schemas) | τ baixo — aceita correlações fracas. *A criança acha que o balão pode voar.* |
| **Crescimento** (entropia caindo) | τ sobe rapidamente — o sistema aprende a discriminar. |
| **Maturidade** (muitos schemas) | τ alto — só aceita como "irmão" quem é realmente parecido. |

Isso replica o fenômeno de **escassez como semântica**: quando há pouca informação disponível, qualquer associação vale. Conforme o repertório cresce, o sistema fica mais criterioso.

---

### 5. O Event é absorvido por um Schema

Um **`EventSchema`** é um padrão emergente — ele não é criado antes dos eventos, ele **nasce deles**.

Quando um schema absorve um novo evento:
- O evento é marcado com o UUID do schema (`schema_id`).
- O autômato celular do schema é ativado com a seed do evento (modo *High-Res Active*).
- O centroid do schema é atualizado (média dos embeddings — útil para visualização).
- O campo `concept` do schema pode ser atualizado por uma LLM, que tenta descrever em linguagem natural o que aquele schema "representa".

Com o tempo, um schema rico em eventos começa a ter uma identidade semântica emergente — não definida por uma regra, mas construída pela experiência.

---

### 6. O autômato celular: a memória viva

Cada schema possui um **`EventModelAutomaton`** — um autômato celular (inspirado no Jogo da Vida de Conway) que evolui tick a tick.

Quando um evento chega, ele **ativa** o autômato com sua seed (High-Res Active). Quando o sistema está em repouso, o autômato opera em modo **Passive Reflexive** — evoluindo por inércia, sem estímulo externo.

A memória de um evento é "evocada" quando o padrão do autômato em repouso se aproxima da seed original. Isso é detectado pela **distância de Hamming** — quanto mais bits em comum, mais forte a ressonância.

---

### 7. Ressonância episódica: memórias que emergem sozinhas

Um `Event` tem um **quorum** — a fração mínima de seus Points que precisa ressoar simultaneamente nos autômatos para que a memória seja "surfaceada".

> Com `resonance_threshold = 0.35` e 5 sintagmas, o quorum é **2 de 5**.

Se dois ou mais sintagmas de um evento antigo ressoarem ao mesmo tempo (dentro de uma janela temporal), o sistema "lembra" daquele evento — sem que ninguém tenha pedido.

Esse é o análogo computacional do **Default Mode Network** biológico: o cérebro em repouso revivendo experiências passadas de forma espontânea.

---

## Resumo do fluxo

```
Texto de entrada
    │
    ▼
Segmentação em sintagmas (LLM)
    │
    ▼
Point (texto + embedding)  ×N
    │
    ▼
Event (sequência de Points + seed + trajetória)
    │
    ▼
Neocortex.route(event)
    │
    ├─ DTW similarity contra todos os events nos schemas
    │
    ├─ score ≥ τ(H)?  ──SIM──▶  EventSchema.absorb(event)
    │                             └─ autômato ativado (HIGH_RES_ACTIVE)
    │                             └─ centroid atualizado
    │                             └─ concept evolui (LLM)
    │
    └─ score < τ(H)?  ──NÃO──▶  Novo EventSchema criado
                                  └─ absorve o evento inaugural
```

---

## Referências técnicas

Para os detalhes matemáticos, consulte [`ARCHITECTURE.md`](./ARCHITECTURE.md).
Para o backlog e próximos passos, consulte [`BACKLOG.md`](./BACKLOG.md).
