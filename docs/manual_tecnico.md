# Documentação Técnica - Sistema de Funcionários Terceirizados

## 📋 Visão Geral

Este sistema web permite o gerenciamento e visualização organizada de funcionários terceirizados, processando dados automaticamente de planilhas Excel e apresentando-os em uma interface web moderna e responsiva.

## 🏗️ Arquitetura

### Estrutura de Diretórios
```
funcionarios-tercerizadas/
├── src/                    # Código fonte da aplicação web
├── data/                   # Dados de entrada (planilhas Excel)
├── scripts/                # Scripts de processamento Python
├── docs/                   # Documentação técnica
├── backup/                 # Arquivos de backup e versões antigas
├── assets/                 # Recursos estáticos
├── config/                 # Configurações do sistema
└── [arquivos raiz]         # Arquivos de configuração do projeto
```

### Componentes Principais

#### 1. Interface Web (`src/index.html`)
- **Tecnologias**: HTML5, CSS3, JavaScript vanilla
- **Funcionalidades**:
  - Exibição organizada por seções de serviço
  - Busca em tempo real
  - Design responsivo
  - Estatísticas automáticas

#### 2. Processador de Dados (`scripts/generate_html_from_excel.py`)
- **Tecnologias**: Python 3.x + Pandas + OpenPyXL
- **Funcionalidades**:
  - Leitura automática de planilhas Excel
  - Detecção inteligente de colunas
  - Geração de HTML estruturado
  - Mapeamento de serviços e localizações

#### 3. Dados de Entrada (`data/*.xlsx`)
- **Formato**: Planilhas Excel (.xlsx)
- **Estrutura esperada**:
  - Coluna de nomes de funcionários
  - Coluna de localizações
  - Metadados inferidos do nome do arquivo

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.6+
- Navegador web moderno
- Git (opcional)

### Instalação Automática
```bash
# Execute o script de configuração
python setup.py
```

### Instalação Manual
```bash
# 1. Instalar dependências Python
pip install -r requirements.txt

# 2. Verificar estrutura de arquivos
python setup.py
```

## 🚀 Uso

### Processamento de Dados
```bash
# Executar processamento das planilhas
python scripts/generate_html_from_excel.py
```

### Visualização
```bash
# Abrir no navegador
start src/index.html
# ou
# Abrir manualmente src/index.html no navegador
```

## 📊 Formato dos Dados

### Estrutura das Planilhas Excel

Cada planilha deve conter pelo menos uma coluna com nomes de funcionários. O sistema detecta automaticamente:

- **Colunas de nome**: "Nome", "Funcionário", "Colaborador", etc.
- **Colunas de localização**: "Local", "Unidade", "Setor", etc.
- **Mapeamento de serviço**: Baseado no nome do arquivo Excel

### Exemplo de Planilha
```
| Nome Completo          | Localização    |
|------------------------|----------------|
| João Silva Santos      | Sede           |
| Maria Oliveira Costa   | Arouche        |
| Pedro Santos Lima      | Efape          |
```

## ⚙️ Configuração

### Arquivo `config/settings.py`
Contém todas as configurações do sistema:

- Caminhos dos diretórios
- Lista de arquivos Excel
- Mapeamento de serviços
- Configurações da aplicação

### Personalização
Para adicionar novos serviços:
1. Adicione a planilha Excel na pasta `data/`
2. Atualize o `SERVICE_MAPPING` em `config/settings.py`
3. Execute o processamento novamente

## 🔍 Algoritmo de Processamento

### Detecção de Colunas
1. **Análise de cabeçalhos**: Busca por palavras-chave em português
2. **Análise de conteúdo**: Verifica padrões de dados
3. **Fallback**: Usa primeira coluna como nomes se não detectar

### Mapeamento de Serviços
- Nome do arquivo → Tipo de serviço
- Configurado em `SERVICE_MAPPING`
- Permite personalização completa

### Geração de HTML
- Template estruturado por seções
- Numeração sequencial de funcionários
- Classes CSS consistentes
- Metadados de localização e descrição

## 📈 Métricas e Estatísticas

### Dados Atuais (16/12/2024)
- **279 funcionários** totais
- **13 áreas de serviço** ativas
- **45 locais únicos** de atuação
- **10 planilhas Excel** processadas

### Cálculo Automático
- Total de funcionários: Contagem de registros válidos
- Áreas ativas: Número de seções geradas
- Locais únicos: Extração e deduplicação de localizações

## 🐛 Troubleshooting

### Problemas Comuns

#### 1. Erro de dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 2. Arquivos Excel não encontrados
- Verificar se estão na pasta `data/`
- Verificar permissões de leitura
- Verificar formato (.xlsx)

#### 3. HTML não atualiza
- Executar novamente o script de processamento
- Verificar se o arquivo `src/index.html` foi sobrescrito
- Limpar cache do navegador

#### 4. Busca não funciona
- Verificar se JavaScript está habilitado
- Verificar console do navegador por erros
- Testar com diferentes termos de busca

### Logs e Debug
```bash
# Executar com debug
python scripts/generate_html_from_excel.py --debug
```

## 🔄 Manutenção

### Atualização de Dados
1. Adicionar/modificar planilhas em `data/`
2. Atualizar configurações se necessário
3. Executar processamento
4. Testar visualização

### Backup
- Arquivos antigos movidos automaticamente para `backup/`
- Manter histórico de versões
- Backup antes de grandes mudanças

### Limpeza
```bash
# Limpar arquivos temporários
python scripts/cleanup.py
```

## 📝 Desenvolvimento

### Estrutura do Código
- `generate_html_from_excel.py`: Script principal de processamento
- `index.html`: Template da aplicação web
- `settings.py`: Configurações centralizadas

### Adição de Funcionalidades
1. Modificar script Python para nova lógica
2. Atualizar template HTML se necessário
3. Testar thoroughly
4. Atualizar documentação

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Verificar esta documentação
- Consultar issues no repositório
- Contatar o mantenedor

---

**Última atualização da documentação:** 16/12/2024</content>
<parameter name="filePath">c:\Users\bruno.vargas\Desktop\PROJETOS\funcionarios-tercerizadas\docs\manual_tecnico.md