# Gerar imagens no ChatGPT da pessoa

## Antes

1. Confirme que há autorização para usar a conta, gastar a cota e baixar as imagens (passo 2 do SKILL.md).
2. Carregue as ferramentas do Claude in Chrome de uma vez e abra uma aba **nova** em `https://chatgpt.com/`.
3. Não logado, captcha ou aviso de limite: pare e peça que a pessoa resolva. Não digite senha e não contorne nada.
4. Não abra outras conversas da conta.

## Primeira mensagem: bloco de estilo + imagem 1

Escreva numa linha só, porque quebra de linha pode enviar a mensagem. Estrutura:

> Gere uma imagem. Formato [quadrado], fundo totalmente transparente (PNG com alfa). Estilo fixo para toda esta conversa: [técnica], [época ou referência de linguagem], [luz], [acabamento], cores apenas [hex da marca]. Sem texto, sem letras, sem números, sem logotipos, sem marcas, sem [proibições do MIV]. Imagem 1: [cena concreta, ângulo, gesto]. Objeto inteiro dentro do quadro, com folga.

Descreva técnica e matéria ("fotografia recortada à tesoura, retícula de pontos grandes, tinta fora de registro"), não adjetivo ("bonito, moderno"). Não cite artista vivo, marca ou personagem.

## Seguintes

> Gere a imagem 2, mesmo estilo exato, fundo transparente, quadrada, objeto inteiro com folga: [cena]. Sem texto.

Uma por vez. **Só envie a próxima quando a anterior terminar** (o botão de parar some). Enviar durante a geração junta dois pedidos numa imagem só. Espere em passos de até 10 s: costuma levar de 40 a 90 s. Olhe cada resultado e, se sair do estilo, peça correção específica, no máximo duas vezes. Não escolha por "qual prefere?" se a opção já serve.

Fundos e texturas: peça opaco, sem objeto, contraste baixo, "bordas iguais ao centro". No HTML, use a textura só como luz, para a cor da marca não mudar: `filter:grayscale(1) brightness(.6) contrast(2)` com `mix-blend-mode:soft-light`. O ponto neutro é cinza médio: se a arte clarear ou escurecer, ajuste o `brightness`.

## Baixar

As imagens da conversa ficam em `main img`, e a página só mantém as próximas da tela. Role, colete e baixe pelo navegador:

```js
// 1) com a conversa rolada, liste
[...document.querySelectorAll('main img')].filter(i=>i.naturalWidth>700).map((i,n)=>[n,i.alt,i.naturalWidth,i.naturalHeight,i.src.slice(0,90)])
// 2) baixe uma, já sabendo o índice
const i=[...document.querySelectorAll('main img')].filter(i=>i.naturalWidth>700)[0];
const b=await(await fetch(i.src)).blob();const a=document.createElement('a');
a.href=URL.createObjectURL(b);a.download='peca-01.png';a.click();b.size
```

Se a página mudou e isso falhar, use o botão de baixar da própria imagem. Mova da pasta de downloads para `img/` só os arquivos desta peça, com nome que diz o que é (`cadeira.png`). Confira tamanho e se há transparência. Não saiu transparente? Peça de novo em fundo liso e recorte, ou use a imagem dentro de uma forma.

Salve os pedidos em `prompts.md` e feche a aba que abriu.
