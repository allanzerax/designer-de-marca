# designer de marca

Skill para o Claude Code. Você entrega o manual de identidade visual (MIV) e ela cria **carrossel, post estático e story** com a cara da marca.

- **Imagens:** geradas no **seu ChatGPT**, pelo Chrome. Sem chave de API.
- **Texto, fontes, logo e diagramação:** HTML, sempre editável.
- **Referência:** mande um post de que gostou. Ela usa a lógica e veste com a sua marca.

## Instalar

No Claude Code:

```
/plugin marketplace add allanzerax/designer-de-marca
/plugin install designer-de-marca@designer-de-marca
```

Ou copie `skills/designer-de-marca` para `~/.claude/skills/`.

## Precisa de

- Claude Code, Python 3.9+ e Chrome, Edge, Brave ou Chromium
- para gerar imagens sozinho: extensão Claude in Chrome e ChatGPT logado. Sem isso, a skill escreve os pedidos, você gera e coloca na pasta `img/`

## Usar

Digite `/designer-de-marca` (instalada como plugin: `/designer-de-marca:designer-de-marca`) ou fale normalmente: "vamos fazer um design", "faz um post", "cria um carrossel". Dá para adiantar: `/designer-de-marca carrossel 5 lâminas`.

> faz um carrossel de 6 lâminas sobre [assunto] com o MIV que está em ./manual.pdf

> quero um story com essa referência (print.png), na identidade da marca

Abra o Claude Code na pasta do cliente. A skill procura o MIV ali e pergunta, uma coisa por vez:

1. qual é o MIV (só se não encontrar)
2. se há uma referência de design
3. o texto do post
4. o formato e, no carrossel, quantas lâminas

Depois: roteiro para aprovar → imagens → HTML → conferência → PNGs.

```
designer/
  marca/    marca.json, direcao.md, marca.css, fontes
  pecas/AAAA-MM-DD-assunto/
    peca.html   edite aqui      prompts.md   pedidos de imagem
    img/        imagens         png/         artes finais
    prancha.png                 tudo numa tela
```

## Bom saber

- As imagens gastam a cota do seu ChatGPT, e a skill pede autorização antes. Siga os termos do serviço. A página do ChatGPT muda, e o modo manual é o plano B.
- Ela não publica nada nem digita senha.
- Confira dados e direitos de uso antes de postar.

Licença MIT. As fontes baixadas seguem as licenças próprias.
