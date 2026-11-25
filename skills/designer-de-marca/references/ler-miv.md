# Ler o MIV

PDF: abra as páginas como imagem (ferramenta de leitura, em blocos de até 20), porque texto extraído perde proporção, exemplo e "não faça". Site, pasta ou imagens: veja tudo antes de resumir.

## O que extrair

| Campo | Procure | Cuidado |
|---|---|---|
| Cores | HEX, RGB, CMYK, Pantone, proporção | código escrito vale mais que cor medida na imagem. Só CMYK ou Pantone: converta e marque `estimado` |
| Fontes | família, peso, função, caixa, entrelinha | fonte paga: peça o arquivo. Sem arquivo, proponha uma parecida do Google Fonts e avise |
| Logo | versões, respiro, mínimo, fundos permitidos | peça SVG ou PNG transparente. Não recorte do PDF sem avisar |
| Elementos | formas, fios, padrões, ícones, selos | anote medida e quando usar |
| Imagem | foto, ilustração, luz, tratamento | é a base do bloco de estilo do GPT |
| Voz | tom, caixa, pontuação, bordões | vale para manchete e legenda |
| Proibições | tudo em "não faça" | copie por inteiro: elas evitam a maioria dos retrabalhos |

MIV omisso num ponto (ex.: não fala de story): decida pela lógica do resto e registre como `estimado`. Contradição interna: pergunte.

## direcao.md

Meia página, nesta ordem: conceito em uma frase · personalidade em 3 a 5 palavras e o que ela não é · voz com um antes/depois · imagem · composição (cheia ou vazia, simétrica ou não, quanta cor) · proibições · estilo aprovado (vazio no início).

## marca.json

Siga `assets/marca.exemplo.json`. Caminhos são relativos ao próprio `marca.json`. Em `cores`, dê nomes curtos, sem acento: viram variáveis CSS (`--cor-tinta`). `papeis` diz qual cor faz fundo, texto e destaque por padrão. Em `fontes`, use `arquivos` (locais) ou `google: true`. `regras.texto_minimo` é em px numa arte de 1080 de largura.
