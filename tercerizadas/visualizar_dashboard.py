"""
Visualizador de Dashboard - Abre automaticamente no navegador
===========================================================

Script para gerar e abrir o dashboard HTML no navegador padrão.
"""

import webbrowser
import os
from pathlib import Path
from gerar_dashboard import gerar_dashboard_html, gerar_dashboard_json

def abrir_dashboard():
    """Gera e abre o dashboard no navegador"""
    print("🚀 Preparando dashboard...")
    
    # Gerar dashboard atualizado
    arquivo_html = gerar_dashboard_html("dashboard_dinamico.html")
    
    # Caminho absoluto do arquivo
    caminho_absoluto = Path(arquivo_html).absolute()
    url = f"file:///{caminho_absoluto}".replace("\\", "/")
    
    print(f"🌐 Abrindo dashboard no navegador...")
    print(f"   📄 Arquivo: {caminho_absoluto}")
    
    try:
        # Abrir no navegador padrão
        webbrowser.open(url)
        print("✅ Dashboard aberto com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print(f"💡 Abra manualmente o arquivo: {caminho_absoluto}")

def criar_atalho_dashboard():
    """Cria um arquivo batch para facilitar o acesso"""
    batch_content = f"""@echo off
echo 🚀 Atualizando dashboard...
cd /d "{Path.cwd()}"
"{Path.cwd()}/.venv/Scripts/python.exe" visualizar_dashboard.py
pause
"""
    
    with open("Abrir_Dashboard.bat", "w", encoding="utf-8") as f:
        f.write(batch_content)
    
    print("📋 Atalho criado: Abrir_Dashboard.bat")
    print("💡 Dica: Clique duas vezes no arquivo .bat para abrir o dashboard rapidamente")

def menu_opcoes():
    """Menu interativo para o usuário"""
    print("\n" + "="*60)
    print("🏢 VISUALIZADOR DE DASHBOARD - SERVIÇOS TERCEIRIZADOS")
    print("="*60)
    print()
    print("Escolha uma opção:")
    print("1. 🌐 Gerar e abrir dashboard no navegador")
    print("2. 📄 Apenas gerar arquivos HTML e JSON")
    print("3. 📋 Criar atalho (.bat) para acesso rápido")
    print("4. 🔄 Ver status atual dos dados")
    print("0. ❌ Sair")
    print()
    
    while True:
        try:
            opcao = input("Digite sua opção (0-4): ").strip()
            
            if opcao == "1":
                abrir_dashboard()
                break
            elif opcao == "2":
                gerar_dashboard_html()
                gerar_dashboard_json()
                break
            elif opcao == "3":
                criar_atalho_dashboard()
                break
            elif opcao == "4":
                mostrar_status()
                break
            elif opcao == "0":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite um número de 0 a 4.")
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break

def mostrar_status():
    """Mostra status atual dos dados"""
    from template_servicos import TemplateServicos
    
    print("\n📊 STATUS ATUAL DOS DADOS")
    print("-" * 40)
    
    template = TemplateServicos()
    template.carregar_todos_dados()
    relatorio = template.gerar_relatorio_completo()
    
    print(f"📈 Resumo geral:")
    print(f"   • Total de áreas: {relatorio['resumo_geral']['total_areas']}")
    print(f"   • Total de funcionários: {relatorio['resumo_geral']['total_funcionarios']}")
    print(f"   • Áreas ativas: {relatorio['resumo_geral']['areas_com_dados']}")
    
    print(f"\n🏢 Status por área:")
    for chave, area_info in relatorio['areas'].items():
        status = "✅ Ativa" if area_info['total_funcionarios'] > 0 else "⏳ Aguardando dados"
        print(f"   • {area_info['nome']}: {status} ({area_info['total_funcionarios']} funcionários)")
    
    # Verificar arquivos
    print(f"\n📁 Arquivos disponíveis:")
    arquivos_importantes = [
        "manutencao_predios.xlsx",
        "servicos_copas.xlsx", 
        "template_seguranca_acesso.xlsx",
        "template_transporte.xlsx",
        "dashboard_dinamico.html",
        "dados_dashboard.json"
    ]
    
    for arquivo in arquivos_importantes:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} (não encontrado)")

if __name__ == "__main__":
    # Verificar se é execução direta ou com argumentos
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--direto":
        # Abrir direto sem menu
        abrir_dashboard()
    else:
        # Mostrar menu
        menu_opcoes()