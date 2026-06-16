# Catalogador de Lixo Eletrônico (protótipo)

Protótipo de aplicação web para catalogar imagens de lixo eletrônico, detectar duplicatas e classificar automaticamente com IA.

## Funcionalidades principais

- **Upload de imagens**: suporte a câmera de smartphone e seleção de arquivo
- **Detecção de duplicatas**: usando pHash para encontrar imagens já conhecidas
- **Classificação automática com IA** (TensorFlow MobileNetV2): classifica automaticamente em 8 categorias
- **Armazenamento**: imagens em `uploads/`, metadados em SQLite (`data/images.db`)
- **Painel administrativo**: visualizar, remover e gerenciar itens do catálogo
- **Visual moderno**: tema escuro com glassmorphism e responsivo

## Categorias de lixo eletrônico

1. **Equipamentos de informática**: Computadores, notebooks, monitores, impressoras
2. **Dispositivos de comunicação**: Celulares, modems, roteadores
3. **Equipamentos de áudio e vídeo**: Televisores, caixas de som, câmeras
4. **Pilhas e baterias**: Pilhas, baterias recarregáveis, baterias de lítio
5. **Carregadores e cabos**: Carregadores, cabos USB, adaptadores
6. **Eletrodomésticos eletrônicos**: Micro-ondas, liquidificadores, ferros elétricos
7. **Equipamentos de iluminação**: Lâmpadas, luminárias, LEDs
8. **Componentes eletrônicos**: Placas, chips, resistores, capacitores

## Como executar

### Opção 1: Docker (recomendado com IA)

```bash
docker compose build --no-cache
docker compose up
# Acesse http://localhost:8000
```

Requer Docker Desktop ativo. A IA estará habilitada automaticamente.

### Opção 2: Ambiente local (sem IA, rápido)

```bash
.venv-1\Scripts\activate
python app.py
# Acesse http://localhost:8000
```

**Nota**: TensorFlow não está instalado no ambiente local (Python 3.14.6 não tem wheels compatíveis). Use Docker para IA.

### Opção 3: Instalar IA localmente

1. Instale Python 3.11
2. Crie novo venv: `python3.11 -m venv .venv-tf`
3. Ative: `.venv-tf\Scripts\activate`
4. Instale: `pip install -r requirements.txt`
5. Execute: `python app.py`

## Fluxo de uso

1. **Upload**: Envie uma imagem ou tire uma foto com a câmera
2. **Análise automática**: O app verifica se é uma imagem duplicada
3. **Sugestões**: 
   - Se duplicada, mostra a categoria já conhecida
   - Se nova, oferece sugestões de categoria (pHash + IA)
4. **Catalogação**: Escolha a categoria ou aceite a sugestão da IA
5. **Armazenamento**: Imagem é guardada com metadados

## Autenticação

- Admin login: `admin` / `password` (pode mudar com env vars)
  - `E_LIXO_ADMIN_USER`
  - `E_LIXO_ADMIN_PASS`

## Estrutura do projeto

```
.
├── app.py                 # Backend Flask principal
├── requirements.txt       # Dependências Python
├── Dockerfile            # Para rodar em container
├── docker-compose.yml    # Orquestração Docker
├── templates/
│   ├── base.html         # Template base (nav, footer, estilo)
│   ├── index.html        # Home (upload)
│   ├── catalogs.html     # Visualização do catálogo
│   ├── admin.html        # Painel admin
│   └── login.html        # Login admin
├── data/                 # Banco SQLite
├── uploads/              # Imagens armazenadas
└── tests/
    └── run_tests.py      # Testes automatizados
```

## Próximos passos possíveis

- ✅ IA automática com TensorFlow
- ✅ Visual renovado e moderno
- Persistência de usuários admin (bcrypt, BD)
- Melhorias em performance (cache, índices)
- API REST completa
- Dashboard com estatísticas
- Exportação de dados (CSV, JSON)

## Requisitos

- Python 3.11+ (para IA) ou 3.14+ (sem IA)
- Flask 2.2.5
- Pillow, imagehash, requests
- TensorFlow CPU 2.14 (Docker ou Python 3.11)

## Licença

Protótipo. Uso livre para fins de aprendizado.
