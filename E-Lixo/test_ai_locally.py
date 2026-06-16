#!/usr/bin/env python3
"""
Quick test script for trying TensorFlow classification locally without Docker.
This tests the try_classify() function with a sample image.

Usage: 
  python test_ai_locally.py path/to/image.jpg
"""

import sys
import os

# Add app module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import try_classify, CATEGORY_EXPLANATIONS, LABEL_TO_CATEGORY

def test_image(image_path):
    """Test classification on a single image."""
    if not os.path.exists(image_path):
        print(f"❌ Imagem não encontrada: {image_path}")
        return False
    
    print(f"🔍 Testando classificação de IA em: {image_path}")
    print("-" * 60)
    
    result = try_classify(image_path)
    
    if result is None:
        print("⚠️ TensorFlow não está disponível ou falhou na classificação.")
        print("💡 Para instalar:")
        print("   - Opção 1: Use Docker (recomendado)")
        print("   - Opção 2: pip install tensorflow-cpu==2.14.0")
        return False
    
    print(f"✅ Classificação bem-sucedida!")
    print()
    print(f"  Label (ImageNet):    {result.get('label', 'N/A')}")
    print(f"  Confiança:            {result.get('confidence', 'N/A'):.1%}")
    print(f"  Categoria:            {result.get('category', 'N/A')}")
    print()
    print(f"  Explicação:")
    explanation = result.get('explanation', 'Sem explicação')
    for line in explanation.split('\n'):
        print(f"    {line}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python test_ai_locally.py <caminho_da_imagem>")
        print()
        print("Exemplos:")
        print("  python test_ai_locally.py uploads/test.jpg")
        print("  python test_ai_locally.py tests/test_upload.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_image(image_path)
    sys.exit(0 if success else 1)
