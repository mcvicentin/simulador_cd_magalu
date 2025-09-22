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
git clone https://github.com/mcvicentin/simulador_cd_magalu.git
cd simulador_cd_magalu

```
### 2. Instalar dependências
Crie um ambiente virtual (recomendado) e instale as dependências:

```bash
pip install -r requirements.txt

```
### 3. Executar simulador

**📓 No Jupyter Notebook**
Abra o **`run_simulation.ipynb`** e use os sliders para variar parâmetros (**`n_entregas`** e **`custo_km`**).
O notebook gera automaticamente:
  - Custos totais Recife vs Salvador
  - Diferença mensal e economia percentual
  - Gráfico comparativo de custos
  - Diferença acumulada (até 24 meses)

**💻 No terminal**
Rode o script de linha de comando:

```bash
python run_simulation.py
```

O programa perguntará:

  - Número total de entregas por mês
  - Custo médio por km
  - Custos fixos de aluguel (usar default ou inserir manualmente)

Exemplo de saída:

```bash
Custo Recife:   R$ 17,705,000
Custo Salvador: R$ 25,295,000

Diferença mensal (Salvador - Recife): R$ 7,590,000
Economia percentual ao escolher Recife: 30.01%
```

**📁 Reprodutibilidade**

  - O arquivo simulador_CD_magalu.ipynb contém todo o pipeline para reconstruir o dataset (cidades_ne150k.csv) do zero, caso seja necessário.
  - Para uso direto do simulador, basta o CSV (cidades_ne150k.csv) já processado.
