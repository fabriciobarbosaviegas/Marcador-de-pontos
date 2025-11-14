# 🗺️ Marcador de Pontos — Geocodificação Automática para Google My Maps

* [📥 Entrada](#-entrada)
* [📤 Saída](#-saída)
* [🛠️ Instalação](#️-instalação)
* [▶️ Como Executar](#️-como-executar)
* [📄 Estrutura do Projeto](#-estrutura-do-projeto)
* [⚙️ Funcionamento Interno](#️-funcionamento-interno)

  * [main.py](#mainpy)
  * [utils.py](#utilspy)
* [📍 Importando no Google My Maps](#-importando-no-google-my-maps)
* [⚠️ Limitações](#️-limitações)

Este projeto permite **converter endereços de uma planilha ODS em coordenadas geográficas**, gerando um arquivo CSV importável no **Google My Maps**.

A ferramenta lê a coluna **“Endereço”** de todas as abas da planilha, encontra latitude e longitude via *geocoding* (Nominatim / OpenStreetMap) e gera um CSV contendo:

* **Coluna `WKT`** → `(longitude latitude)`
* **Coluna `Endereço`** → texto original do endereço

Inclui ainda uma **interface gráfica (GUI)** desenvolvida em Tkinter permitindo uso por qualquer pessoa sem necessidade de terminal.

---

## 📥 Entrada

Arquivo **ODS** com ao menos uma coluna:

```
Endereço
Rua Exemplo, 123
Av. Teste, 45
...
```

A ferramenta automaticamente acrescenta:

```
, Pelotas - RS
```

*(pode ser modificado no código)*

---

## 📤 Saída

Arquivo CSV:

| WKT                  | Endereço                       |
| -------------------- | ------------------------------ |
| ( -52.1234 -31.987 ) | Rua Exemplo, 123, Pelotas - RS |

O arquivo é importável diretamente no **Google My Maps**.

---

## 🛠️ Instalação

### 1. Clone o repositório (ou faça o download)

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```
---

## ▶️ Como Executar

```bash
python main.py
```

A interface gráfica será aberta.

---

## 📄 Estrutura do Projeto

```
/
├── main.py          # Interface gráfica
├── utils.py         # Lógica principal de leitura e geocodificação
├── README.md
└── requirements.txt
```

---

## ⚙️ Funcionamento Interno

### **main.py**

* Tkinter GUI
* Thread para processamento assíncrono
* Log em tempo real
* Barra de progresso dinâmica
* Permite abrir o CSV gerado

### **utils.py**

* `process_ods_file`

  * Lê todas as abas da planilha
  * Extrai coluna “Endereço”

* `get_coordinates_from_address`

  * Consulta geocoding no Nominatim
  * 3 tentativas com backoff

* `process_file`

  * Cria CSV
  * Escreve coluna `WKT` com `(longitude latitude)`
  * Retorna número de erros e lista de endereços falhados

---

## 📍 Importando no Google My Maps

1. Abra o Google My Maps
2. Crie um novo mapa (Para um mapa existente crie uma nova camada)
3. Clique em *“Importar”*
4. Selecione o CSV gerado
5. Escolha **WKT** como coluna de localização
6. Use **Endereço** como rótulo

---

## ⚠️ Limitações

* Endereços incompletos podem retornar `None`
* Pode ser necessário limpar caracteres especiais ou abreviações confusas



Aqui está o **README revisado com uma Table of Contents** totalmente funcional e clicável (links automáticos do GitHub):

---
