"""
Gerador de Dashboard HTML para Serviços Terceirizados
====================================================

Este script gera um dashboard HTML interativo com os dados reais das planilhas.
"""

import json
from pathlib import Path
from template_servicos import TemplateServicos

def gerar_dashboard_html(arquivo_saida="dashboard_dinamico.html"):
    """Gera dashboard HTML com dados reais"""
    
    # Carregar dados reais
    template = TemplateServicos()
    template.carregar_todos_dados()
    relatorio = template.gerar_relatorio_completo()
    
    # Template HTML base
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Serviços Terceirizados</title>
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
        }

        .update-info {
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 0.9rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-number {
            font-size: 3rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 1.1rem;
            color: #6c757d;
            font-weight: 500;
        }

        .areas-section {
            padding: 30px;
        }

        .section-title {
            font-size: 2rem;
            color: #343a40;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 300;
        }

        .areas-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }

        .area-card {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            overflow: hidden;
            transition: transform 0.3s ease;
        }

        .area-card:hover {
            transform: translateY(-5px);
        }

        .area-header {
            padding: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .area-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .area-description {
            opacity: 0.9;
            font-size: 0.95rem;
        }

        .area-content {
            padding: 25px;
        }

        .area-stats {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .area-stat {
            text-align: center;
        }

        .area-stat-number {
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
        }

        .area-stat-label {
            font-size: 0.9rem;
            color: #6c757d;
            margin-top: 5px;
        }

        .locations-list {
            margin-top: 20px;
        }

        .locations-title {
            font-weight: 600;
            color: #343a40;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }

        .location-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .location-item:last-child {
            border-bottom: none;
        }

        .location-name {
            color: #495057;
            font-weight: 500;
        }

        .location-count {
            background: #667eea;
            color: white;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .no-data {
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            margin: 10px 0;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 10px;
            margin-top: 15px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 10px;
            transition: width 0.5s ease;
        }

        .services-list {
            margin-top: 15px;
        }

        .service-item {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #495057;
        }

        .footer {
            background: #343a40;
            color: white;
            padding: 20px 30px;
            text-align: center;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .areas-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 Dashboard de Serviços Terceirizados</h1>
            <p>Gestão e controle de áreas de atuação</p>
            <div class="update-info">
                📅 Última atualização: {timestamp}
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_areas}</div>
                <div class="stat-label">Áreas Cadastradas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_funcionarios}</div>
                <div class="stat-label">Total de Funcionários</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{areas_com_dados}</div>
                <div class="stat-label">Áreas Ativas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_locais}</div>
                <div class="stat-label">Locais Atendidos</div>
            </div>
        </div>

        <div class="areas-section">
            <h2 class="section-title">Áreas de Atuação</h2>
            <div class="areas-grid">
                {areas_cards}
            </div>
        </div>

        <div class="footer">
            🚀 Template de Serviços Terceirizados | Dados carregados automaticamente das planilhas Excel
        </div>
    </div>
</body>
</html>"""

    # Calcular total de locais únicos
    locais_unicos = set()
    for area_info in relatorio['areas'].values():
        for local in area_info['locais_atendidos']:
            locais_unicos.add(local)

    # Gerar cards das áreas
    areas_cards = []
    for chave, area_info in relatorio['areas'].items():
        tem_dados = area_info['total_funcionarios'] > 0
        status_icon = '✅' if tem_dados else '⏳'
        
        if tem_dados:
            # Área com dados
            locations_html = ""
            if area_info['funcionarios_por_local']:
                locations_html = f"""
                <div class="locations-list">
                    <div class="locations-title">📍 Locais de Atuação</div>
                    {''.join([f'''
                    <div class="location-item">
                        <span class="location-name">{local}</span>
                        <span class="location-count">{count}</span>
                    </div>
                    ''' for local, count in area_info['funcionarios_por_local'].items()])}
                </div>
                """
            
            services_html = ""
            if area_info['tipos_servico']:
                services_html = f"""
                <div class="services-list">
                    {''.join([f'<div class="service-item">🔧 {servico}</div>' for servico in area_info['tipos_servico']])}
                </div>
                """
            
            progress = min(100, (area_info['total_funcionarios'] / max(relatorio['resumo_geral']['total_funcionarios'], 1)) * 100)
            
            card_content = f"""
            <div class="area-stats">
                <div class="area-stat">
                    <div class="area-stat-number">{area_info['total_funcionarios']}</div>
                    <div class="area-stat-label">Funcionários</div>
                </div>
                <div class="area-stat">
                    <div class="area-stat-number">{len(area_info['locais_atendidos'])}</div>
                    <div class="area-stat-label">Locais</div>
                </div>
                <div class="area-stat">
                    <div class="area-stat-number">{len(area_info['tipos_servico'])}</div>
                    <div class="area-stat-label">Serviços</div>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress:.1f}%"></div>
            </div>
            {services_html}
            {locations_html}
            """
        else:
            # Área sem dados
            card_content = """
            <div class="no-data">
                📋 Template criado - aguardando preenchimento dos dados<br>
                <small>Preencha o arquivo Excel correspondente para ver os dados aqui</small>
            </div>
            """
        
        area_card = f"""
        <div class="area-card">
            <div class="area-header">
                <div class="area-title">{status_icon} {area_info['nome']}</div>
                <div class="area-description">{area_info['descricao']}</div>
            </div>
            <div class="area-content">
                {card_content}
            </div>
        </div>
        """
        
        areas_cards.append(area_card)

    # Preencher template
    from datetime import datetime
    html_final = html_template.replace("{timestamp}", datetime.now().strftime("%d/%m/%Y às %H:%M"))
    html_final = html_final.replace("{total_areas}", str(relatorio['resumo_geral']['total_areas']))
    html_final = html_final.replace("{total_funcionarios}", str(relatorio['resumo_geral']['total_funcionarios']))
    html_final = html_final.replace("{areas_com_dados}", str(relatorio['resumo_geral']['areas_com_dados']))
    html_final = html_final.replace("{total_locais}", str(len(locais_unicos)))
    html_final = html_final.replace("{areas_cards}", ''.join(areas_cards))
    
    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    print(f"✅ Dashboard HTML criado: {arquivo_saida}")
    print(f"📊 Dados incluídos:")
    print(f"   • {relatorio['resumo_geral']['total_funcionarios']} funcionários")
    print(f"   • {relatorio['resumo_geral']['areas_com_dados']} áreas ativas")
    print(f"   • {len(locais_unicos)} locais únicos")
    
    return arquivo_saida

def gerar_dashboard_json():
    """Gera arquivo JSON para uso em aplicações web"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    relatorio = template.gerar_relatorio_completo()
    
    # Adicionar timestamp
    from datetime import datetime
    relatorio['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    arquivo = "dados_dashboard.json"
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Dados JSON criados: {arquivo}")
    return arquivo

def main():
    """Função principal"""
    print("🚀 Gerando Dashboard HTML...")
    
    # Gerar dashboard HTML com dados reais
    arquivo_html = gerar_dashboard_html()
    
    # Gerar dados JSON
    arquivo_json = gerar_dashboard_json()
    
    print(f"\n🎉 Dashboard pronto!")
    print(f"   📄 HTML: {arquivo_html}")
    print(f"   📄 JSON: {arquivo_json}")
    print(f"\n💡 Para visualizar: Abra o arquivo {arquivo_html} no seu navegador")

if __name__ == "__main__":
    main()