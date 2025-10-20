# 👥 Lista de Funcionários - Guia de Uso

## ✅ Sistema de Listagem Criado!

Agora você tem várias formas de visualizar e exportar a lista de funcionários com suas respectivas áreas e locais.

## 🚀 Formas de Usar

### 1. Lista Rápida (Mais Simples) ⭐
```bash
python lista_rapida.py
```
- Mostra todos os funcionários organizados por área
- Exibe nome, tipo de serviço e locais de atuação
- Formato limpo e direto

### 2. Menu Completo (Mais Opções)
```bash
python listar_funcionarios.py
```
Opções disponíveis:
- **1**: Lista detalhada por área (com locais separados)
- **2**: Lista organizada por local (agrupa por local)
- **3**: Gerar planilha Excel (várias abas)
- **4**: Gerar arquivo JSON (para integrações)
- **5**: Buscar funcionário por nome
- **6**: Todas as opções de uma vez

### 3. Busca Rápida de Funcionário
```bash
# Exemplo: buscar por "SILVA"
python listar_funcionarios.py
# Escolha opção 5 e digite "SILVA"
```

## 📊 Arquivos Gerados

### Excel: `lista_funcionarios.xlsx`
- **Aba "Lista_Completa"**: Todos os funcionários
- **Aba "Manutenção_de_Prédios"**: Só funcionários desta área
- **Aba "Serviço_de_Copa"**: Só funcionários desta área
- **Aba "Por_Local"**: Agrupado por local

### JSON: `lista_funcionarios.json`
- Dados estruturados para sistemas
- Formato para integrações
- Inclui timestamp e totais

## 📋 Informações Exibidas

Para cada funcionário você verá:
- ✅ **Nome completo**
- ✅ **Área de atuação** (Manutenção, Copa, etc.)
- ✅ **Tipo de serviço** (descrição detalhada)
- ✅ **Locais de atuação** (Sede, Arouche, Casa Verde, etc.)

## 📊 Status Atual dos Seus Dados

- **Manutenção de Prédios**: ✅ 63 funcionários
  - Locais: Sede, Arouche, Efape, Casa Verde, Cape, Rio Branco, São Domingos, Armênia
  
- **Serviço de Copa**: ✅ 4 funcionários  
  - Local: Sede

- **Segurança e Controle de Acesso**: ⏳ Aguardando dados
- **Transporte**: ⏳ Aguardando dados

## 🔍 Exemplos de Uso

### Ver lista completa rapidamente:
```bash
python lista_rapida.py
```

### Gerar planilha Excel para compartilhar:
```bash
python listar_funcionarios.py
# Digite: 3
```

### Procurar funcionário específico:
```bash
python listar_funcionarios.py  
# Digite: 5
# Digite o nome: SILVA
```

### Gerar todos os formatos:
```bash
python listar_funcionarios.py
# Digite: 6
```

## 💡 Dicas

1. **Para relatórios**: Use a planilha Excel (opção 3)
2. **Para consulta rápida**: Use `lista_rapida.py`
3. **Para integração com sistemas**: Use o arquivo JSON (opção 4)
4. **Para buscar alguém**: Use a busca por nome (opção 5)

## 📈 Resultado Esperado

Você terá acesso a:
- ✅ **Lista completa** de todos os 67 funcionários
- ✅ **Organização por área** (Manutenção: 63, Copa: 4)
- ✅ **Detalhamento por local** (8 locais diferentes)
- ✅ **Múltiplos formatos** (Console, Excel, JSON)
- ✅ **Busca por nome** para localizar funcionários específicos

---

**Para começar:** Execute `python lista_rapida.py` e veja a lista completa dos seus funcionários! 📋