# Catalogador de Lixo Eletrônico (protótipo)

Protótipo de aplicação web para catalogar imagens de lixo eletrônico e detectar duplicatas. O app grava imagens enviadas e usa pHash para identificar imagens já conhecidas; quando desconhecida, pede que o usuário escolha uma categoria e envie uma explicação.

Funcionalidades:
- Upload de imagens e suporte a captura via câmera em smartphones (input `capture="environment"`).
- Detecção de imagens duplicadas por pHash.
- Armazenamento de imagem em `uploads/` e metadados em banco SQLite (`data/images.db`).

Categorias padrão:
- Equipamentos de informática
- Dispositivos de comunicação
- Equipamentos de áudio e vídeo
- Pilhas e baterias
- Carregadores e cabos
- Eletrodomésticos eletrônicos
- Equipamentos de iluminação
- Componentes eletrônicos

Como rodar (Windows):

1. Criar e ativar um ambiente virtual (opcional mas recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Rodar o servidor:

```powershell
python app.py
```

4. Abrir no navegador: http://localhost:8000

Para ver os itens cadastrados acesse: http://localhost:8000/catalogs

Notas:
- Este é um protótipo simples que usa comparação por pHash. Conforme o catálogo crescer, a detecção automática ficará mais eficaz.
- Próximos passos possíveis: integrar um modelo de visão computacional para classificação automática, otimizar banco para buscas por similaridade, adicionar autenticação de usuários.
