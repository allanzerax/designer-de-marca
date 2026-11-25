#!/usr/bin/env python3
"""Cria a pasta de uma peça com HTML nas medidas certas."""
import argparse, html, os, pathlib, sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import marca as M

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--marca", required=True)
ap.add_argument("--formato", required=True, choices=["carrossel", "estatico", "quadrado", "story", "reels"])
ap.add_argument("--laminas", type=int, default=None)
ap.add_argument("--saida", required=True)
a = ap.parse_args()
p, m = M.ler(a.marca)
n = a.laminas or {"carrossel": 6, "story": 3}.get(a.formato, 1)
fmt = {"carrossel": "feed", "estatico": "feed"}.get(a.formato, a.formato)
s = pathlib.Path(a.saida).expanduser().resolve()
if (s / "peca.html").exists():
    sys.exit(f"já existe {s / 'peca.html'}: escolha outra pasta")
(s / "img").mkdir(parents=True, exist_ok=True)
M.css(p, m)


def rel(x):
    return pathlib.Path(os.path.relpath(x, s)).as_posix()


logo = next(iter(m.get("logos", {}).values()), None)
tag = f'<img data-logo src="{html.escape(rel(p.parent / logo))}" alt="{html.escape(m["nome"])}" style="position:absolute;left:64px;bottom:var(--s-base);height:56px">' if logo else ""
base = (pathlib.Path(__file__).resolve().parent.parent / "assets" / "formatos.css").read_text(encoding="utf-8")
sec = "\n\n".join(f'''<section data-peca="{i:02d}" data-formato="{fmt}">
  <h1 data-texto style="position:absolute;left:64px;right:64px;top:var(--s-topo);font:800 120px/1 var(--fonte-titulo)">manchete {i}</h1>
  {tag}
</section>''' for i in range(1, n + 1))
minimo = m.get("regras", {}).get("texto_minimo", 22)
(s / "peca.html").write_text(f'''<!doctype html>
<html lang="pt-BR" data-texto-minimo="{minimo}">
<head><meta charset="utf-8"><title>{html.escape(m["nome"])}: {html.escape(s.name)}</title>
<link rel="stylesheet" href="{html.escape(rel(p.parent / "marca.css"))}">
<style>
{base}:root{{--colunas:{min(3, n)}}}
/* desenho desta peça */
</style></head>
<body>

{sec}

</body></html>
''', encoding="utf-8")
print("criado", s / "peca.html")
