# Guia de Testes — E-Lixo com IA

## 1. Teste Local Rápido (sem Docker)

Se quiser testar o app sem TensorFlow (rápido):

```bash
# Ativar ambiente local
.venv-1\Scripts\activate

# Rodar Flask
python app.py

# Abrir navegador
http://localhost:8000
```

**Funcionalidades disponíveis**: Upload, detecção de duplicatas (pHash), catálogo, admin

**IA desabilitada**: Sem sugestão automática (TensorFlow não instalado localmente)

---

## 2. Teste Docker com IA (recomendado)

Quando `docker compose build` terminar:

```bash
# Iniciar container
docker compose up

# Abrir navegador
http://localhost:8000
```

**O que você verá**:
- ✅ Upload funciona
- ✅ IA automática classifica imagens
- ✅ Categoria e explicação aparecem
- ✅ Botão "Usar IA" preenchE a categoria

**Tempo esperado**: Build = 5-10 min (TensorFlow é grande), Container = segundos

---

## 3. Script de Teste de IA Local

Se quiser testar a função `try_classify()` localmente com uma imagem:

```bash
# Com TensorFlow instalado (Python 3.11):
python test_ai_locally.py uploads/seu_arquivo.jpg

# Ou com arquivo de teste:
python test_ai_locally.py tests/test_upload.jpg
```

**Saída esperada**:
```
🔍 Testando classificação de IA em: uploads/test.jpg
---
✅ Classificação bem-sucedida!

  Label (ImageNet):    cellular telephone
  Confiança:            0.87
  Categoria:            Dispositivos de comunicação

  Explicação:
    Celulares, modems, roteadores e outros dispositivos...
```

---

## 4. Fluxo de Upload com IA no Navegador

**Home** (`/`):
1. Clique em "Selecionar arquivo" ou tire uma foto (câmera)
2. Aguarde análise (alguns segundos para IA)
3. Veja o resultado:
   - **Se duplicada**: Mostra categoria já conhecida
   - **Se nova**: Mostra sugestão da IA + botão "Usar IA"
4. Clique "Usar IA" para aceitar sugestão ou escolha manual
5. Clique "Enviar" para catalogar

**Catálogo** (`/catalogs`):
- Lista todas as imagens catalogadas
- Cada uma com categoria, explicação e ID

**Admin** (`/admin`):
- Login: `admin` / `password` (ou env vars)
- Visualiza/deleta itens
- CORS da sessão mantida

---

## 5. Imagens de Teste Recomendadas

Para ver a IA funcionando bem, teste com:

- **Celular / Smartphone**: → Dispositivos de comunicação
- **Notebook / Laptop**: → Equipamentos de informática
- **Lâmpada / LED**: → Equipamentos de iluminação
- **Bateria / Pilha**: → Pilhas e baterias
- **Carregador / Cabo USB**: → Carregadores e cabos
- **TV / Televisor**: → Equipamentos de áudio e vídeo
- **Micro-ondas**: → Eletrodomésticos eletrônicos
- **Placa mãe / Circuit board**: → Componentes eletrônicos

---

## 6. Troubleshooting

### Docker build travado?
```bash
# Cancelar (Ctrl+C) e recomeçar
docker compose build --no-cache --progress=plain

# Ou verificar status:
docker ps -a
docker logs <container_id>
```

### TensorFlow não encontrado?
- Você está usando Python 3.11+? (localmente exige 3.11 mínimo)
- Docker vai ter automaticamente
- Ou instale: `pip install tensorflow-cpu==2.14.0`

### IA não responde rápido?
- Normal: primeira execução carrega o modelo (~3-5s)
- Próximas são mais rápidas (modelo em cache)

### Upload falha?
- Verifique permissões em `/uploads`
- Use PNG/JPG/JPEG/GIF/BMP
- Arquivo < 10MB

---

## 7. Verificar Funcionamento da IA

**Verificar se TensorFlow está no container**:
```bash
docker exec -it e-lixo-web-1 python -c "import tensorflow; print(tensorflow.__version__)"
# Saída esperada: 2.14.0
```

**Testar classificação dentro do container**:
```bash
docker exec -it e-lixo-web-1 python test_ai_locally.py uploads/test.jpg
```

---

## 8. Performance Esperada

| Operação | Tempo | Notas |
|----------|-------|-------|
| Upload imagem | <1s | Até 10 MB |
| pHash (duplicatas) | <1s | Hash rápido |
| IA (TensorFlow) | 3-5s | Primeira vez; 1-2s depois |
| Detectar duplicata | <1s | Comparação com BD |
| **Total upload + análise** | **~4-6s** | Com IA habilitada |

---

## 9. Dados Persistem?

- ✅ `uploads/`: imagens salvas no container
- ✅ `data/images.db`: SQLite persiste
- ⚠️ Com `docker compose up`: dados perdidos se `docker compose down`
- ✅ Use `docker volume` para persistência permanente

---

## Próximas Melhorias

- [ ] API REST completa
- [ ] Exportação (CSV, JSON)
- [ ] Dashboard com estatísticas
- [ ] Detecção de cores/materiais
- [ ] Histórico de uploads
- [ ] Autenticação com senhas hasheadas (bcrypt)
