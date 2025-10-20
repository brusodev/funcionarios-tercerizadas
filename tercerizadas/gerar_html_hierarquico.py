"""
Gerador de Template HTML - Estrutura Hierárquica
===============================================

Template HTML que segue a estrutura exata da planilha:
- Título da área
- Descrição do serviço
- Locais agregados em uma linha
- Lista de funcionários indentada
"""

from template_servicos import TemplateServicos
from datetime import datetime
import webbrowser
import os

def gerar_html_estrutura_hierarquica(arquivo_saida="funcionarios_estrutura.html"):
    """Gera HTML seguindo a estrutura hierárquica da planilha"""
    
    # Carregar dados de todas as 4 planilhas
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    # Template HTML base
    html_template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lista de Funcionários - Estrutura Hierárquica</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 40px 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 15px 20px;
            border-radius: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .stat-number {
            font-size: 1.8em;
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
            border-radius: 10px;
            background: white;
            transition: all 0.3s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }

        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #64748b;
        }

        .content {
            padding: 40px;
        }

        .area-section {
            margin-bottom: 50px;
            background: #fafbfc;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        .area-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 30px;
            font-size: 1.8em;
            font-weight: 700;
            text-align: center;
            margin: 0;
        }

        .service-description {
            background: #f1f5f9;
            padding: 20px 30px;
            font-size: 1.1em;
            color: #475569;
            font-style: italic;
            border-bottom: 1px solid #e2e8f0;
        }

        .locations-line {
            background: #e2e8f0;
            padding: 20px 30px;
            font-size: 1em;
            color: #1e293b;
            font-weight: 600;
            border-bottom: 2px solid #cbd5e1;
            word-wrap: break-word;
            line-height: 1.4;
        }

        .employees-section {
            padding: 30px;
        }

        .employees-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .employee-item {
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .employee-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-left-color: #764ba2;
        }

        .employee-number {
            background: #667eea;
            color: white;
            padding: 8px 12px;
            border-radius: 50%;
            font-weight: bold;
            font-size: 0.9em;
            min-width: 40px;
            text-align: center;
        }

        .employee-name {
            font-weight: 600;
            color: #1e293b;
            font-size: 1.1em;
            flex: 1;
        }

        .employee-service {
            color: #059669;
            font-size: 0.9em;
            background: #ecfdf5;
            padding: 5px 10px;
            border-radius: 6px;
            white-space: nowrap;
        }

        .no-data {
            text-align: center;
            padding: 60px 30px;
            color: #64748b;
        }

        .no-data-icon {
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.5;
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
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 20px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
            z-index: 1000;
        }

        .print-btn:hover {
            background: #764ba2;
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        }

        @media print {
            .print-btn, .search-container { display: none; }
            body { background: white; }
            .container { box-shadow: none; }
            .area-section { break-inside: avoid; page-break-inside: avoid; }
            .employees-grid { grid-template-columns: 1fr 1fr; }
        }

        @media (max-width: 768px) {
            .employees-grid {
                grid-template-columns: 1fr;
            }
            
            .stats {
                flex-direction: column;
                gap: 15px;
            }
            
            .employee-item {
                flex-direction: column;
                text-align: center;
                gap: 10px;
            }
            
            .locations-line {
                font-size: 0.9em;
                padding: 15px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Lista de Funcionários</h1>
            <p>Serviços Terceirizados - Estrutura Hierárquica</p>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_funcionarios}</span>
                    <span class="stat-label">Funcionários</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_areas}</span>
                    <span class="stat-label">Áreas Ativas</span>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_locais}</span>
                    <span class="stat-label">Locais Únicos</span>
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
            {areas_html}
        </div>

        <div class="footer">
            <p>📅 Atualizado em: {timestamp}</p>
            <p>💼 Sistema de Gerenciamento de Funcionários Terceirizados</p>
        </div>
    </div>

    <button class="print-btn" onclick="window.print()" title="Imprimir Lista">
        🖨️ Imprimir
    </button>

    <script>
        // Funcionalidade de busca
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const areaSections = document.querySelectorAll('.area-section');
            
            areaSections.forEach(section => {
                const employees = section.querySelectorAll('.employee-item');
                let hasVisibleEmployee = false;
                
                employees.forEach(employee => {
                    const name = employee.querySelector('.employee-name').textContent.toLowerCase();
                    if (name.includes(searchTerm)) {
                        employee.style.display = 'flex';
                        hasVisibleEmployee = true;
                    } else {
                        employee.style.display = 'none';
                    }
                });
                
                // Mostrar/esconder seção baseado se tem funcionários visíveis
                const employeesSection = section.querySelector('.employees-section');
                if (hasVisibleEmployee) {
                    section.style.display = 'block';
                    employeesSection.style.display = 'block';
                } else if (searchTerm) {
                    section.style.display = 'none';
                } else {
                    section.style.display = 'block';
                    employeesSection.style.display = 'block';
                }
            });
        });

        // Animação de entrada
        window.addEventListener('load', function() {
            const sections = document.querySelectorAll('.area-section');
            sections.forEach((section, index) => {
                setTimeout(() => {
                    section.style.opacity = '0';
                    section.style.transform = 'translateY(30px)';
                    section.style.transition = 'all 0.6s ease';
                    
                    setTimeout(() => {
                        section.style.opacity = '1';
                        section.style.transform = 'translateY(0)';
                    }, 100);
                }, index * 200);
            });
        });
    </script>
