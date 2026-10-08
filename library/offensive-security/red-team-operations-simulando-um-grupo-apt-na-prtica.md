---
id: ckb-3dc46b909213
title: Red Team Operations Simulando Um Grupo APT Na Prtica
category: offensive-security
format: course-notes
language: pt
tags: [evasion, malware, mitre-attack, powershell, red-team, windows]
summary: This document provides an overview of red team operations by analyzing the tactics, techniques, and procedures used by APT groups, including evasion methods like AMSI bypass and direct syscalls.
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemini-3.1-flash-lite
  confidence: 0.95
classified_by: google:gemini-3.1-flash-lite@2026-10-08T00:57:35Z
---

Red Team Operations –
Simulando um grupo APT na prática
O que é APT
APT (Advanced Persistent Threat) é um grupo ou ator de ameaça que
realiza ataques cibernéticos sofisticados, prolongados e direcionados a
uma entidade específica, geralmente visando roubar informações valiosas
ou causar danos. Esses ataques são caracterizados por:
- Persistência
- Furtividade
- Capacidade de se adaptar
- Evasão de detecções
ANATOMIA
fonte: SOC Investigations
fonte: Google Image Search
MITRE ATT&CK E TTPS
as táticas são os
objetivos táticos que
uma ameaça pode usar
durante uma operação.
as técnicas descrevem as
ações que as ameaças
realizam para atingir
seus objetivos.
os procedimentos são as
etapas técnicas
necessárias para
executar a ação.
fonte: redteam.guide
Modus Operandi - APT29 E APT 38
APT29 (também conhecido como "Cozy Bear" ou "The Dukes")
Origem: APT29 é amplamente associado ao governo russo, especificamente ao Serviço de
Inteligência Estrangeira (SVR).
Operação: Estima-se que o grupo esteja ativo desde pelo menos 2008.
APT38 (também conhecido como "Lazarus Group")
Origem: APT38 é amplamente associado ao governo da Coreia do Norte, especificamente à
Bureau 121, a unidade de guerra cibernética do país.
Operação: Estima-se que o grupo esteja ativo desde pelo menos 2009
Cadeia de Ataque UNC3313
fonte: Security Affairs
Cadeia de Ataque APT29
fonte: Mitre Center for Threat Informed Defense
Cadeia de Ataque APT29
fonte: Fortinet
Cadeia de Ataque APT38
fonte: Radware
Exemplos:
Táticas, Técnicas e Procedimentos
Acesso Inicial – Spear-Phishing
- Top Domain Levels
(Ex: .xyz, .io, .to,
.xxx)
- - Cloudflare
Turnstile (Evitar
Bots)
- - Whois Privado
- - IDN Homograph e
Punycode
fonte: ResearchGate
Execução – AMSI Bypass
Quando um usuário executa um
script ou abre o PowerShell, o
AMSI.dll é carregado na memória do
processo. Antes do script rodar, o
antivírus usa as funções
AmsiScanBuffer() e
AmsiScanString() para verificar o
código em busca de sinais de
malware. Se algo suspeito for
encontrado, o script é bloqueado e o
antivírus mostra uma mensagem
informando que a execução foi
impedida.
fonte: Pentest Laboratories
Execução – AMSI Bypass
A imagem mostra um comando
PowerShell onde o usuário tenta
contornar a Interface de Verificação
de Malware (AMSI) do Windows para
executar um script bloqueado.
Inicialmente, o download de um
script foi bloqueado pelo software
antivírus, então o usuário utilizou um
código para desativar o AMSI antes
de tentar executar novamente o
comando bloqueado.
fonte: MDSec
Persistência – Técnicas
fonte: Science Direct
Persistência – Backdoor com Lib-nosa
lib-nosa é uma biblioteca C minimalista projetada para
facilitar conexões de socket por meio de operações IOCTL do
driver AFD no Windows. Ao ignorar o winsock2.h ->
(ws2_dll.dll)cabeçalho tradicional, lib-nosa interage
diretamente com as APIs de socket internas do AFD (Ancillary
Function Driver for WinSock), oferecendo aos desenvolvedores
uma alternativa leve e de baixo nível para programação de
rede.
fonte: ViperX by Alexa Souza
Escalação de Privilégios - Técnicas
fonte: Certcube
Defense Evasion – Syscall Direta
Neste método, o malware
implementa diretamente o stub de
syscall no código assembly, o que
significa que ele faz a transição do
modo de usuário para o modo
kernel sem passar pelas funções
das bibliotecas nativas do Windows,
como ntdll.dll. Em vez de invocar a
API NtCreateFile da ntdll.dll, o
malware executa diretamente as
instruções de assembly necessárias
para invocar a syscall. Isso envolve
preparar os registradores e chamar
a instrução syscall.
fonte: RedOps
Defense Evasion – Syscall Indireta
Na syscall indireta, o malware utiliza
a ntdll.dll para executar a chamada
de sistema. O malware invoca a
função NtCreateFile na ntdll.dll, que
por sua vez faz a transição para o
kernel. Isso significa que a
execução do comando syscall
ocorre na memória legítima da
ntdll.dll. Após a execução da syscall
no kernel, o retorno do fluxo de
execução ocorre também na
memória da ntdll.dll
fonte: RedOps
Defense Evasion – Técnicas Gate
Hells Gate: Técnica de evasão avançada que executa syscalls diretamente,
sem passar pelo código de ntdll.dll, onde os EDRs geralmente aplicam hooks.
Ao evitar a biblioteca, o Hells Gate consegue realizar chamadas ao kernel
de forma transparente, minimizando o risco de detecção e aumentando a
furtividade de malwares.
Defense Evasion – Técnicas Gate
Halo's Gate: Variante do Hells Gate, o Halo's Gate utiliza uma técnica de
syscall indireta, resolução de SSN comparando funções vizinhas para
determinar se estão hookadas.
Ao evitar funções monitoradas, ele calcula o syscall correto e o invoca
diretamente, contornando proteções de EDRs e outros sistemas de segurança que
monitoram ntdll.dll.
Defense Evasion – Técnicas Gate
HookChain: Através de uma combinação precisa de técnicas de IAT Hooking,
resolução dinâmica de SSNs e chamadas de sistema indiretas, o HookChain
redireciona o fluxo de execução dos subsistemas do Windows de maneira que
permanece invisível aos olhares vigilantes dos EDRs que atuam somente na
Ntdll.dll, sem necessitar de alterações no código-fonte das aplicações e
malwares envolvidos.
fonte: Helvio Junior aka M4v3r1ck
Defense Evasion – Técnicas Gate
Heavens Gate: Técnica que permite a execução de código
de 64 bits a partir de um processo de 32 bits, conhecida como uma forma de evasão
de arquiteturas mistas.
Heavens Gate aproveita as diferenças entre modos de execução para contornar
proteções e permitir a execução de código malicioso em ambientes restritos.
Quando um aplicativo de 32 bits rodando dentro de um processo de 64 bits precisa chamar
uma função ou interface de sistema de 64 bits, ele deve alternar o processador para o
modo de 64 bits.  É aqui que a técnica Heaven's Gate entra em jogo.
A técnica envolve a execução de uma instrução syscall especial, valor do registrador
code segment: para x86: 0x23, x64: 0x33 que aciona uma troca de contexto do modo de 32
bits para o modo de 64 bits, alterando efetivamente o conteúdo do registro CS.
Defense Evasion – Técnicas Gate
Phantoms Gate: PhantomsGate é uma técnica sofisticada
de injeção de shellcode que utiliza Hell's Gate para
encontrar números de syscalls dinamicamente, modifica
chamadas de sistema para enganar os EDRs e usa o
sequestro de threads para injetar e executar shellcode
em um processo.
Defense Evasion – Drivers Vulnerável
fonte: InfoSec Write Ups by EINiak
Defense Evasion – Process Injection
Mockingjay
A injeção é executada sem alocação de espaço,
configuração de permissões ou mesmo início de um
thread. A exclusividade dessa técnica é que ela requer
uma DLL vulnerável e cópia de código para a seção
correta.
fonte: Security Joes by Thiago Peixoto
Credential Access – Técnicas
fonte: Elastic Global
Movimentação Lateral – Técnicas
●Pass-the-Hash: Técnica onde o invasor usa a hash de senha do usuário para autenticar-se
em outros sistemas, sem precisar conhecer a senha em si.
# psexec.py -hashes <NTLM_HASH> <domain>/<username>@<target_ip>
●Remote Services: Acesso a serviços remotos como RDP, SMB ou SSH para mover-se de um
sistema comprometido para outro.
# mstsc /v:<target_ip>
●Windows Admin Shares: Uso de compartilhamentos administrativos do Windows (como C$,
ADMIN$) para transferir arquivos ou executar comandos remotamente em outros sistemas
dentro do mesmo domínio.
# net use \\<target_ip>\C$ /user:<domain>\<username> <password>
Movimentação Lateral – Técnicas
fonte: Wizlynx Group
Exfiltração – Técnicas
●Dados comprimidos (zip do zip)
●Dados codificados (Base64)
●Dados criptografados (Simétrico e Assimétrico)
●Limites de tamanho de transferência de dados -> fragmentos
de dados (separar arquivos em bytes menores)
●Exfiltração por protocolo alternativo (SSH, DNS, SFTP, SMTP,
HTTPS)
●Exfiltração por canal de C2
●Exfiltração por meio físico (Pendrives, HD Externos e etc)
Exfiltração – Técnicas
fonte: ResearchGate
REFERÊNCIAS
https://www.socinvestigation.com/anatomy-of-the-ransomware-cybercrime-economy/
https://prodigy13.com/kill-chain-pros-cons/
https://redteam.guide/
https://securityaffairs.com/128493/malware/unc3313-apt-two-backdoors.html
https://www.researchgate.net/figure/Data-Exfiltration-via-DNS-queries_fig1_359077112
https://www.fortinet.com/blog/threat-research/teamcity-intrusion-saga-apt29-suspected-exploiting-cve-
2023-42793
https://www.radware.com/cyberpedia/ddos-attacks/the-lazarus-group-apt38-north-korean-threat-actor/
https://www.researchgate.net/figure/Phases-of-a-common-Spear-Phishing-attack_fig1_361946872
https://pentestlaboratories.com/2021/05/17/amsi-bypass-methods/
https://www.mdsec.co.uk/2018/06/exploring-powershell-amsi-and-logging-evasion/
https://www.sciencedirect.com/science/article/pii/S0167404822002498
https://github.com/ViperXSecurity/lib-nosa
https://blog.certcube.com/windows-privilege-escalation-methods/
https://redops.at/en/blog/direct-syscalls-vs-indirect-syscalls
https://github.com/helviojunior/hookchain
https://infosecwriteups.com/byovd-attacks-the-hidden-threats-of-vulnerable-drivers-d1aebe9b552e
https://www.securityjoes.com/post/process-mockingjay-echoing-rwx-in-userland-to-achieve-code-execution
https://www.elastic.co/es/blog/elastic-global-threat-report-breakdown-credential-access
https://www.wizlynxgroup.com/us/cyber-security-usa/red-team-assessment-services
https://www.researchgate.net/figure/Data-Exfiltration-via-DNS-queries_fig1_359077112
