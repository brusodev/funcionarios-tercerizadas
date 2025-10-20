"""
Gerador Unificado de Templates HTML
==================================

Menu para escolher entre diferentes tipos de templates HTML para funcionários.
"""

from gerar_html_funcionarios import gerar_html_funcionarios
from gerar_html_simples import gerar_html_simples
import webbrowser
from pathlib import Path

def abrir_arquivo_no_navegador(arquivo):
    """Abre arquivo HTML no navegador"""
    try:
        caminho_absoluto = Path(arquivo).absolute()
        url = f"file:///{caminho_absoluto}".replace("\\", "/")
        webbrowser.open(url)
        print(f"🌐 Arquivo {arquivo} aberto no navegador!")
        return True
    except Exception as e:
        print(f"❌ Erro ao abrir: {e}")
        print(f"💡 Abra manualmente: {arquivo}")
        return False

def menu_templates_html():
    """Menu para escolher tipo de template HTML"""
    print("\n" + "="*70)
    print("🌐 GERADOR DE TEMPLATES HTML - LISTA DE FUNCIONÁRIOS")
    print("="*70)
    print()
    print("Escolha o tipo de template HTML:")
    print()
    print("1. 🎨 Template Completo (Moderno)")
    print("   • Design profissional com gradientes")
    print("   • Cards interativos por local")
    print("   • Busca em tempo real")
    print("   • Estatísticas detalhadas")
    print("   • Pronto para impressão")
    print()
    print("2. 📋 Template Simples (Focado)")
    print("   • Design limpo e direto")
    print("   • Lista organizada por área/local")
    print("   • Busca de funcionários")
    print("   • Ideal para consulta rápida")
    print()
    print("3. 🏢 Template Agregado (4 Planilhas)")
    print("   • Carrega TODAS as 4 planilhas")
    print("   • Locais agregados automaticamente")
    print("   • 266 funcionários organizados")
    print("   • 35 locais únicos")
    print()
    print("4. � Template Hierárquico (Estrutura da Planilha)")
    print("   • Segue estrutura EXATA da planilha")
    print("   • Título → Descrição → Locais → Funcionários")
    print("   • Layout idêntico ao Excel")
    print("   • Organização visual perfeita")
    print()
    print("5. �🚀 Gerar Todos")
    print("   • Cria todos os templates")
    print("   • Abre todos no navegador")
    print()
    print("0. ❌ Sair")
    print()
    
    while True:
        try:
            opcao = input("Digite sua opção (0-5): ").strip()
            
            if opcao == "1":
                print("\n🎨 Gerando Template Completo...")
                arquivo = gerar_html_funcionarios("funcionarios_completo.html")
                abrir_arquivo_no_navegador(arquivo)
                break
                
            elif opcao == "2":
                print("\n📋 Gerando Template Simples...")
                arquivo = gerar_html_simples("funcionarios_simples.html")
                abrir_arquivo_no_navegador(arquivo)
                break
                
            elif opcao == "3":
                print("\n🏢 Gerando Template Agregado...")
                from gerar_html_agregado import gerar_html_agregado
                arquivo = gerar_html_agregado("funcionarios_agregado.html")
                break
                
            elif opcao == "4":
                print("\n� Gerando Template Hierárquico...")
                from gerar_html_hierarquico import gerar_html_estrutura_hierarquica
                arquivo = gerar_html_estrutura_hierarquica("funcionarios_hierarquico.html")
                break
                
            elif opcao == "5":
                print("\n�🚀 Gerando Todos os Templates...")
                print("\n1/4 - Template Completo:")
                arquivo1 = gerar_html_funcionarios("funcionarios_completo.html")
                print("\n2/4 - Template Simples:")
                arquivo2 = gerar_html_simples("funcionarios_simples.html")
                print("\n3/4 - Template Agregado:")
                from gerar_html_agregado import gerar_html_agregado
                arquivo3 = gerar_html_agregado("funcionarios_agregado.html")
                print("\n4/4 - Template Hierárquico:")
                from gerar_html_hierarquico import gerar_html_estrutura_hierarquica
                arquivo4 = gerar_html_estrutura_hierarquica("funcionarios_hierarquico.html")
                
                print(f"\n✅ Todos os templates criados!")
                print(f"   📄 {arquivo1}")
                print(f"   📄 {arquivo2}")
                print(f"   📄 {arquivo3}")
                print(f"   📄 {arquivo4}")
                
                # Abrir todos
                abrir_arquivo_no_navegador(arquivo1)
                abrir_arquivo_no_navegador(arquivo2)
                break
                
            elif opcao == "0":
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida. Digite um número de 0 a 5.")
                
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break

def gerar_template_direto(tipo="completo"):
    """Gera template diretamente sem menu"""
    if tipo == "completo":
        return gerar_html_funcionarios()
    elif tipo == "simples":
        return gerar_html_simples()
    elif tipo == "agregado":
        from gerar_html_agregado import gerar_html_agregado
        return gerar_html_agregado()
    elif tipo == "hierarquico":
        from gerar_html_hierarquico import gerar_html_estrutura_hierarquica
        return gerar_html_estrutura_hierarquica()
    else:
        print("❌ Tipo inválido. Use 'completo', 'simples', 'agregado' ou 'hierarquico'")
        return None

if __name__ == "__main__":
    import sys
    
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1:
        tipo = sys.argv[1].lower()
        if tipo in ["completo", "simples", "agregado", "hierarquico"]:
            print(f"🚀 Gerando template {tipo}...")
            arquivo = gerar_template_direto(tipo)
            if arquivo:
                abrir_arquivo_no_navegador(arquivo)
        else:
            print("❌ Uso: python gerar_templates_html.py [completo|simples]")
    else:
        # Mostrar menu interativo
        menu_templates_html()