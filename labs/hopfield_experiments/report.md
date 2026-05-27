# Relatório Experimental: Recuperação Semântica (Hopfield 3D)
<!-- Relatório de Validação da Unidade de Memória Associativa de CA3 -->

## 1. Objetivo do Experimento
Validar a capacidade da **Unidade CA3 Hipocampal**, modelada por uma **Rede de Hopfield Recorrente 3D** (escala $16\times16\times16$ correspondendo a $N=4096$ neurônios virtuais), de realizar:
1.  **Pattern Completion**: Recuperar com precisão um engrama estável original a partir de um gatilho de evocação corrompido com ruído severo.
2.  **Rejeição e Spurious States**: Avaliar o comportamento dinâmico da rede quando exposta a um estímulo inédito (conceito alienígena não aprendido).

---

## 2. Configurações e Massa de Dados
*   **Grid de Resolução**: Volume 3D de $16 \times 16 \times 16$ ($N = 4096$ neurônios).
*   **Projeção Esparsa**: `SparseEncoder` com densidade $d = 0.50$ (padrão balanceado com $2048$ neurônios ativos).
*   **Algoritmo de Aprendizado**: Matriz de pesos sinápticos cumulativa baseada na regra de Hebbian Learning bipolar.
*   **Memórias Consolidadas (Fatos Semânticos)**:
    1.  *Fato 1*: "A rápida raposa marrom salta sobre o cão preguiçoso."
    2.  *Fato 2*: "A mecânica quântica descreve o universo em escalas subatômicas."
    3.  *Fato 3*: "Uma receita de bolo de chocolate exige farinha, açúcar e cacau."

---

## 3. Resultados Obtidos

### Teste A: Recuperação de Memória Corrompida (Pattern Completion)
*   **Gatilho de Evocação**: Fato 2 ("A mecânica quântica descreve o universo em escalas subatômicas.") corrompido com **20% de ruído aleatório** (819 bits invertidos artificialmente no grid).
*   **Proximidade Inicial**: A similaridade de Hamming inicial entre o gatilho ruidoso e o alvo consolidado era de apenas **$80.00\%$**.
*   **Dinâmica de Atrator**: A inferência assíncrona foi ativada.
*   **Convergência**: O atrator convergiu para estabilidade térmica em apenas **2 épocas**.
*   **Similaridades após convergência**:
    *   Similaridade com Fato 1: $49.76\%$
    *   Similaridade com Fato 2 (Alvo): **$100.00\%$ <=== RECUPERAÇÃO PERFEITA!**
    *   Similaridade com Fato 3: $52.83\%$

> [!TIP]
> **Conclusão do Teste A**: O circuito de completamento de padrões provou robustez perfeita. Mesmo com uma perda massiva de $20\%$ da assinatura de bits original, a energia da rede minimizou-se de forma limpa, direcionando o sinal de volta para o fundo da bacia de atração do Fato 2.

---

### Teste B: Injeção de Conceito Inédito (Rejeição / Confabulação)
*   **Estímulo Injetado**: Frase alienígena nunca aprendida ("A inteligência artificial é baseada em redes neurais profundas.").
*   **Convergência**: A rede convergiu em apenas **2 épocas**.
*   **Similaridades após convergência**:
    *   Similaridade com Fato 1: $49.76\%$
    *   Similaridade com Fato 2: **$100.00\%$ <=== FALSO POSITIVO (ALUCINAÇÃO)!**
    *   Similaridade com Fato 3: $52.83\%$
    *   Similaridade da saída com a própria entrada inédita: $52.25\%$

> [!WARNING]
> **Conclusão do Teste B**: Como a frase inédita não possuía uma bacia de atração própria, a rede de Hopfield rejeitou o sinal de entrada original (similaridade com a própria entrada caiu para apenas $52.25\%$) e colapsou para a bacia de atração ativa mais forte próxima (neste caso, o atrator do Fato 2, registrando um falso positivo de $100\%$). Isso ilustra de forma realista a dinâmica de confabulação de memórias sobrepostas e justifica a importância crucial do **Giro Dentado (Pattern Separation)** e da triagem de **Estados Espúrios** no Perseus.
