# Fundamentação Matemática das Métricas e Projeções Semânticas — Projeto Perseus
<!-- Guia Teórico-Prático de Preservação Métrica e Redução de Dimensionalidade -->

Este documento estabelece as bases matemáticas, aplicações práticas, prós e contras das métricas semânticas utilizadas no ecossistema **Perseus**, além de fundamentar teoricamente a decisão geométrica de manter o grid em **$27 \times 27$** para mapear embeddings densos de 768 dimensões.

---

## 1. O Teorema Clássico: O Lema de Johnson-Lindenstrauss (JL)

O "teorema clássico" que rege a preservação de distâncias sob redução de dimensionalidade é o **Lema de Johnson-Lindenstrauss (1984)**.

### O Enunciado Matemático
Dado um conjunto de pontos $V$ em um espaço euclidiano de alta dimensão, eles podem ser projetados em um espaço de dimensão muito menor $k$ sem que as distâncias euclidianas mútuas sofram uma distorção maior que um fator $\epsilon \in (0, 1)$.

Formalmente, para qualquer subconjunto de pontos $x, y \in V$, existe um mapeamento linear $f: \mathbb{R}^d \rightarrow \mathbb{R}^k$ tal que:

$$(1 - \epsilon) \|x - y\|^2 \le \|f(x) - f(y)\|^2 \le (1 + \epsilon) \|x - y\|^2$$

### O Papel das Projeções Ortogonais Aleatórias
A forma mais eficiente de realizar esse mapeamento $f$ é através de uma **Projeção Randômica Gaussiana** (multiplicar o vetor por uma matriz aleatória $M \in \mathbb{R}^{d \times k}$ cujos elementos são extraídos de uma distribuição normal $\mathcal{N}(0, 1/k)$).

No **Perseus**, refinamos essa técnica no `SparseEncoder` utilizando a **Ortogonalização por Decomposição QR** da matriz de projeção. Ao forçar que os eixos da matriz de projeção sejam ortogonais entre si, eliminamos correlações espúrias (pontos cegos) na projeção, espalhando uniformemente o sinal denso sobre o grid.

### A Geometria Quase 1-para-1 ($27 \times 27 = 729$ vs. $768$)
A dimensão nativa do nosso modelo de embedding denso é $d = 768$. Ao adotarmos o grid de **$27 \times 27$**, nossa dimensão de saída esparsa é $k = 729$.
*   **Taxa de Redução**: A taxa de dimensão retida é de $\frac{729}{768} \approx 94.9\%$.
*   **Mínima Distorção ($\epsilon \to 0$)**: Como $k \approx d$, o mapeamento linear opera quase como uma **rotação rígida pura** no espaço de Hilbert. A distorção métrica introduzida pela projeção é virtualmente nula, permitindo que a topologia semântica original seja preservada com fidelidade quase perfeita antes de aplicarmos a binarização.

---

## 2. As Métricas Semânticas: Teoria e Prática

Abaixo, detalhamos cada uma das métricas utilizadas e avaliadas no projeto.

### 2.1. Similaridade de Cosseno ($\text{Sim}_{\cos}$)
Mede a proximidade angular entre dois vetores densos, independentemente de suas magnitudes.

#### A Fórmula
$$\text{Sim}_{\cos}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\| \|\vec{v}\|}$$

*   **Aplicação no Perseus**: É a métrica padrão do espaço contínuo. É computada pelo `SemanticEmbedder` e serve como entrada primária para o roteamento do `Neocortex` (via DTW).
*   **Prós**: Altamente robusta para capturar nuances e sutilezas semânticas extraídas pelo modelo de linguagem transformador profundo (BGE).
*   **Contras**: Elevado custo computacional se calculado de forma bruta em lote no ciclo principal de agentes móveis (requer operações de ponto flutuante em alta dimensão $O(d)$).

---

### 2.2. Distância de Hamming clássica vs. SDR Overlap Ratio
A distância de Hamming clássica conta o número de posições nas quais dois vetores diferem.

