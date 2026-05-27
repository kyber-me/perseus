---
name: embedding-distribution-analysis
description: Analisa a distribuição de probabilidade Gaussiana de embeddings BGE e extrai componentes de alto sinal (outliers semânticos fora dos limites sigma).
---

# Skill: Embedding Probability Distribution & Outlier Extraction

## Quando usar esta Skill (Triggers)
Ative esta skill sempre que o usuário solicitar para:
- "analisar a distribuição de probabilidade do embedding"
- "verificar a normalidade gaussiana de uma frase"
- "extrair os spikes/outliers de alto sinal do embedding"
- "identificar as dimensões de maior carga semântica"
- "rodar o laboratório de distribuição gaussiana"

## Instruções de Execução

### 1. Coletar ou Deduzir Parâmetros
O analisador aceita dois modos de entrada. Defina com base no comando do usuário:
*   **Modo Frase Customizada**: Se o usuário fornecer um texto customizado (ex: "rode para 'The quantum cat is alive'"), use o parâmetro `--sentence` / `-s`.
*   **Modo Index de Benchmark**: Se o usuário quiser testar uma das sentenças padrão do nosso benchmark clássico, use o índice correspondente ($0$ a $24$) no parâmetro `--index` / `-i`.
*   **Plotagem Gráfica**: Para gerar a imagem PNG científica com o histograma de Gauss, adicione o parâmetro `--plot` / `-p`.

### 2. Executar o Script
Execute o analisador no ambiente virtual do repositório:
```bash
# Exemplo 1: Frase customizada com gráfico
venv/bin/python labs/embedding_distribution/distribution_analyzer.py --sentence "My custom sentence." --plot

# Exemplo 2: Sentença do benchmark pelo índice
venv/bin/python labs/embedding_distribution/distribution_analyzer.py --index 12 --plot
```

### 3. Ler e Analisar o JSON de Saída
O script salvará o relatório estruturado e a imagem do gráfico em uma subpasta específica por data e hora dentro de:
`labs/embedding_distribution/results/Experimento_Distribuicao_.../` (ex: `labs/embedding_distribution/results/Experimento_Distribuicao_27_Maio_2026_16h43m24s/distribution_report.json`)

Abra este JSON e extraia os dados críticos para sua resposta:
*   **Estatísticas Gerais**: Média ($\mu$) e Desvio Padrão ($\sigma$).
*   **Testes de Normalidade**: O percentual real nas faixas de $1\sigma, 2\sigma, 3\sigma$ comparado ao ideal teórico.
*   **Componentes de Alto Sinal**: Mapeamento dos *outliers* semânticos sob a chave `"high_signal_components"`:
    *   **Caudas Extremas ($>3\sigma$)**: Identifique o índice da dimensão e o desvio absoluto (ex: *Dimensão 308 com desvio de $6.58\sigma$*).
    *   **Transição ($2\sigma$ a $3\sigma$)**: Verifique o número de dimensões nessa faixa que carregam os marcadores secundários.

### 4. Apresentar os Resultados
*   Apresente as métricas sigma e as conformidades de desvio de forma tabular limpa.
*   Liste os componentes de alto sinal mapeados de forma ordenada, explicando o significado cognitivo dessas dimensões como os "marcadores semânticos de alta intensidade" (spikes) da frase.
*   Se a plotagem gráfica foi ativada, informe ao usuário que a imagem em alta resolução `sentence_distribution.png` foi gerada na mesma pasta específica do experimento.
