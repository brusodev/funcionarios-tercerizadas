#!/usr/bin/env python3
"""
Script de configuração inicial do Sistema de Funcionários Terceirizados
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 ou superior é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_requirements():
    """Instala as dependências do Python"""
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        print("📦 Instalando dependências Python...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependências instaladas com sucesso")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar dependências")
            return False
    else:
        print("⚠️ Arquivo requirements.txt não encontrado")
        return False

def check_data_files():
    """Verifica se os arquivos de dados existem"""
    data_dir = Path("data")
    if not data_dir.exists():
        print("❌ Pasta 'data' não encontrada")
        return False

    excel_files = list(data_dir.glob("*.xlsx"))
    if not excel_files:
        print("❌ Nenhum arquivo Excel encontrado na pasta 'data'")
        return False

    print(f"✅ {len(excel_files)} arquivos Excel encontrados")
    return True

def check_main_files():
    """Verifica se os arquivos principais existem"""
    required_files = [
        "src/index.html",
        "scripts/generate_html_from_excel.py",
        "README.md"
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Arquivos necessários não encontrados: {', '.join(missing_files)}")
        return False

    print("✅ Todos os arquivos principais encontrados")
    return True

def main():
    """Função principal de configuração"""
    print("🚀 Configurando Sistema de Funcionários Terceirizados")
    print("=" * 50)

    # Verificações
    checks = [
        ("Verificando versão do Python", check_python_version),
        ("Verificando arquivos principais", check_main_files),
        ("Verificando arquivos de dados", check_data_files),
        ("Instalando dependências", install_requirements)
    ]

    all_passed = True
    for description, check_func in checks:
        print(f"\n{description}...")
        if not check_func():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Configuração concluída com sucesso!")
        print("\nPara executar o sistema:")
        print("1. Execute: python scripts/generate_html_from_excel.py")
        print("2. Abra src/index.html no navegador")
    else:
        print("❌ Configuração falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()