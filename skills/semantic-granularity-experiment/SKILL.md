---
name: semantic-granularity-experiment
description: Executa o benchmark temático de granularidade semântica de 25 frases (Raw vs Centered BGE) e gera uma interpretação qualitativa dinâmica na raiz de results/report.md.
---

# Skill: Semantic Granularity Experiment & Dynamic Analysis Ledger

## Quando usar esta Skill (Triggers)
Ative esta skill sempre que o usuário solicitar para:
- "rodar o experimento semântico"
- "testar a separação de temas"
- "verificar a preservação métrica com centramento"
- "atualizar o relatório de granularidade"
- "analisar o efeito cone ou isotropização"

## Instruções de Execução

### 1. Localizar e Executar o Runner
Execute o script do laboratório de granularidade no ambiente virtual do projeto:
```bash
venv/bin/python labs/semantic_experiments/granularity_runner.py
```
Isso gerará os vetores densos (BGE Inglês nativo `BAAI/bge-base-en-v1.5`), projetará nos grids esparsos de $27 \times 27$ ($N=729$) sob uma densidade de $15\%$, calculará as similaridades para todos os 300 pares e salvará as métricas brutas em:
`labs/semantic_experiments/results/Experimento_Tematico_[Data]_[Hora]/theme_granularity_report.json`

### 2. Ler e Analisar o Relatório JSON
Acesse o arquivo JSON gerado no passo anterior e extraia os resumos chave:
*   `average_intra_theme_cosine` e `average_intra_theme_sdr_overlap` para Raw e Centered.
*   `average_inter_theme_cosine` e `average_inter_theme_sdr_overlap` para Raw e Centered.
*   Calcule a **razão de contraste físico ativo** (Overlap Intra-Tema / Overlap Inter-Tema) para ambos.

### 3. Redigir Análise Dinâmica e de Tempo Real
Não utilize um template engessado ou respostas automáticas repetitivas. Você deve escrever uma **análise analítica e reflexão cognitiva real** baseada no resultado empírico:
*   Explique as diferenças de agrupamento semântico denso (Cosseno).
*   Aborde o comportamento físico sináptico (SDR Overlap) em relação ao piso de ruído teórico (que é de exactamente $15.00\%$ para grids com densidade de $15\%$).
*   Destaque os benefícios do **Centramento Semântico (Contrastive Centering)** na neutralização do "efeito cone" do transformer.

### 4. Atualizar o Livro de Registro Central (report.md)
Escreva ou apenda a sua análise formatada em Markdown na raiz de `labs/semantic_experiments/results/report.md`:
*   Se o arquivo não existir, crie-o com a estrutura inicial de cabeçalho.
*   Se o arquivo já existir, **apenda** cronologicamente a nova análise, de forma que o histórico anterior seja inteiramente preservado (ledger cumulativo).
*   Utilize o formato:
    ```markdown
    ## 📅 Experimento: [Data e Hora do JSON] (BGE Inglês Nativo - Cru vs Centrado)
    *   **Embedder**: `BAAI/bge-base-en-v1.5` (768D) | **Grid**: 27x27 (15% densidade)
    *   [Métricas em tabela comparativa]
    *   [Sua interpretação cognitiva em tempo real]
    ```
