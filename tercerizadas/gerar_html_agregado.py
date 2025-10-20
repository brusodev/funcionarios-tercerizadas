"""
Gerador de Template HTML - Lista de Funcionários Agregados por Local
===================================================================

Script para gerar um template HTML com a lista completa de funcionários
organizados pelos locais agregados de todas as planilhas.
"""

from template_servicos import TemplateServicos
from datetime import datetime
import webbrowser
import os

def gerar_html_agregado(arquivo_saida="funcionarios_agregado.html"):
    """Gera template HTML com funcionários agregados por local de todas as planilhas"""
    
    # Carregar dados de todas as 4 planilhas
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    # Obter locais únicos e funcionários por local global
    locais_unicos = template.get_todos_locais_unicos()
    funcionarios_por_local_global = template.get_funcionarios_por_local_global()
    
    # Template HTML base
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Funcionários - Locais Agregados</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 30px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
        }

        .stat-item {
            text-align: center;
            padding: 15px 25px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            display: block;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }

        .search-container {
            padding: 30px 40px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }

        .search-box {
            position: relative;
            max-width: 500px;
            margin: 0 auto;
        }

        .search-input {
            width: 100%;
            padding: 15px 50px 15px 20px;
            font-size: 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            background: white;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: #4f46e5;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
            font-size: 18px;
        }

        .content {
            padding: 40px;
        }

        .locations-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
            margin-top: 20px;
        }

        .location-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        .location-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            border-color: #4f46e5;
        }

        .location-header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .location-name {
            font-size: 1.3em;
            font-weight: 600;
            margin: 0;
        }

        .location-count {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }

        .funcionarios-list {
            padding: 20px;
        }

        .funcionario-item {
            padding: 15px;
            border-bottom: 1px solid #f1f5f9;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
        }

        .funcionario-item:last-child {
            border-bottom: none;
        }

        .funcionario-item:hover {
            background: #f8fafc;
            padding-left: 20px;
        }

        .funcionario-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .funcionario-nome {
            font-weight: 600;
            color: #1e293b;
            font-size: 1.1em;
        }

        .funcionario-numero {
            background: #4f46e5;
            color: white;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.8em;
            margin-right: 10px;
        }

        .funcionario-area {
            color: #64748b;
            font-size: 0.9em;
            font-style: italic;
        }

        .funcionario-servico {
            color: #059669;
            font-size: 0.9em;
            background: #ecfdf5;
            padding: 5px 10px;
            border-radius: 8px;
            white-space: nowrap;
        }

        .footer {
            background: #f8fafc;
            padding: 30px 40px;
            text-align: center;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }

        .print-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #4f46e5;
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .print-btn:hover {
            background: #3730a3;
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(79, 70, 229, 0.4);
        }

        @media print {
            .print-btn { display: none; }
            .search-container { display: none; }
            body { background: white; }
            .container { box-shadow: none; }
            .location-card { break-inside: avoid; }
        }

        @media (max-width: 768px) {
            .locations-grid {
                grid-template-columns: 1fr;
            }
            
            .stats {
                flex-direction: column;
                gap: 15px;
            }
            
            .funcionario-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Lista de Funcionários</h1>
            <p>Serviços Terceirizados - Organizados por Local</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_funcionarios}</span>
                    <span class="stat-label">Funcionários</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_locais}</span>
                    <span class="stat-label">Locais</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_areas}</span>
                    <span class="stat-label">Áreas</span>
                </div>
            </div>
        </div>

        <div class="search-container">
            <div class="search-box">
                <input type="text" class="search-input" id="searchInput" placeholder="🔍 Buscar funcionário por nome...">
                <span class="search-icon">🔍</span>
            </div>
        </div>

        <div class="content">
            <div class="locations-grid" id="locationsGrid">
                {locais_html}
            </div>
        </div>

        <div class="footer">
            <p>📅 Atualizado em: {timestamp}</p>
            <p>💼 Total de {total_funcionarios} funcionários em {total_locais} locais diferentes</p>
        </div>
    </div>

    <button class="print-btn" onclick="window.print()" title="Imprimir Lista">
        🖨️ Imprimir
    </button>

    <script>
        // Funcionalidade de busca
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const locationCards = document.querySelectorAll('.location-card');
            
            locationCards.forEach(card => {
                const funcionarios = card.querySelectorAll('.funcionario-item');
                let hasVisibleFuncionario = false;
                
                funcionarios.forEach(funcionario => {
                    const nome = funcionario.querySelector('.funcionario-nome').textContent.toLowerCase();
                    if (nome.includes(searchTerm)) {
                        funcionario.style.display = 'flex';
                        hasVisibleFuncionario = true;
                    } else {
                        funcionario.style.display = 'none';
                    }
                });
                
                // Mostrar/esconder card baseado se tem funcionários visíveis
                card.style.display = hasVisibleFuncionario ? 'block' : 'none';
            });
        });

        // Animação ao carregar
        window.addEventListener('load', function() {
            const cards = document.querySelectorAll('.location-card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    card.style.transition = 'all 0.6s ease';
                    
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                }, index * 100);
            });
        });
    </script>
