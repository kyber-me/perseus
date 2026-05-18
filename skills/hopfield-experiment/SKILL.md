---
name: hopfield-experiment
description: Executa o pipeline de recuperação semântica in-vitro na HopfieldNet do Perseus, injetando ruído e recuperando memórias 3D, com saída em JSON.
---

# Skill: Hopfield Semantic Retrieval Pipeline

## Quando usar esta Skill (Triggers)
Ative esta skill sempre que o usuário solicitar para "rodar um experimento hopfield", "testar evocação de memória", "injetar um conceito", ou "rodar o pipeline de memória do Perseus". O usuário não precisa fornecer especificações técnicas exaustivas; você (o agente) deve orquestrar a execução.

## Instruções de Execução

1. **Localizar o Runner Automático**:
   O motor de execução de experimentos está localizado em: `labs/hopfield_experiments/hopfield_runner.py`.
   A classe `HopfieldExperimentSkill` contida lá é responsável por criar o ambiente In-Vitro, consolidar memórias, aplicar ruídos, extrair a matriz da HopfieldNet e exportar automaticamente as métricas de similaridade em um relatório `.json`.

2. **Coletar ou Deduzir Parâmetros**:
   Se o usuário der um comando vago (ex: "rode um teste com ruído"), invente um cenário criativo e semanticamente rico para o experimento.
   Você precisa definir:
   - **Nome do Experimento**: Um título legível e sem espaços.
   - **Fatos Base (Memórias)**: Pelo menos 3 frases densas/fatos distintos.
   - **Fato de Teste (Cue)**: Pode ser a corrupção de um dos fatos base (para testar atratores) ou um "Conceito Alienígena" (para testar estados espúrios).
   - **Ruído (Noise Level)**: Float entre `0.0` e `0.50` (sugestão: `0.20`).
   
3. **Executar o Experimento**:
   Crie um script `python` curto (pode ser na pasta `scratch/` ou um temporário) que importa `HopfieldExperimentSkill`, instancia a classe, passa seus parâmetros para `run_semantic_retrieval()` e imprime o caminho do JSON salvo.
   Execute esse script via bash.

4. **Analisar a Saída JSON**:
   O runner salvará um relatório na pasta `labs/results/`. 
   Use sua ferramenta de leitura de arquivos para acessar o JSON gerado.

5. **Apresentar o Relatório**:
   Não imprima o JSON bruto. Faça uma síntese de inteligência analítica baseada no JSON:
   - Se ocorreu uma `PERFECT_RECOVERY` (Atrator salvou a memória do ruído).
   - Se ocorreu um `SPURIOUS_BLEND` / `ATTRACTED` (A máquina confabulou ou misturou memórias).
   - Forneça uma reflexão rápida sobre o porquê daquilo ter acontecido com base na entropia matemática da rede.
