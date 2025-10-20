# 🏢 Template de Organização de Serviços Terceirizados

## ✅ Template Criado com Sucesso!

Seu template está pronto e funcionando perfeitamente com os dados das suas planilhas existentes.

## 📊 Status Atual dos Dados

- **Manutenção de Prédios**: ✅ 63 funcionários carregados
- **Serviço de Copa**: ✅ 4 funcionários carregados  
- **Segurança e Controle de Acesso**: ⏳ Template criado (precisa preencher)
- **Transporte**: ⏳ Template criado (precisa preencher)

## 🚀 Como Usar o Template

### 1. Relatório Rápido (Mais Usado)
```bash
python gerar_relatorio.py --simples
```

### 2. Salvar Relatório em JSON
```bash
python gerar_relatorio.py --json meu_relatorio.json
```

### 3. Listar Funcionários
```bash
# Todos os funcionários
python gerar_relatorio.py --funcionarios

# Funcionários de uma área específica
python gerar_relatorio.py --funcionarios manutencao_predios
```

### 4. Ver Locais de Atuação
```bash
python gerar_relatorio.py --locais
```

### 5. Usar como Módulo Python
```python
from template_servicos import TemplateServicos

template = TemplateServicos()
template.carregar_todos_dados()
template.exibir_relatorio()
```

## 📋 Próximos Passos

### 1. Completar Áreas Pendentes
Foram criados templates Excel para as áreas que ainda não têm dados:
- `template_seguranca_acesso.xlsx`
- `template_transporte.xlsx`

**Preencha estes templates** seguindo a estrutura:
- Coluna `nº`: Número sequencial
- Coluna `nome`: Nome completo do funcionário  
- Coluna `tipo_manutecao`: Tipo de serviço (ex: "Serviço de segurança patrimonial")
- Coluna `locais`: Locais separados por "/" (ex: "Sede/Arouche/Casa Verde")

### 2. Após Preencher os Templates
Execute novamente o relatório para ver todos os dados:
```bash
python gerar_relatorio.py --simples
```

## 🗂️ Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| `template_servicos.py` | **Código principal** - Classes e funções do template |
| `gerar_relatorio.py` | **Utilitário rápido** - Para gerar relatórios sem programar |
| `exemplo_uso.py` | **Exemplos avançados** - Para aprender mais funcionalidades |
| `README.md` | **Documentação completa** - Guia detalhado |

## 🔧 Funcionalidades Principais

### ✅ O que já funciona:
- ✅ Leitura automática das planilhas Excel
- ✅ Organização por áreas de atuação
- ✅ Relatórios formatados no console
- ✅ Exportação para JSON
- ✅ Análise por local de atuação
- ✅ Contagem de funcionários por área
- ✅ Templates para novas áreas

### 🚀 Benefícios:
- **Organização**: Estrutura clara por áreas de serviço
- **Flexibilidade**: Fácil adição de novas áreas
- **Relatórios**: Múltiplos formatos de saída
- **Automação**: Processamento automático das planilhas
- **Análises**: Distribuição por locais, totais, comparativos

## 💡 Dicas de Uso

1. **Para relatórios rápidos**: Use `gerar_relatorio.py`
2. **Para integrações**: Use os arquivos JSON gerados
3. **Para análises customizadas**: Use `template_servicos.py`
4. **Para aprender mais**: Veja `exemplo_uso.py`

## 📞 Comandos Mais Úteis

```bash
# Ver estrutura geral
python gerar_relatorio.py --simples

# Ver todos os funcionários  
python gerar_relatorio.py --funcionarios

# Ver todos os locais
python gerar_relatorio.py --locais

# Gerar arquivo para Excel/sistemas
python gerar_relatorio.py --json dados_completos.json
```

---

🎉 **Seu template está pronto para uso!** 

Comece executando `python gerar_relatorio.py --simples` para ver o relatório completo dos seus dados atuais.