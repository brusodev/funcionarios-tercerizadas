# 🌐 Dashboard HTML - Serviços Terceirizados

## ✅ Dashboard HTML Criado com Sucesso!

Seu dashboard HTML está pronto e funcional, exibindo todos os dados reais das suas planilhas.

## 📊 Arquivos HTML Disponíveis

### 1. `dashboard_dinamico.html` ⭐ **RECOMENDADO**
- **Dashboard com dados reais** das suas planilhas
- Atualizado automaticamente com informações atuais
- Estatísticas completas e visualizações interativas
- **Este é o arquivo principal para usar**

### 2. `dashboard.html`
- Dashboard estático com dados de exemplo
- Útil como template de referência

## 🚀 Como Usar o Dashboard HTML

### Opção 1: Visualização Automática (Mais Fácil)
```bash
# Gera e abre automaticamente no navegador
python visualizar_dashboard.py --direto
```

### Opção 2: Menu Interativo
```bash  
# Menu com várias opções
python visualizar_dashboard.py
```

### Opção 3: Gerar Manualmente
```bash
# Apenas gerar o arquivo HTML
python gerar_dashboard.py
```

### Opção 4: Abrir Diretamente
- Navegue até a pasta do projeto
- Clique duas vezes em `dashboard_dinamico.html`
- O arquivo abrirá no seu navegador padrão

## 📈 O que o Dashboard Mostra

### 📊 Estatísticas Gerais
- **Total de Áreas**: 4 áreas de atuação
- **Total de Funcionários**: 67 funcionários ativos
- **Áreas Ativas**: 2 com dados carregados
- **Locais Atendidos**: 8 locais únicos

### 🏢 Detalhes por Área
- **Manutenção de Prédios**: ✅ 63 funcionários em 8 locais
- **Serviço de Copa**: ✅ 4 funcionários na Sede
- **Segurança e Controle de Acesso**: ⏳ Aguardando dados
- **Transporte**: ⏳ Aguardando dados

### 📍 Informações Detalhadas
- Distribuição de funcionários por local
- Tipos de serviços oferecidos
- Barras de progresso visuais
- Status de cada área

## 🔄 Atualização Automática

Para manter o dashboard sempre atualizado:

### Quando adicionar novos dados:
1. **Atualize as planilhas** Excel existentes
2. **Execute**: `python visualizar_dashboard.py --direto`
3. **O dashboard será regenerado** com os novos dados

### Para novas áreas (Segurança/Transporte):
1. **Preencha os templates** criados:
   - `template_seguranca_acesso.xlsx`
   - `template_transporte.xlsx`
2. **Renomeie para**: `seguranca_acesso.xlsx` e `transporte.xlsx`
3. **Execute o visualizador** novamente

## 💡 Características do Dashboard

### ✅ Design Responsivo
- Funciona em **desktop, tablet e celular**
- Layout adaptativo e profissional
- Cores e gradientes modernos

### ✅ Interativo
- **Hover effects** nos cartões
- **Informações detalhadas** para cada área
- **Visual atrativo** e fácil de entender

### ✅ Dados Reais
- **Conectado às suas planilhas** Excel
- **Atualização automática** dos números
- **Timestamp** da última atualização

### ✅ Informações Completas
- **Funcionários por local** com contagem
- **Tipos de serviços** de cada área
- **Barras de progresso** visuais
- **Status** de cada área

## 🗂️ Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `dashboard_dinamico.html` | **Dashboard principal** com dados reais |
| `dados_dashboard.json` | Dados estruturados em JSON |
| `visualizar_dashboard.py` | **Script para abrir** no navegador |
| `gerar_dashboard.py` | Gerador do HTML |

## 🎯 Comandos Úteis

```bash
# Ver dashboard atualizado
python visualizar_dashboard.py --direto

# Menu com opções
python visualizar_dashboard.py

# Apenas gerar arquivos
python gerar_dashboard.py

# Ver status dos dados
python gerar_relatorio.py --simples
```

## 📱 Compatibilidade

✅ **Navegadores Suportados:**
- Chrome, Firefox, Safari, Edge
- Versões modernas (últimos 2 anos)

✅ **Dispositivos:**
- Desktop/Laptop
- Tablets
- Smartphones

✅ **Sistemas:**
- Windows, macOS, Linux

---

## 🎉 Resultado Final

Você agora tem um **dashboard HTML profissional** que:

- ✅ **Exibe seus dados reais** das planilhas Excel
- ✅ **Atualiza automaticamente** quando você modificar os dados  
- ✅ **Funciona offline** (não precisa de internet)
- ✅ **Visual moderno** e responsivo
- ✅ **Fácil de usar** e compartilhar

**Para começar:** Execute `python visualizar_dashboard.py --direto` e veja seu dashboard em ação! 🚀