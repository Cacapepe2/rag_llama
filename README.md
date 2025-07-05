# RAG Técnico Telecom (LlamaIndex + Streamlit)

Este app permite fazer perguntas técnicas sobre dados de rede usando RAG com documentos PDF, CSV, TXT e vídeos do YouTube.

## Funcionalidades
- Upload de CSV (com encoding automático)
- Upload de PDF, TXT
- Transcrição automática de vídeos do YouTube (via Whisper)
- Perguntas respondidas via LlamaIndex (com embeddings HuggingFace)
- Proteção por senha (via variável de ambiente)

## Como rodar no Render

1. Crie um novo Web Service
2. Faça deploy a partir deste repositório
3. Configure as variáveis de ambiente:
   - `APP_SENHA=suasenha`
4. Use o comando de inicialização:
   ```
   bash startup.sh
   ```

> Ideal para arquivos pequenos/médios no plano gratuito do Render (512MB RAM).