</body>
</html>"""

    # Processar locais agregados
    locais_html = []
    total_funcionarios = 0
    
    # Contar total de funcionários únicos
    funcionarios_unicos = set()
    for funcionarios_local in funcionarios_por_local_global.values():
        for funcionario, area_nome in funcionarios_local:
            funcionarios_unicos.add((funcionario.numero, funcionario.nome))
    
    total_funcionarios = len(funcionarios_unicos)
    
    # Gerar HTML para cada local
    for local in sorted(locais_unicos):
        if local in funcionarios_por_local_global:
            funcionarios_local = funcionarios_por_local_global[local]
            
            funcionarios_html = []
            for funcionario, area_nome in funcionarios_local:
                funcionario_html = f"""
                <div class="funcionario-item">
                    <div class="funcionario-info">
                        <div class="funcionario-nome">
                            <span class="funcionario-numero">#{funcionario.numero}</span>
                            {funcionario.nome}
                        </div>
                        <div class="funcionario-area">{area_nome}</div>
                    </div>
                    <div class="funcionario-servico">{funcionario.tipo_servico}</div>
                </div>"""
                funcionarios_html.append(funcionario_html)
            
            local_html = f"""
            <div class="location-card">
                <div class="location-header">
                    <h3 class="location-name">📍 {local}</h3>
                    <span class="location-count">{len(funcionarios_local)} funcionário{'s' if len(funcionarios_local) > 1 else ''}</span>
                </div>
                <div class="funcionarios-list">
                    {''.join(funcionarios_html)}
                </div>
            </div>"""
            locais_html.append(local_html)
    
    # Calcular estatísticas
    areas_ativas = sum(1 for area in template.areas.values() if area.funcionarios)
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    # Montar HTML final
    html_final = html_template.replace("{locais_html}", '\n'.join(locais_html))
    html_final = html_final.replace("{total_funcionarios}", str(total_funcionarios))
    html_final = html_final.replace("{total_locais}", str(len(locais_unicos)))
    html_final = html_final.replace("{total_areas}", str(areas_ativas))
    html_final = html_final.replace("{timestamp}", timestamp)
    
    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    # Abrir no navegador
    arquivo_completo = os.path.abspath(arquivo_saida)
    webbrowser.open(f'file://{arquivo_completo}')
    
    # Mostrar estatísticas
    print(f"\n✅ Template HTML gerado com sucesso!")
    print(f"📄 Arquivo: {arquivo_saida}")
    print(f"🌐 Aberto no navegador automaticamente")
    print(f"\n📊 Estatísticas:")
    print(f"   • {total_funcionarios} funcionários únicos")
    print(f"   • {len(locais_unicos)} locais únicos")
    print(f"   • {areas_ativas} áreas ativas")
    
    print(f"\n📍 Locais encontrados:")
    for i, local in enumerate(sorted(locais_unicos), 1):
        count = len(funcionarios_por_local_global.get(local, []))
        print(f"   {i:2d}. {local} ({count} funcionário{'s' if count > 1 else ''})")

if __name__ == "__main__":
    gerar_html_agregado()