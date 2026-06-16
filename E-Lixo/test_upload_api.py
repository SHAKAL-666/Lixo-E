import requests
import json

print("[1] Testando upload de imagem...")
with open('uploads/test_colored.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://127.0.0.1:8000/upload', files=files)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Se sucesso, extrair filename e fazer segundo upload
    if response.status_code == 200:
        data = response.json()
        filename = data.get('filename')
        phash = data.get('phash')
        print(f"\n[2] Catalogando imagem...")
        print(f"  Filename: {filename}")
        print(f"  pHash: {phash[:20]}...")
        
        catalog_response = requests.post(
            'http://127.0.0.1:8000/catalog',
            json={
                'filename': filename,
                'phash': phash,
                'category': 'Equipamentos de informática',
                'explanation': 'Imagem de teste E-Lixo'
            }
        )
        print(f"Catálogo status: {catalog_response.status_code}")
        print(json.dumps(catalog_response.json(), indent=2))
        
        print("\n✅ Upload e catalogação bem-sucedidos!")
    else:
        print("❌ Upload falhou. Verificando arquivo...")
        import os
        files_list = os.listdir('uploads')
        print(f"Arquivos em uploads/: {files_list[:5]}")
