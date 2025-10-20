# TinyTroupe + FastAPI (POC mínima)

POC mínima para validar a biblioteca [TinyTroupe](https://github.com/microsoft/TinyTroupe) com FastAPI.

Objetivo:
- Criar personas (manual e via TinyPersonFactory)
- Rodar uma simulação curta com TinyWorld
- Healthcheck

Sem Docker, sem frontend, sem testes automáticos.

## Estrutura

```
tiny-troupe-persona/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ config.ini
└─ app/
   ├─ main.py        # FastAPI + endpoints
   ├─ personas.py    # TinyPerson manual + TinyPersonFactory
   └─ simulate.py    # TinyWorld run (2–3 steps)
```

## Requisitos

- Python 3.10+
- Windows (com PowerShell)
- Uma chave de API válida (OpenAI ou Azure OpenAI)

## Instalação (Windows)

No diretório do projeto:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install git+https://github.com/microsoft/TinyTroupe.git@main
```

Crie o arquivo `.env` a partir do exemplo e preencha sua chave:

```powershell
copy .env.example .env
# edite .env e informe a OPENAI_API_KEY (ou AZURE_OPENAI_KEY/ENDPOINT)
```

## Configuração

.env.example:
```
OPENAI_API_KEY=
# (ou) AZURE_OPENAI_KEY= / AZURE_OPENAI_ENDPOINT=
```

config.ini mínimo:
```
[General]
api_type=openai
[OpenAI]
model=gpt-4.1-mini
[Simulation]
cache_api_calls=True
[Logging]
level=INFO
```

Notas:
- Para Azure OpenAI, ajuste no `config.ini`: `[General] api_type=azure` e use `AZURE_OPENAI_KEY` + `AZURE_OPENAI_ENDPOINT` no `.env`.

## Executando

```powershell
.venv\Scripts\activate
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Endpoints

- GET /health
  - Retorno: `{"status":"ok"}`

- POST /personas/demo
  - Cria:
    - 1 persona manual com `TinyPerson(...).define(...)`
    - 1 persona via `TinyPersonFactory(context="POC")` (fallback local se LLM indisponível)
  - Retorno (exemplo):
    ```json
    {
      "personas": [
        { "name": "Alice", "age": 28, "occupation": "Software Engineer" },
        { "name": "Maya Thompson", "age": 29, "occupation": "Embedded Systems Engineer" }
      ]
    }
    ```

- POST /simulate/echo
  - Body:
    ```json
    { "topic": "falem sobre Watch Guide", "steps": 2 }
    ```
  - Cria um `TinyWorld("Room", personas)` com 2 personas, envia o tópico para a primeira, roda `world.run(steps)` e retorna:
    ```json
    {
      "transcript": ["linha 1", "linha 2", "..."],
      "notes": "POC-only"
    }
    ```

## Exemplos (PowerShell)

Health:
```powershell
curl http://localhost:8000/health
```

Personas:
```powershell
curl -X POST http://localhost:8000/personas/demo
```

Simulação:
```powershell
curl -X POST http://localhost:8000/simulate/echo -H "Content-Type: application/json" -d "{\"topic\":\"falem sobre Watch Guide\",\"steps\":2}"
```

Dica: Para obter 3–6 linhas de transcript, use `steps=3` ou `4`.

## Troubleshooting

- The api_key client option must be set...
  - Verifique se `.env` está preenchido e o servidor foi reiniciado.
  - Confirme `api_type` no `config.ini` (openai vs azure).

- Pydantic UnsupportedFieldAttributeWarning (validate_default)
  - Aviso de dependência; pode ignorar.

- Agent name ... is already in use
  - A simulação usa nomes únicos por execução. Se ocorrer, reinicie o servidor.

## Segurança

- O `.gitignore` já ignora `.env`. Não comite chaves.
- Se uma chave foi exposta, rotacione-a no provedor.

## Escopo e Regras

- Sem Docker, sem frontend, sem testes, sem camadas extras, sem caching avançado.
- Objetivo único: provar TinyPerson, TinyPersonFactory e TinyWorld funcionando e retornando algo.