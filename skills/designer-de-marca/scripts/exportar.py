#!/usr/bin/env python3
"""Confere e exporta: exportar.py pasta/peca.html [--so-conferir] [--escala 1]"""
import argparse, html, json, os, pathlib, re, shutil, subprocess, sys, tempfile, time


def navegador():
    if os.environ.get("NAVEGADOR"):
        return os.environ["NAVEGADOR"]
    c = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
         "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge", "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    for b in ("ProgramFiles", "ProgramFiles(x86)", "LocalAppData"):
        r = os.environ.get(b)
        if r:
            c += [r + x for x in (r"\Google\Chrome\Application\chrome.exe", r"\Microsoft\Edge\Application\msedge.exe", r"\BraveSoftware\Brave-Browser\Application\brave.exe")]
    c += [shutil.which(x) for x in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "brave-browser", "microsoft-edge")]
    for x in c:
        if x and os.path.exists(x):
            return x
    sys.exit("Não achei Chrome, Brave, Edge ou Chromium. Defina a variável NAVEGADOR com o caminho.")


AUDIT = r"""<script>addEventListener('load',async()=>{
for(const f of document.fonts){try{await f.load()}catch(e){}}await document.fonts.ready;
const av=[],ps=[],min=+(document.documentElement.dataset.textoMinimo||22);
for(const f of document.fonts)if(f.status==='error')av.push('fonte não carregou: '+f.family+' '+f.weight);
for(const p of document.querySelectorAll('[data-peca]')){const n=p.dataset.peca,r=p.getBoundingClientRect(),cs=getComputedStyle(p);
ps.push({nome:n,w:Math.round(r.width),h:Math.round(r.height)});const px=k=>parseFloat(cs.getPropertyValue(k))||64;
for(const i of p.querySelectorAll('img'))if(!i.complete||!i.naturalWidth)av.push(n+': imagem não carregou: '+i.getAttribute('src'));
const ts=[...p.querySelectorAll('[data-texto]')];if(!ts.length)av.push(n+': nenhum data-texto (a checagem de texto não rodou)');
const caixas=ts.map(t=>{const g=document.createRange();g.selectNodeContents(t);const b=g.getBoundingClientRect();return{t,b,s:t.textContent.trim().replace(/\s+/g,' ').slice(0,32)}}).filter(x=>x.b.width);
for(const{t,b,s}of caixas){const st=getComputedStyle(t);
if(parseFloat(st.fontSize)<min)av.push(n+': texto menor que '+min+'px: "'+s+'"');
const e=2,l=[];if(b.left<r.left+64-e)l.push('esquerda');if(b.right>r.right-64+e)l.push('direita');
if(!('livre'in t.dataset)){const fol=parseFloat(st.fontSize)*.15;if(b.top<r.top+px('--s-topo')-fol)l.push('topo');if(b.bottom>r.bottom-px('--s-base')+fol)l.push('base')}
if(l.length)av.push(n+': fora da área segura ('+l.join(', ')+'): "'+s+'"');
if(t.scrollWidth>t.clientWidth+2&&st.display!=='inline')av.push(n+': texto estoura a caixa: "'+s+'"')}
for(const t of p.querySelectorAll('[data-logo]')){const b=t.getBoundingClientRect();
if(b.left<r.left+62||b.right>r.right-62||(!('livre'in t.dataset)&&(b.top<r.top+px('--s-topo')-2||b.bottom>r.bottom-px('--s-base')+2)))av.push(n+': logo fora da área segura')}
for(let i=0;i<caixas.length;i++)for(let j=i+1;j<caixas.length;j++){const A=caixas[i],B=caixas[j];if(A.t.contains(B.t)||B.t.contains(A.t))continue;
const w=Math.min(A.b.right,B.b.right)-Math.max(A.b.left,B.b.left),h=Math.min(A.b.bottom,B.b.bottom)-Math.max(A.b.top,B.b.top);
if(w>4&&h>14)av.push(n+': textos sobrepostos: "'+A.s+'" e "'+B.s+'"')}}
const o=document.createElement('pre');o.id='AUDITORIA';o.textContent=JSON.stringify({ps,av,W:Math.ceil(Math.max(...[...document.querySelectorAll('[data-peca]')].map(e=>e.getBoundingClientRect().right+scrollX)))+60,H:Math.ceil(Math.max(...[...document.querySelectorAll('[data-peca]')].map(e=>e.getBoundingClientRect().bottom+scrollY)))+60});document.body.append(o)})</script>"""


