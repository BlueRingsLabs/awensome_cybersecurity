---
id: ckb-a3d4323ec770
title: Conceitos Bsicos de Ps Explorao 1
category: offensive-security
format: guide
language: pt
tags: [git, linux, metasploit, mitre-attack, tls, windows]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.93
---

TÉCNICAS DE PÓS EXPLORAÇÃO
BÁSICO
JOAS ANTONIO
Sobre o Livro
O objetivo é ensinar técnicas de pós exploração em
sistemas operacionais Windows e Linux;
Esse material ele não é prático, apenas apresenta
métodos para realizar pós exploração;
Um livro básico feito para todos os públicos.
Sobre o Autor
Entusiasta e apaixonado por segurança da informação;
https://www.linkedin.com/in/joas-antonio-dos-santos/
Conceitos de Pós Exploração
Conceito
Pós-exploração significa basicamente as fases da
operação depois que o sistema da vítima é comprometido
pelo invasor. O valor do sistema comprometido é
determinado pelo valor dos dados reais armazenados nele
e como um invasor pode usá-lo para fins maliciosos. O
conceito de pós-exploração surgiu desse fato apenas
sobre como você pode usar as informações do sistema
comprometido da vítima. Essa fase realmente lida com a
coleta de informações confidenciais, a documentação e a
ideia das definições de configuração, interfaces de rede e
outros canais de comunicação. Eles podem ser
usados ​para manter o acesso persistente ao sistema
conforme as necessidades do invasor.
A Importância
A pós-exploração obtém o acesso que temos e tenta estender
e elevar esse acesso. Compreender como os recursos de rede
interagem e como alternar de uma máquina comprometida
para a próxima agrega valor real aos nossos clientes. Identificar
corretamente máquinas vulneráveis ​no ambiente e provar que
as vulnerabilidades são exploráveis ​é bom. Mas ser capaz de
coletar informações para demonstrar um impacto significativo
nos negócios é melhor.
O que envolve a
pós exploração?
Coleta de informação avançada;
Captura de senhas;
Elevação de privilégios;
Movimento Lateral e Pivoting;
Exfiltração de dados;
Acesso persistente;
Mitre Attack
A MITRE introduziu o ATT&CK (Adversarial Tactics,
Techniques & Common Knowledge - Táticas, técnicas e
conhecimento comum dos inimigos) em 2013 como uma
forma de descrever e classificar os comportamentos dos
inimigos com base em observações do mundo real. O
ATT&CK é uma lista estruturada de comportamentos
conhecidos do agressor, que foram compilados em táticas
e técnicas e expressos em várias matrizes, bem como via
STIX/TAXII. Como essa lista é uma representação
abrangente dos comportamentos dos agressores ao
comprometer as redes, ela é útil para várias análises
ofensivas e defensivas, representações e outros
mecanismos.
Mitre Attack-
Matriz
A MITRE dividiu o ATT&CK em várias matrizes
diferentes: Enterprise, Mobile e PRE-ATT&CK. Cada uma
dessas matrizes contém várias táticas e técnicas
associadas ao tema da matriz.
A matriz Enterprise é formada por técnicas e táticas que
se aplicam aos sistemas Windows, Linux e/ou MacOS. A
Mobile contém táticas e técnicas que se aplicam a
dispositivos móveis. A PRE-ATT&CK contém táticas e
técnicas relacionadas às ações dos agressores antes de
tentar explorar uma rede ou sistema em particular.
Mitre Attack–
Diferença de
Matrizes
O PRE-ATT&CK e ATT&CK Enterprise se unem para criar
uma lista completa de táticas que se alinham ao Cyber Kill
Chain. Geralmente, o PRE-ATT&CK alinha-se às primeiras
três fases do kill chain: reconhecimento, armamento e
entrega. O ATT&CK Enterprise alinha-se bem às quatro
últimas fases do kill chain: exploração, instalação,
comando e controle, ações sobre objetivos.

