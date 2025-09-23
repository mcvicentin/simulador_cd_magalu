import pandas as pd
import numpy as np

# ====================================================
# Configurações fixas do CD (RB Investimentos 2025)
# ====================================================
cd_area_m2 = 10_000
preco_m2_recife   = 20.5   # R$/m²
preco_m2_salvador = 29.5   # R$/m²
custo_fix_recife_default   = cd_area_m2 * preco_m2_recife
custo_fix_salvador_default = cd_area_m2 * preco_m2_salvador

# ====================================================
# Carregar tabela das cidades do NE >150k habitantes
# (arquivo já processado com distâncias via ORS)
# ====================================================
df = pd.read_csv("cidades_ne150k.csv")  
# precisa ter: municipio, uf, populacao, dist_recife_km, dist_salvador_km

total_pop = df["populacao"].sum()
km_intra_urbano = 15  # fixo

def simular_para_origem(df_cidades, origem_nome, coluna_dist_km, custo_fixo_origem,
                        n_entregas, custo_km, km_intra_urbano):
    df_sim = df_cidades.copy()
    df_sim["entregas"] = n_entregas * (df_sim["populacao"] / total_pop)

    df_sim["dist_ajustada_km"] = np.where(
        df_sim["municipio"].str.lower() == origem_nome.lower(),
        km_intra_urbano,
        df_sim[coluna_dist_km]
    )

    df_sim["custo_logistico"] = df_sim["entregas"] * df_sim["dist_ajustada_km"] * custo_km

    custo_log_total = df_sim["custo_logistico"].sum()
    custo_total = custo_log_total + custo_fixo_origem

    # arredondar entregas e formatar custo
    df_sim["entregas"] = df_sim["entregas"].round().astype(int)
    df_sim["dist_ajustada_km"] = df_sim["dist_ajustada_km"].round(1)
    df_sim["custo_logistico"] = df_sim["custo_logistico"].round(0)

    resumo = {
        "origem": origem_nome,
        "custo_logistico": custo_log_total,
        "custo_fixo_imobiliario": custo_fixo_origem,
        "custo_total": custo_total
    }

    return resumo, df_sim[["municipio","uf","populacao","entregas","dist_ajustada_km","custo_logistico"]]


def main():
    print("=== Simulador de CD Nordeste (Magalu) ===\n")

    # Entradas do usuário
    n_entregas = int(input("Número total de entregas por mês: "))
    custo_km = float(input("Custo médio por km (R$): "))

    print("\n--- Custos de aluguel ---")
    print("Você pode usar os valores default (RB Investimentos, 2025) ou inserir manualmente.")
    print(f"Recife default:   R$ {custo_fix_recife_default:,.0f}/mês")
    print(f"Salvador default: R$ {custo_fix_salvador_default:,.0f}/mês")
    
    usar_default = input("\nUsar valores default de aluguel? (s/n): ").strip().lower()

    if usar_default == "n":
        custo_fix_recife = float(input("Informe custo fixo mensal de aluguel em Recife (R$): "))
        custo_fix_salvador = float(input("Informe custo fixo mensal de aluguel em Salvador (R$): "))
    else:
        custo_fix_recife = custo_fix_recife_default
        custo_fix_salvador = custo_fix_salvador_default

    # Rodar simulações
    res_rec, det_rec = simular_para_origem(
        df, "Recife", "dist_recife_km", custo_fix_recife,
        n_entregas, custo_km, km_intra_urbano
    )
    res_sal, det_sal = simular_para_origem(
        df, "Salvador", "dist_salvador_km", custo_fix_salvador,
        n_entregas, custo_km, km_intra_urbano
    )

    # Resultados principais
    custo_recife = res_rec["custo_total"]
    custo_salvador = res_sal["custo_total"]
    diff_mensal = custo_salvador - custo_recife
    economia_pct = (diff_mensal / custo_salvador) * 100

    print("\n--- Resumo ---")
    print(f"Custo Recife:   R$ {custo_recife:,.0f}")
    print(f"Custo Salvador: R$ {custo_salvador:,.0f}")
    print(f"\nDiferença mensal (Salvador - Recife): R$ {diff_mensal:,.0f}")
    print(f"Economia percentual ao escolher Recife: {economia_pct:.2f}%")
    print(f"\nObs.: km_intra_urbano fixado em {km_intra_urbano} km para a cidade da origem.")

    # Mostrar detalhamento Recife
    print("\n--- Detalhamento (Recife como origem) ---")
    det_rec_fmt = det_rec.copy()
    det_rec_fmt["custo_logistico"] = det_rec_fmt["custo_logistico"].apply(lambda x: f"R$ {x:,.0f}")
    print(det_rec_fmt.head(10).to_string(index=False))

    # Mostrar detalhamento Salvador
    print("\n--- Detalhamento (Salvador como origem) ---")
    det_sal_fmt = det_sal.copy()
    det_sal_fmt["custo_logistico"] = det_sal_fmt["custo_logistico"].apply(lambda x: f"R$ {x:,.0f}")
    print(det_sal_fmt.head(10).to_string(index=False))

    print("\nArquivos detalhados salvos como 'detalhamento_recife.csv' e 'detalhamento_salvador.csv'.")

if __name__ == "__main__":
    main()