#### O Problema da Escassez (SDRs)
Em representações esparsas distribuídas (**SDR**), onde a ativação é restrita a uma fração pequena (ex: $15\%$ das células ativas), a grande maioria do grid é composta por zeros ($85\%$ inativos). A distância de Hamming clássica é severamente distorcida pelo "acordo passivo de silêncio" (dois vetores que compartilham apenas zeros parecerão falsamente semelhantes).

#### A Solução: SDR Overlap Ratio
Para mitigar isso, definimos a métrica de sobreposição ativa. Sejam $A$ e $B$ os conjuntos de índices das células ativas (valor $= 1$) nos grids projetados $\mathbf{s}_a$ e $\mathbf{s}_b$, e $K$ o número fixo de células ativas por projeção ($K = N \times \text{densidade}$):

$$\text{Sim}_{\text{SDR}}(\mathbf{s}_a, \mathbf{s}_b) = \frac{|A \cap B|}{K}$$

*   **Aplicação no Perseus**: É o sinal de gatilho para a **Unidade CA3 Hipocampal**. Quando a intersecção ativa é alta, a dinâmica de atratores converge rapidamente para recuperar o engrama correto.
*   **Prós**: Operação binária extremamente rápida ($O(K)$ onde $K \ll N$), mimetizando perfeitamente a ativação de sinapses coincidentes no hipocampo biológico.
*   **Contras**: Introduz descontinuidade matemática (por conta do limiar de ativação K-WTA), transformando pequenas variações contínuas em saltos discretos de overlap.

---

### 2.3. Coeficientes de Correlação: Pearson vs. Spearman
Usados para calibrar o alinhamento métrico entre o espaço denso (Cosseno) e o esparso (SDR Overlap).

#### A. Correlação de Pearson ($r$)
Mede o grau de relação **linear** estrita entre duas variáveis quantitativas.
$$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$
*   **No Perseus**: Avalia se a sobreposição esparsa acompanha proporcionalmente a similaridade de cosseno de forma linear.

#### B. Correlação de Spearman ($\rho$)
Mede a relação **monótona** (preservação de postos/ranks) entre duas variáveis. É baseada na diferença de posições ordenadas e não nos valores absolutos.
$$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
*   **No Perseus**: É a métrica mais realista. Devido ao caráter de limiar não linear da binarização (Top-K), não exigimos linearidade matemática perfeita, mas sim **consistência de ordenação**: se a frase A é mais próxima de B do que de C no espaço denso, a projeção de A deve sobrepor-se mais com B do que com C no espaço esparso.

---

## 3. Referências de Estudo Recomendadas

Para aprofundar o entendimento matemático e neurobiológico dos conceitos apresentados:

### A. Redução de Dimensionalidade e o Lema de Johnson-Lindenstrauss
1.  **Dasgupta, S., & Gupta, A. (2003).** *An elementary proof of a theorem of Johnson and Lindenstrauss.* Random Structures & Algorithms, 22(1), 60-65.
    *   *Por que ler*: A demonstração mais didática e acessível do Lema de JL, explicando por que projeções em subespaços aleatórios preservam distâncias métricas.
2.  **Bingham, E., & Mannila, H. (2001).** *Random projection in dimensionality reduction: applications to image and text data.* KDD '01.
    *   *Por que ler*: Demonstra a viabilidade prática de projeções aleatórias aplicadas a dados textuais e embeddings de alta dimensionalidade.

### B. Teoria de Sparse Distributed Representations (SDR) e Computação Neuromórfica
3.  **Hawkins, J., & Ahmad, S. (2016).** *Why neurons have thousands of synapses, a theory of sequence memory in neocortex.* Frontiers in Neural Circuits, 10, 23.
    *   *Por que ler*: Fundamenta por que o cérebro utiliza codificação extremamente esparsa (SDR) para gerenciar capacidade de armazenamento e evitar colapso de interferência de padrões.

### C. Neurobiologia do Giro Dentado (Pattern Separation)
4.  **Treves, A., & Rolls, E. T. (1992).** *Computational analysis of the role of the hippocampus in memory.* Hippocampus, 2(2), 189-199.
    *   *Por que ler*: O paper clássico que modela computacionalmente o Giro Dentado como um separador de padrões (*pattern separation*) esparso que prepara memórias para o armazenamento no sistema CA3 recorrente.
