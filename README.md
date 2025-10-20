# Sistema de Gerenciamento de Funcionários Terceirizados

## 📋 Descrição

Sistema web para gerenciamento e visualização de funcionários terceirizados organizados por tipo de serviço e localização. Os dados são processados automaticamente a partir de planilhas Excel.

## 🏗️ Estrutura do Projeto

```
funcionarios-tercerizadas/
├── src/                    # Código fonte da aplicação
│   └── index.html         # Aplicação principal
├── data/                   # Arquivos de dados Excel
│   ├── Bombeiro Civil.xlsx
│   ├── manutencao_predios.xlsx
│   └── ... (outras planilhas)
├── scripts/                # Scripts de processamento
│   └── generate_html_from_excel.py
├── docs/                   # Documentação
├── backup/                 # Arquivos de backup e versões antigas
├── assets/                 # Recursos estáticos (CSS, JS, imagens)
├── config/                 # Arquivos de configuração
├── .git/                   # Controle de versão
├── .vscode/                # Configurações do VS Code
└── README.md              # Este arquivo
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.x com pandas instalado
- Navegador web moderno

### Instalação
1. Clone o repositório
2. Instale as dependências Python:
   ```bash
   pip install pandas openpyxl
   ```

### Execução
1. Execute o script de processamento:
   ```bash
   python scripts/generate_html_from_excel.py
   ```
2. Abra `src/index.html` no navegador

## 📊 Funcionalidades

- ✅ Visualização organizada por tipo de serviço
- ✅ Busca em tempo real por nome de funcionário
- ✅ Estatísticas automáticas (total de funcionários, áreas, locais)
- ✅ Design responsivo
- ✅ Processamento automático de planilhas Excel

## 📈 Estatísticas Atuais

- **279 funcionários** distribuídos em **13 áreas de serviço**
- **45 locais únicos** de atuação
- Dados atualizados automaticamente das planilhas Excel

## 🛠️ Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend de processamento**: Python + Pandas
- **Dados**: Planilhas Excel (.xlsx)
- **Biblioteca Excel**: SheetJS (XLSX)

## 📝 Estrutura dos Dados

Cada planilha Excel deve conter as seguintes colunas:
- Nome do funcionário
- Localização/Local
- Tipo de serviço (opcional - inferido do nome do arquivo)

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Contato

Bruno Vargas - [seu-email@exemplo.com]

Link do projeto: [https://github.com/brusodev/funcionarios-tercerizadas](https://github.com/brusodev/funcionarios-tercerizadas)

---

**Última atualização:** 16/12/2024 às 14:30</content>
<parameter name="filePath">c:\Users\bruno.vargas\Desktop\PROJETOS\funcionarios-tercerizadas\README.md