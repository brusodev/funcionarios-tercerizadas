"""
Template HTML Simples - Lista de Funcionários
============================================

Versão simplificada focada apenas na listagem de nomes por área e local.
"""

from template_servicos import TemplateServicos
from datetime import datetime

def gerar_html_simples(arquivo_saida="lista_funcionarios_simples.html"):
    """Gera template HTML simples com foco na listagem"""
    
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Funcionários por Área e Local</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        
        .header {
            background: #2c5aa0;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }
        
        .area {
            background: white;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .area-title {
            background: #34495e;
            color: white;
            padding: 15px 20px;
            font-size: 1.3rem;
            font-weight: bold;
        }
        
        .locals {
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .local {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            background: #fafafa;
        }
        
        .local-title {
            background: #3498db;
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .funcionario {
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
        }
        
        .funcionario:last-child {
            border-bottom: none;
        }
        
        .funcionario-numero {
            background: #95a5a6;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            margin-right: 10px;
            min-width: 35px;
            text-align: center;
        }
        
        .funcionario-nome {
            font-weight: 500;
            color: #2c3e50;
        }
        
        .stats {
            background: #ecf0f1;
            padding: 10px 20px;
            border-top: 1px solid #ddd;
            font-size: 0.9rem;
            color: #7f8c8d;
        }
        
        .no-data {
            padding: 30px;
            text-align: center;
            color: #95a5a6;
            font-style: italic;
        }
        
        .search {
            margin-bottom: 20px;
            text-align: center;
        }
        
        .search input {
            padding: 10px 15px;
            font-size: 1rem;
            border: 1px solid #ddd;
            border-radius: 25px;
            width: 100%;
            max-width: 400px;
        }
        
        @media print {
            .search { display: none; }
            body { background: white; }
            .area { box-shadow: none; border: 1px solid #ddd; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Lista de Funcionários por Área e Local</h1>
        <p>Atualizado em: {timestamp}</p>
        <p><strong>{total_funcionarios}</strong> funcionários • <strong>{total_areas}</strong> áreas • <strong>{total_locais}</strong> locais</p>
    </div>
    
    <div class="search">
        <input type="text" placeholder="🔍 Buscar funcionário..." id="search" onkeyup="buscarFuncionario()">
    </div>
    
    {areas_content}
    
    <script>
        function buscarFuncionario() {
            const input = document.getElementById('search').value.toLowerCase();
            const funcionarios = document.querySelectorAll('.funcionario');
            
            funcionarios.forEach(function(func) {
                const nome = func.querySelector('.funcionario-nome').textContent.toLowerCase();
                if (nome.includes(input)) {
                    func.style.display = 'flex';
                } else {
                    func.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>"""

    # Processar áreas
    areas_content = []
    total_funcionarios = 0
    areas_ativas = 0
    todos_locais = set()
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            areas_ativas += 1
            total_funcionarios += len(area.funcionarios)
            
            # Obter funcionários por local
            funcionarios_por_local = area.get_funcionarios_por_local()
            todos_locais.update(funcionarios_por_local.keys())
            
            # Gerar HTML dos locais
            locals_html = []
            for local, funcionarios in funcionarios_por_local.items():
                funcionarios_html = []
                
                for func in funcionarios:
                    funcionarios_html.append(f"""
                    <div class="funcionario">
                        <span class="funcionario-numero">#{func.numero}</span>
                        <span class="funcionario-nome">{func.nome}</span>
                    </div>
                    """)
                
                locals_html.append(f"""
                <div class="local">
                    <div class="local-title">📍 {local} ({len(funcionarios)} funcionários)</div>
                    {''.join(funcionarios_html)}
                </div>
                """)
            
            # HTML da área
            area_html = f"""
            <div class="area">
                <div class="area-title">🏢 {area.nome}</div>
                <div class="locals">
                    {''.join(locals_html)}
                </div>
                <div class="stats">
                    📊 Total da área: {len(area.funcionarios)} funcionários em {len(funcionarios_por_local)} locais
                </div>
            </div>
            """
            areas_content.append(area_html)
    
    # Áreas sem dados
    for chave, area in template.areas.items():
        if not area.funcionarios:
            area_html = f"""
            <div class="area">
                <div class="area-title">⏳ {area.nome}</div>
                <div class="no-data">
                    📝 Aguardando preenchimento dos dados<br>
                    <small>Preencha o arquivo: template_{chave}.xlsx</small>
                </div>
            </div>
            """
            areas_content.append(area_html)
    
    # Substituir variáveis
    html_final = html_template.replace("{timestamp}", datetime.now().strftime("%d/%m/%Y às %H:%M"))
    html_final = html_final.replace("{total_funcionarios}", str(total_funcionarios))
    html_final = html_final.replace("{total_areas}", str(areas_ativas))
    html_final = html_final.replace("{total_locais}", str(len(todos_locais)))
    html_final = html_final.replace("{areas_content}", ''.join(areas_content))
    
    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Template HTML simples criado: {arquivo_saida}")
    return arquivo_saida

if __name__ == "__main__":
    print("🚀 Gerando Template HTML Simples...")
    arquivo = gerar_html_simples()
    
    # Abrir no navegador
    try:
        import webbrowser
        from pathlib import Path
        
        caminho_absoluto = Path(arquivo).absolute()
        url = f"file:///{caminho_absoluto}".replace("\\", "/")
        webbrowser.open(url)
        print("🌐 Arquivo aberto no navegador!")
    except:
        print(f"💡 Abra manualmente: {arquivo}")