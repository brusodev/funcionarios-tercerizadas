# 📱 Projeto Celulares Recebidos - Análise de Inventário

**Data:** Outubro 2025  
**Total:** 33.215 aparelhos celulares  
**Valor Total:** R$ 30.241.453,50  
**Recintos:** 5 (Bauru, Ipiranga, Araraquara, Viracopos, São José do Rio Preto)

## 📁 Estrutura do Projeto

```
celulares-recebidos/
├── data/
│   ├── source/           # Dados originais (PDFs, Excel)
│   ├── processed/        # Dados processados finais (JSONs, CSVs)
│   └── temp/            # Arquivos temporários de análise
├── scripts/
│   ├── analysis/        # Scripts de análise e debug
│   ├── extraction/      # Scripts de extração de dados
│   └── validation/      # Scripts de validação e comparação
├── web/                 # Interface web (pesquisador_modelos.html)
├── docs/
│   ├── guides/          # Guias de uso (ABRA_PRIMEIRO.txt, etc.)
│   └── reports/         # Relatórios finais e documentação
├── templates/           # Templates ODT
└── .venv/              # Ambiente virtual Python
```

## 🚀 Como Usar

### Interface Web (Recomendado)
1. Abra `web/pesquisador_modelos.html` no navegador
2. Use as 3 abas: Busca por modelo, Por ADM, Top 20
3. Funciona offline, sem servidor necessário

### Dados Processados
- `data/processed/MEGA_JSON_MODELOS_COMPLETO.json` - Dados completos
- `data/processed/MEGA_JSON_MODELOS_SIMPLIFICADO.json` - Dados simplificados
- `data/processed/RELATORIO_FINAL_33215.csv` - Aparelhos por PDF
- `data/processed/RELATORIO_POR_RECINTO_FINAL_VALIDADO.csv` - Distribuição por recinto

### Documentação
- `docs/guides/ABRA_PRIMEIRO.txt` - Guia rápido
- `docs/guides/GUIA_PESQUISADOR_HTML.txt` - Guia completo da interface web
- `docs/reports/RELATORIO_ARQUIVOS_GERADOS.txt` - Inventário completo

## 📊 Estatísticas Finais

| Recinto | Aparelhos | % |
|---------|-----------|---|
| Bauru | 17.592 | 52.96% |
| Ipiranga | 9.392 | 28.28% |
| Araraquara | 4.965 | 14.95% |
| Viracopos | 665 | 2.00% |
| São José do Rio Preto | 601 | 1.81% |

**Modelos únicos:** 8.220  
**ADMs processados:** 15 (0733-0747)  
**Validação:** 100% ✅

## 🛠️ Scripts Disponíveis

### Análise
- Scripts em `scripts/analysis/` para investigar dados específicos

### Extração
- Scripts em `scripts/extraction/` para processar PDFs e gerar relatórios

### Validação
- Scripts em `scripts/validation/` para verificar consistência dos dados

## 📋 Requisitos

- Python 3.13.7+
- Bibliotecas: PyPDF2, openpyxl, json, csv, re, collections
- Navegador moderno (Chrome 60+, Firefox 55+, etc.)

## 🔍 Validações Realizadas

✅ **Quantidade total:** 33.215 aparelhos confirmados  
✅ **Distribuição por recinto:** Validada linha por linha  
✅ **Valor total:** R$ 30.241.453,50 (100% match)  
✅ **Modelos únicos:** 8.220 catalogados  
✅ **Conversão KG:** 0.49kg = 1 aparelho (Blackberry 9900)

---

**Projeto finalizado em:** Outubro 2025  
**Status:** ✅ COMPLETO E VALIDADO