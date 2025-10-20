"""
Gerador de Template HTML - Lista de Funcionários
===============================================

Script para gerar um template HTML com a lista completa de funcionários
organizados por área e local de atuação.
"""

from template_servicos import TemplateServicos
from datetime import datetime
import json

def gerar_html_funcionarios(arquivo_saida="funcionarios.html"):
    """Gera template HTML com lista de funcionários por área e local"""
    
    # Carregar dados reais de todas as 4 planilhas
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    # Obter locais únicos agregados e funcionários por local
    locais_unicos = template.get_todos_locais_unicos()
    funcionarios_por_local = template.get_funcionarios_por_local_global()
    
    # Template HTML base
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Funcionários - Serviços Terceirizados</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 300;
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 15px;
        }

        .update-info {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 0.9rem;
        }

        .summary {
            background: #f8f9fa;
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .summary-item {
            background: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }

        .summary-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }

        .summary-label {
            color: #6c757d;
            font-weight: 500;
        }

        .content {
            padding: 30px;
        }

        .area-section {
            margin-bottom: 40px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            overflow: hidden;
        }

        .area-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
        }

        .area-title {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .area-description {
            opacity: 0.9;
            font-size: 1rem;
        }

        .area-stats {
            display: flex;
            gap: 30px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .area-stat {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
        }

        .locations-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            padding: 30px;
        }

        .location-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            border-left: 5px solid #667eea;
        }

        .location-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #343a40;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .location-count {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }

        .funcionarios-list {
            display: grid;
            gap: 12px;
        }

        .funcionario-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            border-left: 3px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }

        .funcionario-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .funcionario-nome {
            font-weight: 600;
            color: #343a40;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .funcionario-servico {
            color: #6c757d;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .funcionario-numero {
            background: #e9ecef;
            color: #495057;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-right: 10px;
        }

        .no-data {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 40px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .search-box {
            margin-bottom: 30px;
            text-align: center;
        }

        .search-input {
            padding: 15px 25px;
            font-size: 1.1rem;
            border: 2px solid #e9ecef;
            border-radius: 50px;
            width: 100%;
            max-width: 500px;
            outline: none;
            transition: border-color 0.3s ease;
        }

        .search-input:focus {
            border-color: #667eea;
        }

        .footer {
            background: #343a40;
            color: white;
            padding: 20px 30px;
            text-align: center;
        }

        .print-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            margin: 0 10px;
            transition: background 0.3s ease;
        }

        .print-btn:hover {
            background: #5a67d8;
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
                border-radius: 0;
            }
            
            .search-box, .print-btn {
                display: none;
            }
            
            .area-header {
                background: #667eea !important;
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
            }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .locations-grid {
                grid-template-columns: 1fr;
            }
            
            .summary {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👥 Lista de Funcionários</h1>
            <p>Serviços Terceirizados por Área e Local</p>
            <div class="update-info">
                📅 Última atualização: {timestamp}
            </div>
        </div>

        <div class="summary">
            <div class="summary-item">
                <div class="summary-number">{total_funcionarios}</div>
                <div class="summary-label">Total de Funcionários</div>
            </div>
            <div class="summary-item">
                <div class="summary-number">{total_areas}</div>
                <div class="summary-label">Áreas Ativas</div>
            </div>
            <div class="summary-item">
                <div class="summary-number">{total_locais}</div>
                <div class="summary-label">Locais Atendidos</div>
            </div>
            <div class="summary-item">
                <div class="summary-number">{media_func_local:.1f}</div>
                <div class="summary-label">Média Func/Local</div>
            </div>
        </div>

        <div class="content">
            <div class="search-box">
                <input type="text" class="search-input" placeholder="🔍 Buscar funcionário por nome..." id="searchInput">
                <br><br>
                <button class="print-btn" onclick="window.print()">🖨️ Imprimir</button>
                <button class="print-btn" onclick="exportarPDF()">📄 Exportar PDF</button>
            </div>

            {areas_html}
        </div>

        <div class="footer">
            🚀 Template de Serviços Terceirizados | Total: {total_funcionarios} funcionários em {total_locais} locais
        </div>
    </div>

    <script>
        // Funcionalidade de busca
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const funcionarios = document.querySelectorAll('.funcionario-item');
            
            funcionarios.forEach(function(item) {
                const nome = item.querySelector('.funcionario-nome').textContent.toLowerCase();
                const servico = item.querySelector('.funcionario-servico').textContent.toLowerCase();
                
                if (nome.includes(searchTerm) || servico.includes(searchTerm)) {
                    item.style.display = 'block';
                    item.parentElement.style.display = 'grid';
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Esconder cards de local vazios
            document.querySelectorAll('.location-card').forEach(function(card) {
                const visibleItems = card.querySelectorAll('.funcionario-item[style*="block"], .funcionario-item:not([style*="none"])');
                if (visibleItems.length === 0 && searchTerm !== '') {
                    card.style.display = 'none';
                } else {
                    card.style.display = 'block';
                }
            });
            
            // Esconder seções de área vazias
            document.querySelectorAll('.area-section').forEach(function(section) {
                const visibleCards = section.querySelectorAll('.location-card[style*="block"], .location-card:not([style*="none"])');
                if (visibleCards.length === 0 && searchTerm !== '') {
                    section.style.display = 'none';
                } else {
                    section.style.display = 'block';
                }
            });
        });

        // Função para exportar PDF (placeholder)
        function exportarPDF() {
            alert('Funcionalidade de PDF: Use Ctrl+P e selecione "Salvar como PDF" no seu navegador');
        }

        // Highlight do termo de busca
        function highlightSearchTerm(text, term) {
            if (!term) return text;
            const regex = new RegExp(`(${term})`, 'gi');
            return text.replace(regex, '<mark>$1</mark>');
        }
    </script>
</body>
</html>"""

    # Processar dados por área
    areas_html = []
    total_funcionarios = 0
    total_locais = set()
    areas_ativas = 0
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            areas_ativas += 1
            total_funcionarios += len(area.funcionarios)
            
            # Obter funcionários por local para esta área
            funcionarios_por_local = area.get_funcionarios_por_local()
            
            # Adicionar locais ao conjunto total
            for local in funcionarios_por_local.keys():
                total_locais.add(local)
            
            # Estatísticas da área
            area_stats = [
                f"👥 {len(area.funcionarios)} funcionários",
                f"📍 {len(funcionarios_por_local)} locais",
                f"🔧 {len(area.tipos_servico)} tipo(s) de serviço"
            ]
            
            # HTML dos locais
            locations_html = []
            for local, funcionarios in funcionarios_por_local.items():
                funcionarios_html = []
                
                for func in funcionarios:
                    funcionario_html = f"""
                    <div class="funcionario-item">
                        <div class="funcionario-nome">
                            <span class="funcionario-numero">#{func.numero}</span>
                            {func.nome}
                        </div>
                        <div class="funcionario-servico">{func.tipo_servico}</div>
                    </div>
                    """
                    funcionarios_html.append(funcionario_html)
                
                location_html = f"""
                <div class="location-card">
                    <div class="location-title">
                        📍 {local}
                        <span class="location-count">{len(funcionarios)}</span>
                    </div>
                    <div class="funcionarios-list">
                        {''.join(funcionarios_html)}
                    </div>
                </div>
                """
                locations_html.append(location_html)
            
            # HTML da área completa
            area_html = f"""
            <div class="area-section">
                <div class="area-header">
                    <div class="area-title">🏢 {area.nome}</div>
                    <div class="area-description">{area.descricao}</div>
                    <div class="area-stats">
                        {''.join([f'<div class="area-stat">{stat}</div>' for stat in area_stats])}
                    </div>
                </div>
                <div class="locations-grid">
                    {''.join(locations_html)}
                </div>
            </div>
            """
            areas_html.append(area_html)
    
    # Áreas sem dados
    for chave, area in template.areas.items():
        if not area.funcionarios:
            area_html = f"""
            <div class="area-section">
                <div class="area-header">
                    <div class="area-title">⏳ {area.nome}</div>
                    <div class="area-description">{area.descricao}</div>
                    <div class="area-stats">
                        <div class="area-stat">📋 Aguardando dados</div>
                    </div>
                </div>
                <div class="locations-grid">
                    <div class="location-card">
                        <div class="no-data">
                            📝 Template criado - preencha a planilha Excel correspondente<br>
                            <small>Arquivo: template_{chave}.xlsx</small>
                        </div>
                    </div>
                </div>
            </div>
            """
            areas_html.append(area_html)
    
    # Calcular média de funcionários por local
    media_func_local = total_funcionarios / max(len(total_locais), 1)
    
    # Preencher template
    html_final = html_template.replace("{timestamp}", datetime.now().strftime("%d/%m/%Y às %H:%M"))
    html_final = html_final.replace("{total_funcionarios}", str(total_funcionarios))
    html_final = html_final.replace("{total_areas}", str(areas_ativas))
    html_final = html_final.replace("{total_locais}", str(len(total_locais)))
    html_final = html_final.replace("{media_func_local}", str(media_func_local))
    html_final = html_final.replace("{areas_html}", ''.join(areas_html))
    
    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Template HTML criado: {arquivo_saida}")
    print(f"📊 Dados incluídos:")
    print(f"   • {total_funcionarios} funcionários")
    print(f"   • {areas_ativas} áreas ativas")
    print(f"   • {len(total_locais)} locais únicos")
    print(f"💡 Para visualizar: Abra o arquivo {arquivo_saida} no seu navegador")
    
    return arquivo_saida

def main():
    """Função principal"""
    print("🚀 Gerando Template HTML de Funcionários...")
    arquivo = gerar_html_funcionarios()
    
    # Abrir automaticamente no navegador
    try:
        import webbrowser
        from pathlib import Path
        
        caminho_absoluto = Path(arquivo).absolute()
        url = f"file:///{caminho_absoluto}".replace("\\", "/")
        webbrowser.open(url)
        print("🌐 Arquivo aberto automaticamente no navegador!")
    except Exception as e:
        print(f"💡 Abra manualmente o arquivo: {arquivo}")

if __name__ == "__main__":
    main()