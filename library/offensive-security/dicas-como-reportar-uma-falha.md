---
id: ckb-ac697b3592a2
title: Dicas Como Reportar Uma Falha
category: offensive-security
format: guide
language: pt
tags: [bug-bounty, mitre-attack, tls, vulnerability-management]
authors: [Joas Antonio Dos Santos]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.31
---

Dicas: Como reportar uma
falha?
#0day #CVE #BugBounty
Joas Antonio
Detalhes
• Esse documento foi criado para ajudar pesquisadores de segurança
da informação a reportar suas vulnerabilidades e obter suas CVEs;
• Espero que ajude de alguma forma a reportar seu 0day ou alguma
vulnerabilidade em programas de Bug Bounty;
Meu LinkedIn: https://www.linkedin.com/in/joas-antonio-dos-santos/
Como encontrar vulnerabilidades?
• Primeiramente, é necessário conhecer os vetores de ataque do ambiente que você
está explorando, seja uma aplicação web, um Hardware ou um sistema
operacional. Entender como ele funciona e quais são os principais vetores de
ataque, que tipos de exploração de vulnerabilidade é comum e pegar algum
recurso, algum plugin ou componente e procurar vulnerabilidades, seja a nível de
aplicação ou até mesmo em baixo nível;
• Segundo, eu recomendo que procure programas de recompensa também, pois
quando se tem algo para testar e aprimorar suas habilidades pode ser que você
encontre vulnerabilidades e certamente ganhe uma recompensa;
• Terceiro, você pode testar os equipamentos que você tem em casa, seja um
roteador por exemplo, e assim procurar vulnerabilidades neles;
• Eu recomendo que você foque e teste todas as possibilidades, muita das vezes
uma vulnerabilidade pode levar a outra, por isso é sempre bom conhecer e saber
mesclar todo tipo de vulnerabilidade para gerar um impacto maior;
• Explore banco de dados de vulnerabilidades como exploit-db e o próprio Mitre,
pois você pode acabar melhorando uma PoC ou encontrando algo novo e mais
crítico ainda;
Plataformas de Bug Bounty
• HackerOne
• Bugcrowd
• Intigriti
• Bug Hunt
• Hackaflag
• Yogosha
• Zeroday initiative
• Open Bug Bounty
• YesWeHack
• Cobalt.io
• Synack Red Team
Como eu sei que tenho um 0day?
• Afeta algum produto? Algum componente que é utilizado por
terceiros? Ou que afeta a versão de algum programa? Existe algum
exploit da vulnerabilidade que você achou para esse produto
especifico? Existe alguma CVE Registrada? Consegue replicar essa
vulnerabilidade em um ambiente especifico ou em qualquer tipo de
ambiente? Essa vulnerabilidade precisa ativar alguma configuração
extra?
• Essas perguntas que você deve se fazer, as duas últimas é detalhes a
mais, porém  você tem um 0day respondendo pelo menos sim nas 4
primeiras perguntas;
• Mas em caso de dúvidas, reporte essa vulnerabilidade e espere a
fabricante se pronunciar;
Como reportar para o Mitre e obter minha
CVE?
• Dependendo do Report que você fizer, sua CVE pode ser gerada em
pouco tempo, mas para isso você precisa ser bem objetivo no seu
report e ter informações suficientes;
• Quer aprender a reportar? Segue o passo a passo nas próximas
páginas;
Reportando sua vulnerabilidade: Acessando
Site
• Acesse o site: https://cveform.mitre.org
Reportando sua vulnerabilidade: Tipo de
submissão
• Vamos selecionar no Select a Request Type: Request a CVE ID
Reportando sua vulnerabilidade: Definindo E-
mail
• Vamos selecionar no Enter your e-mail address: Coloque seu e-mail
que vai receber as notificações da CVE e etc...
Reportando sua vulnerabilidade: Quantas
CVEs serão geradas
• Você pode definir o número de IDs necessário para sua CVE, caso
sejam múltiplas vulnerabilidades que deseja reportar em um único
componente, software ou sistema.
Reportando sua vulnerabilidade: CNA
• As CNAs são os responsáveis pela atribuição dos IDS da CVE e por
manter essas informações e as publicar, dentro do escopo de cada
organização, geralmente grandes empresas entram para controlar
regularmente as CVEs que são atribuídas aos seus produtos;
• Consulte a lista de CNA, caso o fabricante esteja entre essas listas,
reporte diretamente a eles;
• Se não, basta marcar a primeira caixa e caso também não tenha uma
CVE atribuída, marque a segunda caixa;
Reportando sua vulnerabilidade: CNA
• As CNAs são os responsáveis pela atribuição dos IDS da CVE e por
manter essas informações e as publicar, dentro do escopo de cada
organização, geralmente grandes empresas entram para controlar
regularmente as CVEs que são atribuídas aos seus produtos;
• Consulte a lista de CNA, caso o fabricante esteja entre essas listas,
reporte diretamente a eles;
• Se não, basta marcar a primeira caixa e caso também não tenha uma
CVE atribuída, marque a segunda caixa;
Reportando sua vulnerabilidade: Tipo de
Vulnerabilidade
• Vamos definir um tipo de vulnerabilidade, caso não seja nenhuma da
lista, clique em Other or Unknown e coloque o nome da
vulnerabilidade;
Reportando sua vulnerabilidade: Definindo
Fabricante e Produto
• Agora vamos definir o Vendor (Fabricante) do produto, embaixo está
um exemplo;
• Depois o produto que está sendo afetado e a versão dele, seja versão
do firmware ou build dependendo da circunstância;
Reportando sua vulnerabilidade: Reconheceu
a vulnerabilidade e Tipo de Ataque
• Ele vai perguntar se o Fabricante confirmou ou reconheceu a
vulnerabilidade, caso você não tenha reportado para ele, coloque NO,
mas recomendo você reportar;
• E o tipo de ataque você vai escolher, Local, Físico, Remoto ou caso
nenhum desses, coloque outro;
Reportando sua vulnerabilidade: Reconheceu
a vulnerabilidade e Tipo de Ataque
• Tipo de impacto que a vulnerabilidade causa, seja uma execução de
código, negação de serviço ou escalar privilégios e outras
vulnerabilidades;
Reportando sua vulnerabilidade: Componente
afetado e vetor de ataque
• Esse é um exemplo que eu fiz, claro não leve a sério é apenas para dar
uma ideia, mas os componentes afetados é uma configuração, plugin,
biblioteca, API e etc;
Reportando sua vulnerabilidade: Componente
afetado e vetor de ataque
• O vetor de ataque é a forma como é explorada, como o atacante
efetua o ataque, o que é explorado e etc...
Reportando sua vulnerabilidade: Descrição da
vulnerabilidade
• Uma descrição da vulnerabilidade não precisa conter o exploit nem
nada do tipo, só resumir o que se trata a vulnerabilidade e qual
componente ele explora, lembre-se que a Prova do Conceito é algo a
parte, quando sair a correção você pode postar em seu blog ou redes
sociais e o CVE se torna um Identificador para auxiliar as outras
empresas a corrigir tal vulnerabilidade identificada.
http://cveproject.github.io/docs/content/key-details-phrasing.pdf
Reportando sua vulnerabilidade: Descrição da
vulnerabilidade
• Uma descrição da vulnerabilidade não precisa conter o exploit nem
nada do tipo, só resumir o que se trata a vulnerabilidade e qual
componente ele explora, lembre-se que a Prova do Conceito é algo a
parte, quando sair a correção você pode postar em seu blog ou redes
sociais e o CVE se torna um Identificador para auxiliar as outras
empresas a corrigir tal vulnerabilidade identificada.
Reportando sua vulnerabilidade: Conclusão
• Após isso, as outras informações não são necessárias, mas recomendo
que você coloque informações complementares se for necessário para
detalhar mais a vulnerabilidade;
• Depois que você preencher as informações e obter sua CVE ela vai ficar
reservada para depois ser divulgada;
• Conforme cada report realizado, você vai adquirindo mais skills para
que sua CVE seja aprovada rapidamente, sem a necessidade de dar
informações mais precisas;
CONCLUSÃO
• E se você quiser obter mais detalhes referente a carreira na área de
bug bounty, eu desenvolvi um documento: https://bit.ly/3hgypb4
• Espero que esse documento ajude você de alguma forma, convido
você entrar no meu perfil, pois lá tenho alguns artigos sobre Relatório,
CVEs, Zeroday e etc;
Fique a vontade em me contatar, abraços!