Metasploit
O Metasploit possui uma ampla variedade de módulos pós-
exploração que podem ser executados em alvos
comprometidos para reunir evidências, se aprofundar na rede
de destino e muito mais.
WINDOWS
Post Capture Modules
Post Gather Modules
Post Manage Modules
LINUX
Post Gather Modules
OS X
Post Gather Modules
MULTIPLE OS
Post Gather Modules
Post General Modules
Meterpreter–
O que é?
O Meterpreter, a forma abreviada de Meta-
Interpreter é uma carga útil avançada e
multifacetada que opera via injeção de DLL. O
Meterpreter reside completamente na memória
do host remoto e não deixa vestígios no disco
rígido, dificultando a detecção com técnicas
forenses convencionais. Scripts e plugins podem
ser carregados e descarregados dinamicamente,
conforme necessário, e o desenvolvimento do
Meterpreter é muito forte e está em constante
evolução.
Meterpreter-
Objetivo
Com payloads em geral, geralmente é oferecido um
shell através do qual podemos simplesmente interagir
com o sistema. Sob essas circunstâncias normais, uma
vez que o sistema é explorado, uma única carga útil é
entregue, capaz de executar comandos. E se você
quiser baixar um arquivo? Ou você quer pegar os
hashes de senha de todas as contas de usuário? Ou
você deseja girar para outro rede? Ou você deseja
aumentar seu privilégio? Bem, é claro que você pode
fazer essas tarefas, mas imagine o número de etapas e
dificuldades que você precisará superar enquanto
segue por este caminho
Meterpreter
Outro fato bonito sobre o meterpreter é sua
capacidade de permanecer indetectável por sistemas
de detecção de intrusão mais usados. Incorporando-se
ao processo de pré-execução no host remoto, ele não
altera os arquivos do sistema no HDD e, portanto, não
fornece nenhuma pista para o HIDS [Host Intrusion
Detect System. Além disso, o processo no qual o
meterpreter está sendo executado pode ser alterado
em a qualquer momento, então rastreá-lo ou encerrá-
lo torna-se bastante difícil, mesmo para um pessoa.
Meterpreter e Exemplos
Meterpreter-
Examples
Um laboratório interessante que você pode testar é
subir uma máquina Windows XP e Windows 7 e utilizar
dois exploits:
- MS08_067
- MS17-010
Duas vulnerabilidades para realizar shell reversa em
uma máquina, lembre-se que no Windows você
precisa definir o payload conforme a arquitetura do
alvo, então se o alvo for 32 bits você utiliza.
Set payload Windows/meterpreter/reverse_tcp
Caso seja 64 bits
Set payload Windows/x64/meterpreter/reverse_tcp
Meterpreter-
Examples
Por meio de um alvo comprometido, você pode executar um Arp
Scanner e enumerar todos os hosts de uma rede
Meterpreter-
Examples
Verificar se o alvo comprometido é uma máquina virtual
Meterpreter-
Examples
Coletar Hashes e tokens de senha do alvo
Meterpreter-
Examples
Enumerar aplicativos de uma máquina
Meterpreter-
Examples
Traz sugestões de exploits locais para realizar pós
exploração
Meterpreter-
Examples
Enumerar configurações de serviços Linux
Meterpreter-
Examples
Reune informações de rede em regras no Iptables,
interfaces, informações de rede sem fio, portas abertas e etc
Meterpreter-
Examples
O módulo enum_protections tenta encontrar certos
aplicativos instalados que podem ser usados ​para impedir
ou detectar nossos ataques, o que é feito localizando
determinados locais binários e ver se eles são realmente
executáveis.
Meterpreter-
Examples
O módulo enum_users_history reúne informações
específicas do usuário. Lista de usuários, histórico do bash,
histórico do mysql, histórico do vim, lastlog e sudoers.
Meterpreter-
Script
E claro, assim como os módulos do metasploit são abertos para
modificação, o Meterpreter tem scripts que podem ser melhorados,
caso você queira criar seus próprios scripts é essencial conhecer de
Ruby e entender sua estrutura.
Caso tenha interesse de entender, fiz o código comentado de um script
meterpreter, vou colocar outros códigos, seja exploits e módulos de pós
exploração também.
https://github.com/CyberSecurityUP/Development-for-Metasploit
https://www.offensive-security.com/metasploit-unleashed/custom-scripting/
https://www.offensive-security.com/metasploit-unleashed/custom-scripting/
Técnicas de Pós Exploração
O que será
apresentado
nesse cápitulo?
Dicas e métodos para exploração de vulnerabilidades;
Técnicas de coleta de senhas e enumeração de usuários;
Quebra de senhas;
Spawn de Shells;
Exploit-db, Searchsploit e Metasploit;
Métodos de escalação de privilégios Linux;
Métodos de escalação de privilégios Windows;
Desenvolvendo o pensamento Try Harder;
Explorando
vulnerabilidades
Sempre que você está realizando um PenTest à primeira
etapa que sempre realizamos é o Scanning para identificar à
versão do sistema operacional, serviços sendo utilizados e
portas que estão abertas. E após essa identificação você
procura brechas de segurança, seja em nível de sistema ou
no nível de aplicação.
Mas para entender melhor como conseguir explorar uma
vulnerabilidade, precisamos entender as camadas de
segurança e como afetar cada uma delas.
Camadas de
Segurança -
Física
Segurança Física:
(Salvaguardar as pessoas, o hardware, os programas, as redes e
os dados contra ameaças físicas)
PenTest nessa camada:
Mapear entradas da empresa, Identificar mecanismo de
segurança física;
Utilizar técnicas de Lockpicking para entrar em uma empresa;
Acessar salas de servidores ou um escritório se passando por
um funcionário e utilizando BadUSB para espetar no
computador mais fácil;
Mergulhar na Lixeira (Dumpster Diving);
Interceptar sinais de frequência;
Camadas de
Segurança -
Redes
Segurança de Redes:
Protege as redes e seus serviços contra modificação, destruição
ou divulgação não autorizada
PenTest nessa camada:
Quebrar a senha de uma rede wireless ou tentar invadir tal rede
por meio de um computador infectado dentro dela;
Enumerar hosts, serviços e portas abertas em uma rede;
Procurar por brechas e vulnerabilidades nesses hosts, talvez
um exploit pronto para comprometer um serviço que está em
uma versão vulnerável;
Exfiltrar dados de uma rede;
Pivoting e movimentos laterais;
Camadas de
Segurança -
Sistemas
Segurança de Sistemas:
Protege o sistema e suas informações contra roubo,
corrupção, acesso não autorizado ou mau uso
PenTest nessa camada:
Quebra de hashes de senhas;
Comprometer os serviços sendo rodados nesse sistema;
Escalação de privilégios;
Roubo de informações;
Camadas de
Segurança -
Aplicações
Segurança de Aplicativos:
Abrange o uso de software, hardware e métodos processuais
para proteger os aplicativos contra ameaças externas
PenTest nessa camada:
Identificar versões de aplicação;
Explorar vulnerabilidades em aplicações;
Roubo de informações;
Comprometer o sistema operacional dessa aplicação;
Camadas de
Segurança -
Usuários
Segurança de Usuários Finais:
Garante que um usuário válido esteja conectado e que o
usuário conectado tenha permissão para utilizar um
aplicativo/programa
PenTest nessa camada:
Técnicas de OSINT;
Engenharia Social;
Phishings;
Quebra de controles de acessos;
Explorando
vulnerabilidades
Esses são apenas alguns dos métodos que pode ser
utilizados para explorar cada camada de segurança de uma
organização;
Obviamente que dentro desses métodos você tem técnicas
que podem ser utilizadas para alcançar determinados
objetivos;
Dicas
Fique sempre de olho em novas vulnerabilidades que vão
surgindo;
Pratique em laboratórios técnicas de exploração que vai
desde da camada de aplicação até à camada de sistemas,
pois muita das vezes uma brecha surge em aplicações e que
resulta no comprometimento do sistema;
Além de estudar formas de realizar pentest nessas camadas e
entender as brechas de segurança que existem;
Comandos
Linux
https://github.com/mubix/post-exploitation/wiki/Linux-Post-
Exploitation-Command-List
Comandos
Windows
https://medium.com/@int0x33/day-26-the-complete-list-of-
windows-post-exploitation-commands-no-powershell-
999b5433b61e
Coleta de senhas
e enumeração de
usuários -
Windows
Comandos utilizados para coletar usuários com diferentes tipos de privilégios
net accounts
net accounts /domain
net logalgroup administrators
net localgroup administrators /dmain
net group "domain Admins" /domain
net group "Enterprise Admins" /domain
net view /localgroup
net localgroup Administrators
net localgroup /Domain
gpresult: view group policy
gupdate: update group policy
gpresult /z
net users
Coleta de senhas e
enumeração de usuários
-Windows
Dump de hashs de senha
Você pode utilizar o Mimikatz, o Meterpreter ele tem
um script pronto para isso.
Coleta de senhas e enumeração
de usuários -Windows
Enumerando usuários com SMB_USER
nmap -p445 — script smb-protocols
<target ip>
nmap -p139 — script smb-protocols
<target ip>
nmap --script smb-enum-users.nse -
p445 <host>
nmap -sU -sS --script smb-enum-
users.nse -p <port> <host>
Coleta de senhas
e enumeração de
usuários -
Windows
Outros métodos
https://www.offensive-security.com/metasploit-
unleashed/john-ripper/
https://medium.com/@Shorty420/enumerating-ad-
98e0821c4c78
https://null-byte.wonderhowto.com/how-to/enumerate-smb-
with-enum4linux-smbclient-0198049/
https://www.youtube.com/watch?v=YxeXfHkHAUI
https://www.youtube.com/watch?v=sXqT95eIAjo
https://www.youtube.com/watch?v=sA51iv07cp8
Coleta de senhas e enumeração
de usuários -Linux
Coletando usuários em Linux
cat /etc/passwd
Less /etc/passwd
More /etc/passwd
tail -5 /etc/passwd
head -5 /etc/passwd
awk -F':' '{ print $1}' /etc/passwd
cut -d: -f1 /etc/passwd
getent passwd
compgen -u
Coleta de senhas
e enumeração de
usuários –Linux
Coletando hash de senha
cat /etc/shadow
Openssl passwd -1
openssl passwd -1 -salt yoursalt
python -c "import crypt; print
crypt.crypt('joske’)”
Getent passwd
Coleta de senhas
e enumeração de
usuários –Linux
Outros métodos:
https://github.com/mubix/post-
exploitation/wiki/Linux-Post-Exploitation-
Command-List#user_accounts
https://backdoorshell.gitbooks.io/oscp-useful-
links/content/linux-post-exploitation.html
Enumeração
HTTP
Dirb Enumeration:
https://www.hackingarticles.in/comprehensive-
guide-on-dirb-tool/
Recon:
https://github.com/OfJAAH/ReconOfJAAAH
Nmap HTTP Enumeration:
https://nmap.org/nsedoc/scripts/http-enum.html
Quebra de senhas
–Passiva
(Criptografias e
Hashs)
John The Ripper: https://www.tunnelsup.com/getting-
started-cracking-password-hashes/
Hashcrack:
https://laconicwolf.com/2018/09/29/hashcat-
tutorial-the-basics-of-cracking-passwords-with-
hashcat/
HashKiller: https://hashkiller.io/
Quebra de
senhas –Online
SSH Brute Force: https://linuxconfig.org/ssh-password-
testing-with-hydra-on-kali-linux
https://sempreupdate.com.br/introducao-ao-hydra-
brute-force/
SMB Brute Force: https://github.com/m4ll0k/SMBrute
https://www.youtube.com/watch?v=F_CaOtXIPJg
https://techwagyu.com/best-brute-force-password-
cracking-software/
HTTP Brute Force:
https://redteamtutorials.com/2018/10/25/hydra-brute-force-
https/
Dica: Em muitos challenges as senhas do Rockyou.txt são padrão
Spawn Shells
Após comprometer um sistema, muita das vezes você não tem uma shell
interativa, apenas uma tela toda preta que vai digitando os comandos, mas
não sabe quais os resultados são apresentados na maioria dos comandos
que você vai inserindo, por isso como uma técnica de pós exploração é
utilizado Shell Interativas que você pode gerar elas utilizando vários
métodos.
Utilizando Python: python -c 'import pty; pty.spawn("/bin/sh")’
Utilizando Python 3: python3 -c 'import pty; pty.spawn("/bin/sh")’
Utilizando ECHO: echo 'os.system('/bin/bash')’
Utilizando SH: /bin/sh –i
Utilizando Perl: perl -e 'exec "/bin/sh";’
Utilizando Lua: Lua; os.execute('/bin/sh')
Buscando
métodos de pós
exploração
E caso você queira procurar exploits locais, scripts auxiliares e outros
métodos para elevar seus privilégios ou quebrar um controle de acesso, eu
recomendo 2 ferramentas;
https://exploit-db.com/
https://www.exploit-db.com/searchsploit
Ambas as duas ferramentas que são a mesma coisa, te ajuda à procurar
exploits públicos que pode elevar seus privilégios ou explorar uma
vulnerabilidade para ganhar uma shell reversa como root;
E o Metasploit como adicional, contém diversas vulnerabilidades que são
constantemente usadas e digo que é bacana você explorar melhor essa
ferramenta;
https://www.offensive-security.com/metasploit-unleashed/
Escalação de
privilégio por
Kernel
Quando falamos de escalar privilégios para conseguir root, temos diversas
maneiras para que isso seja realizado e uma delas é via Kernel;
Muitos Kernel tem vulnerabilidades que permitem explorar uma brecha
para elevar root;
https://threatpost.com/local-privilege-escalation-flaw-in-linux-
kernel-allows-root-access/137748/
Usando o comando Uname –a ele mostra a versão do Kernel do seu alvo,
basta apenas procurar um exploit no exploit-db ou no próprio searchsploit;
Escalação de
privilégio por
Kernel -Example
Veja que temos diversos exploits e ai se o alvo possuir GCC
você pode subir uma servidor http utilizando python e com wget
baixar na máquina do alvo.
Filtro de pesquisa no Searchsploit:
searchsploit linux kernel 3.2 --exclude="(PoC)|/dos/"
Escalação de
privilégio por
Kernel -Example
Sempre vá para a pasta /tmp, são poucos casos raros que você
não vai conseguir escrever ou executar algo, então subiu o
arquivo.c, faz a compilação dele com gcc.
Caso na máquina não tenha, faça no seu Kali e já suba o arquivo
compilado, porém seu Kali for 64 bits e o alvo 32 bits, vai
precisar baixar essa biblioteca (apt-get install gcc-multilib)
E na hora da compilação em 32 digitar: gcc –m32 exploit.c –o
exploit
No alvo, de permissão de execução pro exploit, digitando:
chmod +x exploit e ai basta digitar em seguida ./exploit para
executar.
Escalaçãode privilégio
por Kernel –Exploit-db
https://payatu.com/guide-linux-privilege-escalation
https://www.youtube.com/watch?v=8rNsxbCgKzY
https://www.youtube.com/watch?v=3o5lUYmY0BA
https://www.youtube.com/watch?v=DODDAWnWD5k
Escalaçãode privilégio–
Pesquisararquivoscom
privilégiospara root
SUID e GUID
https://github.com/rebootuser/LinEnum
https://github.com/mzet-/linux-exploit-suggester
wget https://highon.coffee/downloads/linux-local-
enum.sh
Escalação de
privilégio por
Kernel
CVE-2010-2959 - 'CAN BCM' Privilege Escalation - Linux Kernel
< 2.6.36-rc1 (Ubuntu 10.04 / 2.6.32)
CVE-2010-3904 - Linux RDS Exploit - Linux Kernel <= 2.6.36-rc8
https://www.exploit-db.com/exploits/15285/
CVE-2016-5195 - Dirty Cow - Linux Privilege Escalation - Linux
Kernel <= 3.19.0-73.8
https://dirtycow.ninja/
Escalação de
privilégio - Linux
Outros métodos para escalar privilégios você pode encontrar
aqui:
https://gtfobins.github.io/
Seja via Docker, Perl, APT, SUDO e etc. Basta explorar e
pesquisar como aplicar esses métodos, uma ferramenta que vai
te ajudar é o LinEnum para detectar a melhor forma de
conseguir Root
https://www.youtube.com/watch?v=WgTL7KM44YQ
https://www.youtube.com/watch?v=_LyiOBGP9iw
https://www.youtube.com/watch?v=X_ixKHvOpJQ
https://www.youtube.com/watch?v=VF4In6rIPGc
https://www.youtube.com/watch?v=4nCnh6BHcUg
Escalação de
privilégio -Windows
Windows Server 2003 Priv Escalation:
https://www.exploit-db.com/exploits/6705
https://github.com/Re4son/Churrasco
Escalação de
privilégio -Windows
Windows Server 7/10 Priv Escalation Powershell:
https://www.exploit-db.com/exploits/39719
Psexec Priv Escalation:
Escalação de
privilégio -
Windows
Utilizando chaves de registros insegura para escalar privilégios
https://medium.com/@orhan_yildirim/windows-privilege-
escalation-insecure-registery-permissions-ad969880dcc3
https://medium.com/bugbountywriteup/privilege-escalation-
in-windows-380bee3a2842
https://tryhackme.com/room/windowsprivescarena
Escalação de
privilégio -
Windows
Outros métodos de escalação de privilégios:
https://sushant747.gitbooks.io/total-oscp-
guide/privilege_escalation_windows.html
https://www.youtube.com/watch?v=3BQKpPNlTSo
https://www.youtube.com/watch?v=C9GfMfFjhYI
https://www.youtube.com/watch?v=yXe4X-AIbps
https://www.fuzzysecurity.com/tutorials/16.html
Pós exploração-
Ferramentas
https://github.com/Hackplayers/evil-winrm
https://github.com/EmpireProject/Empire
https://github.com/byt3bl33d3r/SILENTTRINITY
https://github.com/topics/hackthebox
https://github.com/dostoevskylabs/dostoevsky-pentest-notes
https://linuxsecurity.expert/security-tools/post-exploitation-
tools
https://github.com/topics/post-exploitation
Dicas
Esse livro foi apenas para apresentar alguns conceitos básicos
de pós exploração, existem muito mais e daria um livro
originalmente publicado e bem legal só para falar de pós
exploração;
Mas se você quer aprimorar suas habilidades em PenTest eu
recomendo que você desenvolva laboratórios ou pratique em
um Hack the box, Vulnhub ou Try Hack Me;
Dá uma olhada em Writeups também, veja artigos do pessoal,
interaja com a comunidade para assim você aprender novas
técnicas e se aprofundar mais ainda;
Espero que a partir desse pequeno e-book você consiga ir atrás
de novos métodos, conhecer de maneira profunda maneira de
realizar pós exploração, pois é á dificuldade de muitos
PenTesters e a minha também kkkk;
Mas se você adquirir fundamentos, conhecer como a tecnologia
funciona, entender o seu processo, não será difícil encontrar
maneiras de utilizar para fins “maliciosos”
TryHarder
E claro, a metodologia que a Offensive Security utiliza é bastante
essencial nesse processo, pois em qualquer CTF você vai ter
que quebrar a cabeça para conseguir aquela flag;
Por isso, ser um try harder é nunca desistir e na dificuldade
achar o caminho certo, encontrar a chave para aquela porta de
aço reforçado;
Pensar fora da caixa é essencial, por isso um bom PenTester não
deixa de se atualizar e procurar diferentes tipos de meios para
sempre melhorar suas habilidades;
REFERENCE
https://subscription.packtpub.com/book/networking_and_servers/9781782163589/7/ch07lvl1sec34/what-is-
post-
exploitation#:~:text=As%20the%20term%20suggests%2C%20post,of%20it%20for%20malicious%20purposes.
https://www.sciencedirect.com/topics/computer-science/post-exploitation
https://metasploit.help.rapid7.com/docs/about-post-exploitation
https://www.anomali.com/pt/what-mitre-attck-is-and-how-it-is-useful
https://attack.mitre.org/
https://www.offensive-security.com/metasploit-unleashed/post-module-reference/
https://www.exploit-db.com/docs/english/18229-white-paper--post-exploitation-using-meterpreter.pdf
https://www.offensive-security.com/metasploit-unleashed/windows-post-gather-modules/
https://www.offensive-security.com/metasploit-unleashed/linux-post-gather-modules/
https://medium.com/canivete-sui%C3%A7o-hacker/metasploit-dismistificado-ii-5-
b6d3dc47b83c#:~:text=O%20Meterpreter%20%C3%A9%20uma%20payload,completion%2C%20canais%20e
%20outras%20fun%C3%A7%C3%B5es.
https://www.offensive-security.com/metasploit-unleashed/existing-scripts/
https://gohacking.com.br/treinamentos/ehpx-sp03.html
http://www.pentest-standard.org/index.php/Post_Exploitation
https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_-_linux.html
https://medium.com/@sdgeek/oscp-pen-testing-resources-271e9e570d45
https://github.com/Shiva108/CTF-notes/tree/master/OSCP-Materials-
master/Window%20Privilege%20Escalation%20and%20Post%20Exploitation
REFERENCE
https://purplesec.us/physical-penetration-testing/
https://www.hackers-arise.com/post/2018/11/26/metasploit-basics-part-21-post-exploitation-with-mimikatz
https://medium.com/@arnavtripathy98/smb-enumeration-for-penetration-testing-e782a328bf1b
https://www.offensive-security.com/metasploit-unleashed/meterpreter-basics/
https://www.slashroot.in/how-are-passwords-stored-linux-understanding-hashing-shadow-utils
https://netsec.ws/?p=337
https://xapax.gitbooks.io/security/content/spawning_shells.html
https://github.com/emilyanncr/Windows-Post-Exploitation
https://null-byte.wonderhowto.com/how-to/crack-shadow-hashes-after-getting-root-linux-system-0186386/
http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_-_linux.html
https://github.com/JoaoPauloF/OSCP/blob/master/OSCPnotes.md
https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/
https://www.youtube.com/watch?v=h5PRvBpLuJs&t=5s
https://www.youtube.com/watch?v=Bc7WoDXhcjM
https://www.udemy.com/course/linux-privilege-escalation-for-beginners/
https://www.udemy.com/course/windows-privilege-escalation-for-beginners/
https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA
https://acaditi.com.br/ (CEH)
