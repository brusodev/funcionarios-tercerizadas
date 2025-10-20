# Template de Organização de Serviços Terceirizados

Este template foi criado para organizar e gerenciar informações sobre serviços terceirizados em diferentes áreas de atuação.

## 📋 Áreas de Atuação Suportadas

1. **Manutenção de Prédios** - Serviços de manutenção predial corretiva e preventiva
2. **Serviço de Copa** - Serviços de copa e cozinha nos prédios  
3. **Segurança e Controle de Acesso** - Serviços de segurança patrimonial
4. **Transporte** - Serviços de transporte e motoristas

## 🗂️ Estrutura de Dados

Cada planilha deve conter as seguintes colunas:
- `nº`: Número sequencial do funcionário
- `nome`: Nome completo do funcionário
- `tipo_manutecao`: Descrição do tipo de serviço prestado
- `locais`: Locais de atuação (separados por "/")

## 🚀 Como Usar

### 1. Executar o Template Principal
```bash
python template_servicos.py
```

### 2. Usar como Módulo Python
```python
from template_servicos import TemplateServicos

# Criar instância
template = TemplateServicos()

# Carregar dados
template.carregar_todos_dados()

# Exibir relatório
template.exibir_relatorio()

# Salvar em JSON
template.salvar_relatorio_json("meu_relatorio.json")
```

### 3. Carregar Planilha Específica
```python
template = TemplateServicos()
template.carregar_dados_planilha("nova_planilha.xlsx", "area_chave")
```

## 📊 Relatórios Gerados

O template gera:
- **Relatório Console**: Visualização formatada no terminal
- **Arquivo JSON**: Dados estruturados para integração
- **Templates Excel**: Modelos para novas áreas

## 📁 Arquivos Gerados

- `relatorio_servicos.json`: Relatório completo em JSON
- `template_seguranca_acesso.xlsx`: Template para área de segurança
- `template_transporte.xlsx`: Template para área de transporte

## 🔧 Funcionalidades

### Análise por Área
- Total de funcionários por área
- Tipos de serviço oferecidos
- Locais de atuação
- Distribuição de funcionários por local

### Relatórios
- Resumo geral consolidado
- Detalhamento por área
- Exportação em múltiplos formatos

### Templates
- Criação automática de planilhas modelo
- Estrutura padronizada
- Fácil preenchimento

## 📈 Exemplo de Saída

```
🏢 RELATÓRIO DE SERVIÇOS TERCEIRIZADOS
================================================================================

📊 RESUMO GERAL:
   • Total de áreas: 4
   • Total de funcionários: 67
   • Áreas com dados: 2

🔹 MANUTENÇÃO DE PRÉDIOS
   📝 Serviços de manutenção predial corretiva e preventiva
   👥 Funcionários: 63
   🔧 Tipos de serviço:
      • Serviço de manutenção predial corretiva e preventiva nos prédios
   📍 Locais atendidos:
      • Sede (63 funcionários)
      • Arouche (63 funcionários)
      • Casa Verde (63 funcionários)
      ...
```

## 🛠️ Personalização

Você pode facilmente:
- Adicionar novas áreas de atuação
- Modificar a estrutura de dados
- Personalizar os relatórios
- Integrar com outros sistemas

## 📋 Próximos Passos

1. Preencher os templates gerados para Segurança e Transporte
2. Executar novamente para ver dados completos
3. Usar os relatórios JSON para integrações
4. Personalizar conforme suas necessidades específicas