</body>
</html>"""

    # Processar dados por área (seguindo estrutura hierárquica)
    areas_html = []
    total_funcionarios = 0
    areas_ativas = 0
    todos_locais = set()
    
    for chave, area in template.areas.items():
        if area.funcionarios:  # Só processar áreas com dados
            areas_ativas += 1
            total_funcionarios += len(area.funcionarios)
            
            # Coletar todos os locais únicos desta área
            locais_area = set()
            for funcionario in area.funcionarios:
                locais_funcionario = funcionario.get_locais_lista()
                locais_area.update(locais_funcionario)
                todos_locais.update(locais_funcionario)
            
            # Criar linha de locais agregados (como na planilha)
            locais_linha = '/'.join(sorted(locais_area))
            
            # Gerar HTML dos funcionários
            funcionarios_html = []
            for i, funcionario in enumerate(area.funcionarios, 1):
                funcionario_html = f"""
                <div class="employee-item">
                    <div class="employee-number">#{funcionario.numero}</div>
                    <div class="employee-name">{funcionario.nome}</div>
                    <div class="employee-service">{funcionario.tipo_servico}</div>
                </div>"""
                funcionarios_html.append(funcionario_html)
            
            # HTML da área completa (estrutura hierárquica)
            area_html = f"""
            <div class="area-section">
                <h2 class="area-title">{area.nome}</h2>
                <div class="service-description">{area.descricao}</div>
                <div class="locations-line">{locais_linha}</div>
                <div class="employees-section">
                    <div class="employees-grid">
                        {''.join(funcionarios_html)}
                    </div>
                </div>
            </div>"""
            areas_html.append(area_html)
        
        else:  # Áreas sem dados
            area_html = f"""
            <div class="area-section">
                <h2 class="area-title">⏳ {area.nome}</h2>
                <div class="service-description">{area.descricao}</div>
                <div class="locations-line">Aguardando dados das planilhas</div>
                <div class="no-data">
                    <div class="no-data-icon">📋</div>
                    <p>Dados desta área serão carregados quando a planilha estiver disponível.</p>
                </div>
            </div>"""
            areas_html.append(area_html)
    
    # Montar HTML final
    timestamp = datetime.now().strftime('%d/%m/%Y às %H:%M')
    
    html_final = html_template.replace("{areas_html}", '\n'.join(areas_html))
    html_final = html_final.replace("{total_funcionarios}", str(total_funcionarios))
    html_final = html_final.replace("{total_areas}", str(areas_ativas))
    html_final = html_final.replace("{total_locais}", str(len(todos_locais)))
    html_final = html_final.replace("{timestamp}", timestamp)
    
    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    # Abrir no navegador
    arquivo_completo = os.path.abspath(arquivo_saida)
    webbrowser.open(f'file://{arquivo_completo}')
    
    # Mostrar estatísticas
    print(f"\n✅ Template HTML Estrutura Hierárquica gerado com sucesso!")
    print(f"📄 Arquivo: {arquivo_saida}")
    print(f"🌐 Aberto no navegador automaticamente")
    print(f"\n📊 Estatísticas:")
    print(f"   • {total_funcionarios} funcionários")
    print(f"   • {areas_ativas} áreas ativas")
    print(f"   • {len(todos_locais)} locais únicos")
    
    print(f"\n🏢 Áreas processadas:")
    for chave, area in template.areas.items():
        if area.funcionarios:
            print(f"   ✅ {area.nome}: {len(area.funcionarios)} funcionários")
        else:
            print(f"   ⏳ {area.nome}: Aguardando dados")
    
    return arquivo_saida

if __name__ == "__main__":
    gerar_html_estrutura_hierarquica()