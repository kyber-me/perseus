# Perseus Agent Guide

Este arquivo serve como ponto de entrada para assistentes de IA (como Antigravity) que trabalham no projeto Perseus.

## 📚 Documentação Principal

- [**Arquitetura**](docs/ARCHITECTURE.md): Definição teórica, dinâmica de autômatos, mecanismo de ressonância e metabolismo (LTP).
- [**Backlog**](docs/BACKLOG.md): Lista prioritária de tarefas e metas de implementação.
- [**Logs de Sessão**](docs/SESSION_LOG.md): Histórico completo de conversas e decisões de design.

## 🛠️ Guia de Desenvolvimento

- **Ambiente**: O projeto possui seu próprio `venv` dentro da pasta `perseus/`.
- **Módulos**: O código fonte reside em `src/perseus/`.
- **Configuração**: Use o `pyrightconfig.json` local para correta resolução de tipos e módulos.
- **Visualização**: O comando `perseus-viz` (ou rodar `automaton_viz.py`) permite visualizar o comportamento dos autômatos em tempo real.
- **Laboratórios de Validação**:
    - [**Semantic Experiments**](labs/semantic_experiments/): Estudo de contrastive centering e preservação métrica.
    - [**Hopfield Experiments**](labs/hopfield_experiments/): Testes de convergência, atração e estados espúrios em redes Hebbianas 3D.
    - [**Embedding Distribution**](labs/embedding_distribution/): Analisador de distribuição normal (Gauss) e outliers semânticos ($>3\sigma$).

## 🧠 Princípios de Codificação

1. **Simplicidade**: Mantenha o código enxuto e fiel aos conceitos biológicos/matemáticos sem abstrações desnecessárias.
2. **Modularidade**: O motor do autômato (`Automaton`) é separado da lógica de memória hipocampal (`HippocampalAutomaton`).
3. **Preservação de Contexto**: Sempre verifique as meta-diretrizes no topo do `ARCHITECTURE.md` antes de grandes alterações.

## 🤖 Skills Agênticas Locais (Suporte a Memória Agêntica)

Temos skills locais parametrizadas em `skills/` que guiam IAs a interagir com os experimentos:
- [**Semantic Granularity**](skills/semantic-granularity-experiment/SKILL.md): Executa estudos comparativos de granularidade semântica.
- [**Hopfield Experiment**](skills/hopfield-experiment/SKILL.md): Roda testes qualitativos sobre as bacias de atração do hipocampo.
- [**Embedding Distribution Analysis**](skills/embedding-distribution-analysis/SKILL.md): Analisa a normalidade estatística e mapeia picos (spikes) de coordenadas de embeddings.
