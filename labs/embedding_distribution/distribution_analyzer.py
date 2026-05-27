import os
import sys
import json
import datetime
import argparse
import numpy as np

# Ajustar os paths para que imports funcionem corretamente de forma independente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from embedding.semantic_embedder import SemanticEmbedder
from labs.semantic_experiments.granularity_runner import BENCHMARK_DATASET

# Aplanar o dataset de 25 frases para permitir seleção simples por índice
BENCHMARK_SENTENCES = []
for theme, sentences in BENCHMARK_DATASET.items():
    BENCHMARK_SENTENCES.extend(sentences)

def main():
    parser = argparse.ArgumentParser(
        description="Estudo de Distribuição de Probabilidade Gaussiana em Embeddings do Perseus."
    )
    parser.add_argument(
        "--sentence", "-s",
        type=str,
        help="Frase customizada a ser analisada estatisticamente."
    )
    parser.add_argument(
        "--index", "-i",
        type=int,
        help="Índice (0 a 24) da frase a selecionar do benchmark de 25 frases."
    )
    parser.add_argument(
        "--plot", "-p",
        action="store_true",
        help="Gera e salva um gráfico científico de alta fidelidade em formato PNG."
    )
    
    args = parser.parse_args()
    
    # Validação e seleção da frase
    text = ""
    if args.sentence:
        text = args.sentence
        print(f"[*] Analisando frase customizada inserida por CLI:")
    elif args.index is not None:
        if args.index < 0 or args.index >= len(BENCHMARK_SENTENCES):
            print(f"[!] Erro: índice {args.index} fora dos limites (deve ser entre 0 e {len(BENCHMARK_SENTENCES)-1}).")
            sys.exit(1)
        text = BENCHMARK_SENTENCES[args.index]
        print(f"[*] Analisando frase selecionada do benchmark (Índice {args.index}):")
    else:
        # Default: primeira frase do benchmark
        text = BENCHMARK_SENTENCES[0]
        print(f"[*] Nenhum parâmetro fornecido. Analisando frase padrão (Índice 0 do benchmark):")
        
    print(f"  > \"{text}\"\n")
    
    # Inicialização do Embedder e geração do embedding
    print("[*] Carregando SemanticEmbedder (BAAI/bge-base-en-v1.5)...")
    embedder = SemanticEmbedder(input_dim=768)
    
    emb = embedder.embed(text)
    print(f"[+] Embedding gerado com sucesso! Shape: {emb.shape} | Norma (L2): {np.linalg.norm(emb):.4f}\n")
    
    # --- 1. CÁLCULO DAS ESTATÍSTICAS BÁSICAS ---
    mean_val = float(np.mean(emb))
    std_val = float(np.std(emb))
    min_val = float(np.min(emb))
    max_val = float(np.max(emb))
    
    # --- 2. CÁLCULO DAS CONTAGENS SIGMA (TESTE DE NORMALIDADE) ---
    # Limite 1 Sigma [-1σ, +1σ]
    inside_1sig = np.sum((emb >= mean_val - std_val) & (emb <= mean_val + std_val))
    pct_1sig = float(inside_1sig / len(emb))
    
    # Limite 2 Sigma [-2σ, +2σ]
    inside_2sig = np.sum((emb >= mean_val - 2 * std_val) & (emb <= mean_val + 2 * std_val))
    pct_2sig = float(inside_2sig / len(emb))
    
    # Limite 3 Sigma [-3σ, +3σ]
    inside_3sig = np.sum((emb >= mean_val - 3 * std_val) & (emb <= mean_val + 3 * std_val))
    pct_3sig = float(inside_3sig / len(emb))
    
    # --- 3. EXTRAÇÃO DOS COMPONENTES DE ALTO SINAL (CAUDAS DE GAUSS) ---
    # Caudas Extremas (> 3σ)
    tail_indices = np.where(np.abs(emb - mean_val) > 3 * std_val)[0]
    tails_list = []
    for idx in tail_indices:
        tails_list.append({
            "dimension_index": int(idx),
            "value": float(emb[idx]),
            "deviation_sigmas": float(np.abs(emb[idx] - mean_val) / std_val)
        })
    tails_list = sorted(tails_list, key=lambda x: x["deviation_sigmas"], reverse=True)
    
    # Zona de Transição (entre 2σ e 3σ)
    trans_indices = np.where((np.abs(emb - mean_val) > 2 * std_val) & (np.abs(emb - mean_val) <= 3 * std_val))[0]
    trans_list = []
    for idx in trans_indices:
        trans_list.append({
            "dimension_index": int(idx),
            "value": float(emb[idx]),
            "deviation_sigmas": float(np.abs(emb[idx] - mean_val) / std_val)
        })
    trans_list = sorted(trans_list, key=lambda x: x["deviation_sigmas"], reverse=True)
    
    # --- 4. EXIBIÇÃO EM TABELA NO TERMINAL ---
    print("="*75)
    print("🔬 ANÁLISE DE PROBABILIDADE DA DISTRIBUIÇÃO DO EMBEDDING (768D)")
    print("="*75)
    print(f"  - Média Aritmética (μ)        : {mean_val:+.6f}  (Teórico Gaussiano: ~0.000000)")
    print(f"  - Desvio Padrão Real (σ)      : {std_val:.6f}   (Teórico Gaussiano: 0.036084)")
    print(f"  - Amplitude dos Extremos      : [{min_val:+.6f} a {max_val:+.6f}]")
    print("-"*75)
    print("  FAIXAS SIGMA (DISTRIBUIÇÃO EMPÍRICA VS TEÓRICA DE GAUSS):")
    print("-"*75)
    
    def print_sigma_row(label, count, pct, theoretical):
        deviation = pct - theoretical
        print(f"  * {label:<12} : {count:>4} / 768 | Real: {pct:.2%} | Teórico: {theoretical:.2%} | Desvio: {deviation:+.2%}")
        
    print_sigma_row("1 Sigma (1σ)", inside_1sig, pct_1sig, 0.6827)
    print_sigma_row("2 Sigma (2σ)", inside_2sig, pct_2sig, 0.9545)
    print_sigma_row("3 Sigma (3σ)", inside_3sig, pct_3sig, 0.9973)
    
    print("-"*75)
    print("🎯 COMPONENTES DE ALTO SINAL MAPEADOS (OUTLIERS SEMÂNTICOS)")
    print("-"*75)
    print(f"  * CAUDA EXTREMA (Desvio > 3σ) [Total: {len(tails_list)}]:")
    for item in tails_list:
        print(f"    - Dimensão {item['dimension_index']:>3} : Valor {item['value']:+.6f} | Desvio: {item['deviation_sigmas']:.2f}σ")
        
    print(f"\n  * ZONA DE TRANSIÇÃO (2σ a 3σ) [Total: {len(trans_list)}]:")
    for item in trans_list[:15]:
        print(f"    - Dimensão {item['dimension_index']:>3} : Valor {item['value']:+.6f} | Desvio: {item['deviation_sigmas']:.2f}σ")
    if len(trans_list) > 15:
        print(f"    ... e mais {len(trans_list) - 15} dimensões registradas no JSON de relatório.")
    print("="*75)
    
    # --- 5. SALVAMENTO DO RELATÓRIO JSON ---
    report_data = {
        "sentence": text,
        "dimensions": len(emb),
        "statistics": {
            "mean": round(mean_val, 6),
            "std_dev": round(std_val, 6),
            "min": round(min_val, 6),
            "max": round(max_val, 6)
        },
        "normality_check": {
            "one_sigma": {
                "empirical_count": int(inside_1sig),
                "empirical_percentage": round(pct_1sig, 4),
                "theoretical_percentage": 0.6827,
                "deviation": round(pct_1sig - 0.6827, 4)
            },
            "two_sigma": {
                "empirical_count": int(inside_2sig),
                "empirical_percentage": round(pct_2sig, 4),
                "theoretical_percentage": 0.9545,
                "deviation": round(pct_2sig - 0.9545, 4)
            },
            "three_sigma": {
                "empirical_count": int(inside_3sig),
                "empirical_percentage": round(pct_3sig, 4),
                "theoretical_percentage": 0.9973,
                "deviation": round(pct_3sig - 0.9973, 4)
            }
        },
        "high_signal_components": {
            "extreme_tails_above_3sigma": tails_list,
            "transition_zone_2sigma_to_3sigma": trans_list
        }
    }
    
    # Geração dinâmica do nome da pasta específica por data e hora
    pt_months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    now = datetime.datetime.now()
    folder_name = f"Experimento_Distribuicao_{now.day}_{pt_months[now.month-1]}_{now.year}_{now.strftime('%Hh%Mm%Ss')}"
    
    results_dir = os.path.join(os.path.dirname(__file__), "results", folder_name)
    os.makedirs(results_dir, exist_ok=True)
    
    report_filepath = os.path.join(results_dir, "distribution_report.json")
    with open(report_filepath, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)
        
    print(f"[+] Relatório em formato JSON salvo com sucesso em:\n    {report_filepath}\n")

    # --- 6. GERAÇÃO DO GRÁFICO CIENTÍFICO PNG (MATPLOTLIB) ---
    if args.plot:
        print("[*] Renderizando gráfico de alta fidelidade...")
        try:
            import matplotlib.pyplot as plt
            
            # Configuração estética premium (Dark Mode editorial)
            plt.style.use('dark_background')
            plt.rcParams['figure.facecolor'] = '#0c0c0e'
            plt.rcParams['axes.facecolor'] = '#121216'
            plt.rcParams['text.color'] = '#c8c8c8'
            plt.rcParams['axes.labelcolor'] = '#c8c8c8'
            plt.rcParams['xtick.color'] = '#8c8c90'
            plt.rcParams['ytick.color'] = '#8c8c90'
            plt.rcParams['grid.color'] = '#25252a'
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Histograma empírico real (Neon Magenta)
            count, bins, ignored = ax.hist(
                emb, 
                bins=40, 
                density=True, 
                alpha=0.55, 
                color='#ff0096', 
                edgecolor='#1c1c22', 
                label='Frequência Empírica (768D)'
            )
            
            # Curva teórica Gaussiana (Neon Cyan)
            x_curve = np.linspace(mean_val - 4 * std_val, mean_val + 4 * std_val, 500)
            y_curve = (1 / (std_val * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_curve - mean_val) / std_val) ** 2)
            ax.plot(x_curve, y_curve, color='#00ffc8', linewidth=2.5, label='Curva PDF de Gauss')
            
            # Linhas verticais para os limites Sigma
            ax.axvline(mean_val, color='#8c8c90', linestyle='--', alpha=0.7, label='Média (μ)')
            
            ax.axvline(mean_val - std_val, color='#e0c832', linestyle=':', alpha=0.8)
            ax.axvline(mean_val + std_val, color='#e0c832', linestyle=':', alpha=0.8, label='Limites 1σ')
            
            ax.axvline(mean_val - 2 * std_val, color='#ff6c00', linestyle=':', alpha=0.8)
            ax.axvline(mean_val + 2 * std_val, color='#ff6c00', linestyle=':', alpha=0.8, label='Limites 2σ')
            
            ax.axvline(mean_val - 3 * std_val, color='#ff003c', linestyle=':', alpha=0.8)
            ax.axvline(mean_val + 3 * std_val, color='#ff003c', linestyle=':', alpha=0.8, label='Limites 3σ')
            
            # Ajustar limites do eixo X para focar no conteúdo principal
            ax.set_xlim(mean_val - 4 * std_val, mean_val + 4 * std_val)
            
            # Título e Legendas
            displayed_text = f"\"{text[:55]}...\"" if len(text) > 55 else f"\"{text}\""
            ax.set_title(f"Distribuição de Coordenadas do Embedding - BGE (768D)\n{displayed_text}", fontsize=11, fontweight='bold', pad=15)
            ax.set_xlabel("Valor da Coordenada na Dimensão", fontsize=10, labelpad=10)
            ax.set_ylabel("Densidade de Probabilidade", fontsize=10, labelpad=10)
            
            # Adicionar caixa de texto com estatísticas e percentuais
            stats_text = (
                f"Estatísticas:\n"
                f" μ = {mean_val:+.6f}\n"
                f" σ = {std_val:.6f}\n"
                f" Min/Max = [{min_val:+.4f} a {max_val:+.4f}]\n\n"
                f"Distribuição Real vs Teórica:\n"
                f" 1σ: {pct_1sig:.2%} (Real) vs 68.27% (Teo)\n"
                f" 2σ: {pct_2sig:.2%} (Real) vs 95.45% (Teo)\n"
                f" 3σ: {pct_3sig:.2%} (Real) vs 99.73% (Teo)"
            )
            props = dict(boxstyle='round,pad=0.5', facecolor='#16161c', edgecolor='#ff0096', alpha=0.95)
            ax.text(
                0.97, 0.95, 
                stats_text, 
                transform=ax.transAxes, 
                fontsize=8, 
                fontfamily='monospace',
                verticalalignment='top', 
                horizontalalignment='right', 
                bbox=props
            )
            
            ax.legend(loc='upper left', frameon=True, facecolor='#16161c', edgecolor='#25252a', fontsize=8)
            ax.grid(True, linestyle=':', alpha=0.5)
            
            # Salvar o gráfico em alta resolução
            plot_filepath = os.path.join(results_dir, "sentence_distribution.png")
            plt.savefig(plot_filepath, dpi=180, bbox_inches='tight', facecolor='#0c0c0e')
            plt.close()
            print(f"[+] Gráfico científico de alta resolução salvo em:\n    {plot_filepath}\n")
            
        except ImportError:
            print("[!] Erro: não foi possível carregar o matplotlib para geração gráfica.")

if __name__ == "__main__":
    main()
