#!/usr/bin/env python3
"""Prepara a marca. Uso: marca.py fontes|contraste|css caminho/marca.json"""
import itertools, json, pathlib, re, sys, urllib.parse, urllib.request


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def ler(p):
    p = pathlib.Path(p).expanduser().resolve()
    m = json.loads(p.read_text(encoding="utf-8"))
    for n, h in m["cores"].items():
        if not re.fullmatch(r"#[0-9A-Fa-f]{6}", h):
            sys.exit(f"cor '{n}' precisa ser #RRGGBB, veio {h}")
        if slug(n) != n:
            sys.exit(f"nome de cor '{n}': use minúsculas, sem acento e com hífen")
    for papel, n in m.get("papeis", {}).items():
        if n not in m["cores"]:
            sys.exit(f"papel '{papel}' aponta para cor inexistente: {n}")
    return p, m


def lum(h):
    v = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in v]
    return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]


def contraste(a, b):
    x, y = sorted((lum(a), lum(b)))
    return (y + .05) / (x + .05)


def baixar(url):
    # sem user-agent de navegador o Google Fonts devolve TTF, que funciona offline
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=60) as r:
        return r.read()


def fontes(p, m):
    d = p.parent / "fontes"
    for papel, f in m["fontes"].items():
        if not f.get("google"):
            for a in f.get("arquivos", []):
                print("ok  " if (p.parent / a["arquivo"]).exists() else "FALTA", a["arquivo"])
            continue
        d.mkdir(exist_ok=True)
        feitos = []
        estilos = [False, True] if f.get("italico") else [False]
        for peso, it in itertools.product(f.get("pesos", [400]), estilos):
            arq = d / f"{slug(f['familia'])}-{peso}{'-italic' if it else ''}.ttf"
            if not arq.exists():
                eixo = f"ital,wght@1,{peso}" if it else f"wght@{peso}"
                q = urllib.parse.quote(f["familia"]).replace("%20", "+")
                try:
                    css = baixar(f"https://fonts.googleapis.com/css2?family={q}:{eixo}").decode()
                    url = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)[1]
                    arq.write_bytes(baixar(url))
                except Exception as e:
                    print(f"FALHOU {f['familia']} {peso}: {e}. Confira nome e peso no Google Fonts.")
                    continue
            feitos.append({"arquivo": f"fontes/{arq.name}", "peso": peso, "italico": it})
            print("ok  ", arq.name)
        f["arquivos"] = feitos
    p.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def css(p, m):
    o = ["/* gerado por marca.py: edite marca.json e gere de novo */"]
    fam = []
    for papel, f in m["fontes"].items():
        for a in f.get("arquivos", []):
            peso = str(a.get("peso", 400))
            o.append(f"@font-face{{font-family:'{f['familia']}';src:url('{a['arquivo']}');font-weight:{peso};font-style:{'italic' if a.get('italico') else 'normal'}}}")
        fam.append(f"  --fonte-{slug(papel)}:'{f['familia']}',{f.get('reserva', 'sans-serif')};")
    o.append(":root{")
    o += [f"  --cor-{n}:{h};" for n, h in m["cores"].items()]
    o += [f"  --{slug(k)}:var(--cor-{n});" for k, n in m.get("papeis", {}).items()]
    o += fam + ["}"]
    (p.parent / "marca.css").write_text("\n".join(o) + "\n", encoding="utf-8")
    print("criado", p.parent / "marca.css")


def tabela(p, m):
    for (a, x), (b, y) in itertools.combinations(m["cores"].items(), 2):
        r = contraste(x, y)
        print(f"{r:5.1f}:1  {a} + {b}: " + ("texto e título" if r >= 4.5 else "só título grande" if r >= 3 else "não usar em texto"))


if __name__ == "__main__":
    acoes = {"fontes": fontes, "css": css, "contraste": tabela}
    if len(sys.argv) != 3 or sys.argv[1] not in acoes:
        sys.exit(__doc__)
    acoes[sys.argv[1]](*ler(sys.argv[2]))
