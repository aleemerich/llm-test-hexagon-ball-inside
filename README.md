# Testes com LLMs - Caso de reciocínio com Exágono e Bola dentro

## Premissa 

A IA receberá um único PROMPT (simples e pouco focado) e será analisado o que ela consegue desenvolver para resolver esse prompt da melhor forma.


## Prompt: 

"Escreva um programa em Python que mostra uma bola quicando dentro de um hexágono giratório. A bola deve ser afetada pela gravidade e pelo atrito, e deve quicar nas paredes rotativas de forma realista."



## IAs (LLMs) que foram testadas (todas de acesso FREE):

- ChatGPT (GPT- 4o mini)
- DeepSeek (R1)
- DeepSeek (sem R1)
- Copilot via Github (GPT4)
- Copilot via Github (Claude 3.5 Sonnet)

OBS: O Copilot foi adicionado para termos LLMs fora dos principais noticiados para tentar retirar alguns vieses.

## Bibliotecas usadas

- Chat GPT: pygame, math, sys
- DeepSeek sem R1: pygame, math, sys
- DeepSeek R1: pygame e math
- Copilot GH Cloude: pygame, math, sys

## Resultado:

O DeepSeek R1, ChatGPT com GPT- 4o mini, e o Copilot com Cloude 3.5 deram um código que atendia o desavio já em sua primeira resposta. O DeepSeek sem R1 também chegou lá, mas precisou de 3 prompt extra para pedir algumas correções.

O ponto que CHAMOU MUITO ATENÇÃO (ao menos pra mim) foi que o DeepSeek R1 apresentou um racional para gerar o código impressionante e usou menos bibliotecas externas. Se houvesse a necessidade de aprender, entender o que e como foi gerado, evoluir ou modificar o código, ficaria N vêzes mais fácil usando o racional do DeepSeek com R1 do que os dos outros.

Ainda, o Copilot, via Github, com Cloude 3.5 criou uma animação tão bom (ou até mais real) quando as outras e está também disponível de forma free para quem quiser usar. 

O Copilot, via GitHub, com o GPT4, que é um dos mais usados pelos DEV se não me engano, desapontou muito, mas muito mesmo e não gerou nada factível em termos de um "produto final", mesmo depois de várias interações.



## Conclusão: 

Eu acredito que nas comparações que estamos vendo por aí, estão faltando algo mais profundo do que apenas defender marcas. Como citei acima, acredito que em uma simulação simples como essa, há pontos importantes a serem levados em consideração além de só vermos o produto final. Esse teste poderia ser extendido a outras LLM para traçar um melhor comparativo, mas por questões de tempo disponível parei por aqui. Se quiserem contribuir, seria muito bacana para evoluirmos
