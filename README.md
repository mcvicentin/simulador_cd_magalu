# simulador_cd_magalu

# Simulador de Localização de Centro de Distribuição (Magalu)

Este repositório apresenta um estudo de caso para apoiar a decisão de abertura de um novo **Centro de Distribuição (CD)** no Nordeste, comparando as cidades de **Recife (PE)** e **Salvador (BA)**.

O objetivo é avaliar **custos logísticos e imobiliários**, considerando:
- Custos de aluguel de galpões (referência: RB Investimentos, 2025);
- Custos logísticos baseados em distâncias rodoviárias reais (OpenRouteService + OSM);
- Demanda de entregas ponderada pela população de cidades do Nordeste com mais de 150 mil habitantes (Censo IBGE 2025).

---

## 📂 Estrutura dos arquivos

- **`simulador_CD_magalu.ipynb`**  
  Notebook principal com todo o pipeline:
  - Extração e tratamento da base populacional;
  - Seleção de cidades >150k hab no Nordeste;
  - Geocodificação e cálculo de distâncias rodoviárias Recife/Salvador → cidades;
  - Geração de tabelas e análises comparativas;
  - Construção do dataset final (`cidades_ne150k.csv`).

- **`cidades_ne150k.csv`**  
  Dataset final usado nas simulações. Contém colunas:
  - `municipio, uf, populacao, dist_recife_km, dist_salvador_km`.

- **`run_simulation.ipynb`**  
  Notebook simplificado e interativo (com `ipywidgets`):
  - Permite variar `n_entregas` e `custo_km` com sliders;
  - Mostra custos totais Recife vs Salvador;
  - Gera gráficos de comparação e payback acumulado (24 meses).

- **`run_simulation.py`**  
  Script em Python para uso via linha de comando:
  - Pergunta parâmetros diretamente no terminal;
  - Retorna os resultados formatados (custos, diferença mensal e economia percentual).

---

## ▶️ Como usar

### 1. Clonar o repositório
```bash
git clone https://github.com/usuario/magalu-simulador-cd.git
cd magalu-simulador-cd
