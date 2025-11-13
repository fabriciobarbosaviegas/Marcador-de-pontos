# Marcador de Pontos

Uma interface simples para geocodificar endereços presentes em um arquivo .ods e gerar um CSV com coordenadas.

Como usar

- Requisitos (instalar as dependências):

  - Python 3.8+
  - Instalar dependências listadas em `requirements.txt` (por exemplo: `pip install -r requirements.txt`).

- Modo CLI:

  - Edite `main.py` se necessário e execute:

    python main.py

  - Por padrão ele tentará processar o arquivo `sample/Cópia de Atividade 1 PET.ods`.

- Modo GUI:

  - Execute a interface gráfica:

    python gui.py

  - Use o botão "Selecionar" para escolher o arquivo .ods, defina o nome do arquivo de saída e clique em "Iniciar".

Notas

- A geocodificação usa o serviço Nominatim (OpenStreetMap). Respeite as políticas de uso e limites de taxa.
- Este é um exemplo simples; para grandes quantidades de endereços, considere adicionar caching e respeitar limites de requisições.