def rodar(nav, perfil, url, extra, pronto, saida=None):
    cmd = [nav, "--headless=new", "--disable-gpu", "--no-first-run", "--allow-file-access-from-files", "--hide-scrollbars",
           f"--user-data-dir={perfil}", "--virtual-time-budget=8000", *extra, url]
    with open(saida or os.devnull, "wb") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.DEVNULL)
        fim = time.time() + 60
        # o Chrome headless às vezes não encerra sozinho: espera o resultado e fecha
        while time.time() < fim and not pronto():
            if p.poll() is not None:
                break
            time.sleep(.3)
        time.sleep(.4)
        ok = pronto()
        if p.poll() is None:
            p.kill()
        p.wait()
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html")
    ap.add_argument("--so-conferir", action="store_true")
    ap.add_argument("--escala", type=float, default=1)
    a = ap.parse_args()
    src = pathlib.Path(a.html).expanduser().resolve()
    txt = src.read_text(encoding="utf-8")
    tmp = src.with_name("_exportar_tmp.html")  # ao lado do original, para os caminhos relativos valerem
    nav = navegador()
    perfil = tempfile.mkdtemp(prefix="designer-marca-")

    def injeta(x):
        i = txt.lower().rfind("</body>")
        tmp.write_text(txt[:i] + x + txt[i:] if i >= 0 else txt + x, encoding="utf-8")
        return tmp.as_uri()

    def png(url, w, h, out, esc):
        out.unlink(missing_ok=True)
        if not rodar(nav, perfil, url, [f"--force-device-scale-factor={esc}", f"--window-size={w},{h}", f"--screenshot={out}"],
                     lambda: out.exists() and out.stat().st_size > 0):
            sys.exit(f"não consegui exportar {out.name}")

    try:
        dom = pathlib.Path(perfil) / "dom.html"
        rodar(nav, perfil, injeta(AUDIT), ["--window-size=3600,3000", "--dump-dom"],
              lambda: dom.exists() and b"</html>" in dom.read_bytes()[-200:], dom)
        g = re.search(r'<pre id="AUDITORIA">(.*?)</pre>', dom.read_text(encoding="utf-8", errors="replace"), re.S)
        if not g:
            sys.exit("a conferência não rodou: abra o HTML no navegador e veja se há erro")
        d = json.loads(html.unescape(g[1]))
        if not d["ps"]:
            sys.exit("nenhum [data-peca] no HTML")
        nomes = [x["nome"] for x in d["ps"]]
        if len(set(nomes)) < len(nomes) or any(not re.fullmatch(r"[\w-]+", n) for n in nomes):
            sys.exit(f"data-peca precisa ser único e só com letras, números e hífen: {nomes}")
        print(f"{len(nomes)} arte(s), {len(d['av'])} aviso(s)")
        for x in d["av"]:
            print("  !", x)
        if a.so_conferir:
            return 1 if d["av"] else 0
        out = src.parent / "png"
        out.mkdir(exist_ok=True)
        for x in d["ps"]:
            css = ("<style>html,body{margin:0!important;padding:0!important;display:block!important;width:auto!important;overflow:hidden}"
                   f"[data-peca]:not([data-peca='{x['nome']}']){{display:none!important}}[data-peca]{{border-radius:0!important}}</style>")
            f = out / f"{x['nome']}.png"
            png(injeta(css), x["w"], x["h"], f, a.escala)
            print("  ok", f.relative_to(src.parent))
        png(injeta(""), d["W"], d["H"], src.parent / "prancha.png", min(1, 2800 / d["W"]))
        print("  ok prancha.png")
        return 0
    finally:
        tmp.unlink(missing_ok=True)
        shutil.rmtree(perfil, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
