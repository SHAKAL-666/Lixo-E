# Instalação da IA (TensorFlow) — Instruções

## Opção A: Rodar no Docker (Recomendado)

Se o Docker e Docker Desktop estão instalados:

1. Inicie o Docker Desktop
2. Na pasta do projeto, execute:

```bash
docker compose build --no-cache
docker compose up
```

A aplicação estará disponível em `http://localhost:8000` com suporte completo a classificação automática de imagens via TensorFlow.

### Como funciona:
- O container usa **Python 3.11** com **TensorFlow CPU 2.14.0**
- As imagens são automaticamente classificadas nas 8 categorias de lixo eletrônico
- Explicações detalhadas são geradas automaticamente para cada categoria

---

## Opção B: Instalação Local (Windows)

### Pré-requisitos
- Python 3.11 ou 3.12 (não 3.14.6, pois não há wheels TF compatíveis)
- Gerenciador de pacotes `pip` atualizado

### Passos

1. **Baixe e instale Python 3.11**
   - Acesse https://www.python.org/downloads/release/python-3114/
   - Marque "Add Python 3.11 to PATH" durante a instalação

2. **Crie um novo ambiente virtual com Python 3.11**
   ```bash
   C:\Users\Dev2\AppData\Local\Python\Python311\python.exe -m venv .venv-tf
   .venv-tf\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **Execute o app com TensorFlow habilitado**
   ```bash
   python app.py
   ```

---

## Opção C: Usar Google Colab (Cloud)

Se prefere não instalar localmente, use Google Colab:

1. Acesse https://colab.research.google.com
2. Abra um novo notebook
3. Cole este código:

```python
!pip install tensorflow flask pillow imagehash
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights='imagenet')
# Teste com uma imagem local
img = image.load_img('seu_arquivo.jpg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)
preds = model.predict(x)
print(decode_predictions(preds, top=3)[0])
```

---

## Categorização Automática

A IA classifica imagens em uma destas 8 categorias:

- **Equipamentos de informática**: Computadores, notebooks, monitores, impressoras
- **Dispositivos de comunicação**: Celulares, modems, roteadores
- **Equipamentos de áudio e vídeo**: TVs, caixas de som, câmeras
- **Pilhas e baterias**: Pilhas, baterias recarregáveis, baterias de lítio
- **Carregadores e cabos**: Carregadores, cabos USB, adaptadores
- **Eletrodomésticos eletrônicos**: Micro-ondas, liquidificadores, ferros
- **Equipamentos de iluminação**: Lâmpadas, luminárias, LEDs
- **Componentes eletrônicos**: Placas, chips, resistores, capacitores

---

## Status Atual

✅ Código da IA já está integrado em `app.py` com mapeamento de categorias
✅ Dockerfile configurado com Python 3.11 + TensorFlow
✅ Docker Compose pronto para build
⏳ Aguardando Docker Desktop estar ativo para construir e testar

### Próximos passos:
1. Inicie o Docker Desktop
2. Execute `docker compose build --no-cache && docker compose up`
3. Teste upload de imagem em http://localhost:8000
4. Verifique categorização automática no resultado
