#!/usr/bin/env python3
"""
Script para atualizar o index.html com as seções geradas
"""

import re
from pathlib import Path

# Configurações de caminhos
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
BACKUP_DIR = PROJECT_ROOT / "backup"

def update_index_html():
    """Atualiza o index.html com as seções mais recentes"""

    # Arquivos
    index_file = SRC_DIR / "index.html"
    sections_file = BACKUP_DIR / "sections_generated_latest.html"

    # Verificar se os arquivos existem
    if not index_file.exists():
        print(f"❌ Arquivo index.html não encontrado: {index_file}")
        return False

    if not sections_file.exists():
        print(f"❌ Arquivo de seções não encontrado: {sections_file}")
        print("Execute primeiro: python scripts/generate_html_from_excel.py")
        return False

    # Ler o conteúdo dos arquivos
    with open(index_file, 'r', encoding='utf-8') as f:
        index_content = f.read()

    with open(sections_file, 'r', encoding='utf-8') as f:
        sections_content = f.read()

    # Criar backup do arquivo atual
    import shutil
    from datetime import datetime
    backup_file = BACKUP_DIR / f"index_before_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    shutil.copy2(index_file, backup_file)
    print(f"📦 Backup criado: {backup_file}")

    # Encontrar onde inserir as seções (antes do footer)
    footer_pattern = r'(\s*<div class="footer">)'
    match = re.search(footer_pattern, index_content)

    if not match:
        print("❌ Não foi possível encontrar o local de inserção no index.html")
        return False

    # Remover seções existentes (entre o mainContent e o footer)
    # Padrão para encontrar o início das seções (após o mainContent)
    content_start_pattern = r'(\s*<div class="content" id="mainContent">\s*)'
    content_match = re.search(content_start_pattern, index_content)

    if content_match:
        # Remover todo o conteúdo entre o início do mainContent e o início do footer
        start_pos = content_match.end(1)
        end_pos = match.start(1)
        updated_content = (
            index_content[:start_pos] +
            sections_content +
            index_content[end_pos:]
        )
        print("✅ Seções antigas removidas e novas inseridas")
    else:
        # Fallback: apenas inserir antes do footer (pode causar duplicatas)
        print("⚠️  Não foi possível encontrar o início do mainContent, inserindo apenas antes do footer")
        updated_content = (
            index_content[:match.start(1)] +
            sections_content +
            index_content[match.start(1):]
        )

    # Salvar o arquivo atualizado
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✅ index.html atualizado com sucesso!")
    print(f"📊 Seções inseridas no arquivo: {SRC_DIR / 'index.html'}")

    return True

def main():
    print("🔄 Atualizando index.html com dados das planilhas...")
    print("=" * 50)

    if update_index_html():
        print("\n🎉 Atualização concluída!")
        print("Abra src/index.html no navegador para ver os resultados.")
    else:
        print("\n❌ Falha na atualização.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())