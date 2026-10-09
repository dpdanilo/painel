"""
Troca só o LAYOUT do dashboard, reaproveitando os dados que já estão dentro do
index.html atual. Não baixa nada do TSE e não precisa de DuckDB.

Lê  : index.html (o atual, já publicado)  +  template.html (o layout novo)
Grava: index.html (novo)
"""
import json
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ARQUIVO = "index.html"      # se o seu fica em outra pasta (ex.: docs/index.html), mude aqui
MODELO = "template.html"

src = open(ARQUIVO, encoding="utf-8").read()
i = src.find("const D=")
j = src.find(",S=D.S,", i)
if i < 0 or j < 0:
    sys.exit("ERRO: não achei os dados dentro de " + ARQUIVO)
dados = src[i + len("const D="):j]
D = json.loads(dados)
linhas = D.get("rows") or []
if not linhas or len(linhas[0]) < 22 or "S" not in D:
    sys.exit("ERRO: o index.html atual é de uma versão antiga (sem as colunas de Bolsonaro e "
             "dos candidatos de 2026). Gere os dados de novo com o script no computador.")

modelo = open(MODELO, encoding="utf-8").read()
agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")
novo = modelo.replace("__DATA__", dados).replace("__BUILD__", agora)
open(ARQUIVO, "w", encoding="utf-8").write(novo)
print(f"OK: {len(linhas):,} locais; {ARQUIVO} agora tem {len(novo)/1e6:.1f} MB; layout de {agora}")
