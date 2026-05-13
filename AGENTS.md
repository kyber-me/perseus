# Perseus Agent Guide

Este arquivo serve como ponto de entrada para assistentes de IA (como Antigravity) que trabalham no projeto Perseus.

## 📚 Documentação Principal

- [**Arquitetura**](docs/ARCHITECTURE.md): Definição teórica, dinâmica de autômatos, mecanismo de ressonância e metabolismo (LTP).
- [**Backlog**](docs/BACKLOG.md): Lista prioritária de tarefas e metas de implementação.

## 🛠️ Guia de Desenvolvimento

- **Ambiente**: O projeto possui seu próprio `venv` dentro da pasta `perseus/`.
- **Módulos**: O código fonte reside em `src/perseus/`.
- **Configuração**: Use o `pyrightconfig.json` local para correta resolução de tipos e módulos.
- **Visualização**: O comando `perseus-viz` (ou rodar `automaton_viz.py`) permite visualizar o comportamento dos autômatos em tempo real.

## 🧠 Princípios de Codificação

1. **Simplicidade**: Mantenha o código enxuto e fiel aos conceitos biológicos/matemáticos sem abstrações desnecessárias.
2. **Modularidade**: O motor do autômato (`Automaton`) é separado da lógica de memória hipocampal (`HippocampalAutomaton`).
3. **Preservação de Contexto**: Sempre verifique as meta-diretrizes no topo do `ARCHITECTURE.md` antes de grandes alterações.
