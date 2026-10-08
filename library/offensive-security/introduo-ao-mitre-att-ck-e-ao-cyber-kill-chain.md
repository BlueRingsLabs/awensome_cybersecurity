---
id: ckb-0c6ef8f35ed5
title: Introduo Ao MITRE Att Ck e Ao Cyber Kill Chain
category: offensive-security
format: course-notes
language: pt
tags: [mitre-attack, red-team]
summary: This course material introduces the concepts of Red, Blue, and Purple teaming, as well as the Mitre ATT&CK framework and the Cyber Kill Chain.
authors: [Joas Antonio Dos Santos]
license: NOASSERTION
added: 2026-10-04
classification:
  method: llm
  model: gemma-4-26b-a4b-it
  confidence: 0.95
classified_by: google:gemma-4-26b-a4b-it@2026-10-08T01:01:57Z
---

Introdução ao Mitre Att&ck e
ao Cyber Kill Chain
Joas Antonio
Objetivo do curso
• Red Team vs PenTest
• Purple Team e Red Team
• Red Team Operations
• Conhecendo o conceito de Mitre Att&ck e Cyber Kill Chain
• Como funciona o processo de Adversary Emulation
• Usando o Mitre Att&ck Navigator para estruturar TTPs
• Cracking the Perimeter ou Cracking The Bridge
• Conclusão
26/06/2021
Sobre mim
• Ethical Hacker in Inmetrics, Information Security Researcher, Ethical Hacking and PenTest
Independent, OWASP Member and Researcher, Cybrary Teacher Assistant, Microsoft Innovative
Educator Instructor, Web Developer (Front-End and Back-End), Bug Hunter by HackerOne and
OBB, Python Developer Expert, Shell Script Expert, has over +800 technology courses and +50
certifications, SANS Member, Mitre Att&ck Contributor, Red Team Village Contributor, Texas Cyber
Security Summit Contributor, 1000 CEH Hall of Fame, CIS Member and Research, Infosec
Competence Leader in Security Awareness, Cyber Security Mentor, Cyber Security Awards Finalist
2020, Article and Book Writer, Cracking The Perimeter Framework Creator, Vulnerable Machine
Engineering by Offensive Security, Cyber Security Tutors Founder, Hakin9 Magazine Contributor,
Exin Ethical Hacking Foudation Instructor, Exploit Developer and IT lover.
I love computers since I was 7 years old and in love with the information security area since I was
10 years old.
OSWP | CEH ANSI | CEH Practical | CEH Master | eJPT | OSCP (In Progress 99%)
19years|Asperger
• LinkedIn: https://www.linkedin.com/in/joas-antonio-dos-santos
26/06/2021
Red Team vs PenTest
Joas Antonio
6/26/2021
Red Team vs
PenTest
Other Security Tests
26/06/2021
Red Team vs PenTest
26/06/2021
Red Team vs PenTest
6/26/2021
O que é PenTest
• Pen testing is a process for testing a system, network, web
application, facility or some other resource in order to find as many
vulnerabilities and configuration issues as possible within the time
allotted. Pen testers then exploit those vulnerabilities to determine
the risk of the vulnerabilities.
• Pen testers aren't seeking to discover new vulnerabilities -- zero
days. They aim to find already known but unpatched system
vulnerabilities.
• During a typical pen test, pen testers aim to find a version of installed
software that is known to be vulnerable and then exploit that
vulnerability. This process continues: find other vulnerabilities and
exploit them, combining the attacks in order to reach the end goal.
26/06/2021
O que é Red Team
• Red teaming shares many similarities with pen testing; however, the goals are
different. Red teaming is more scenario-driven than pen testing. The goal of red
team engagements is not just to test the environment and the systems within the
environment, but to test the people and processes of the organization as well.
• Typical red team scenarios include exploiting lost laptops, unauthorized devices
connected to the internal network and compromised DMZ hosts, as well as
testing how the security operations center (SOC) or blue team react to an
advanced persistent threat. Will the SOC or blue team defenders notice when an
employee is exfiltrating data from the network?
• Red teams may also use scenario-driven testing for detection and response, like
testing a business's ability to detect and manage external threats, like phishing
campaigns, social engineering attempts, attempts to gain physical access to the
site, website compromise assessments, protection software evasion, lateral
movement across networks and many other attacks, depending on the
complexity of an organization's systems.
26/06/2021
Purple Team e Red Team
Joas Antonio
6/26/2021
Red Team and Blue Team = Purple Team
26/06/2021
Red Team and Blue Team = Purple Team
26/06/2021
• O Purple Team trabalha em sinergia com Red e Blue Teams, com a missão
de alcançar um nível ainda maior de segurança dentro da organização,
explorando ao máximo rotinas de ataque e defesa, pensando em como
reforçar táticas, técnicas e procedimentos (TTP) de defesa.
• Essa abordagem ajuda a desenvolver e melhorar as duas equipes. A
equipe azul fica mais informada sobre como priorizar, medir e melhorar
sua capacidade de detectar e se defender contra ameaças e ataques, e a
equipe vermelha obtém uma visão do setor sobre tecnologias e
mecanismos usados na defesa.
•
Benefícios do Purple Team
26/06/2021
Comunicação
•
Conforme descrito, o objetivo das equipes vermelha e azul é reforçar a segurança de uma organização, assim como a meta da organização é
promover a conscientização sobre a segurança cibernética . Com o time roxo, o primeiro objetivo é uma comunicação clara e regular entre os
times vermelho e azul, um fluxo constante de informações e esforço simbiótico. Este exercício, recomendado para ser realizado pelo menos uma
vez por ano e sempre que ocorram mudanças significativas, entre as duas equipas, facilita a comunicação e colaboração constantes entre as
equipas, promovendo melhorias constantes na cultura de cibersegurança da organização.
Perspectiva
•
Freqüentemente, uma violação pode ocorrer com o invasor evitando todas as defesas, sem qualquer conhecimento ou detecção da equipe
azul. Devido ao constante estado de mudança na segurança cibernética, isso nem sempre indica uma falta de habilidade ou tecnologia na equipe
azul, mas sim a crescente complexidade dos métodos dos agentes de ameaça e / ou vetores de ataque. O conceito de 'time roxo' efetivamente
elimina essa possibilidade.
•
As equipes vermelha e azul, trabalhando juntas, fornecem transferência de conhecimento regular e consistente, melhorando a capacidade da
organização de impedir cenários de ataque da vida real. No final, a equipe vermelha melhorará os processos de gerenciamento de vulnerabilidade
da organização e a equipe azul aprenderá a entrar na mentalidade dos invasores, portanto, a equipe roxa permite o desenvolvimento de melhores
programas de resposta a incidentes e processos de detecção de vulnerabilidade.
Postura
•
O último benefício que abordaremos também é o benefício importante, e essa é uma postura de segurança mais saudável para sua
organização. Fazendo uso da comunicação constante das equipes roxas, testes anuais de penetração, gerenciamento de vulnerabilidade e
desenvolvimento de infraestrutura e políticas de segurança aprimoradas, as organizações colocam seu melhor pé à frente contra a ameaça de
uma violação de dados.
Red Team
Operations
Joas Antonio
6/26/2021
Red Team Operations
• Once the objectives are set, the red team starts by conducting initial
reconnaissance. Mandiant leverages a combination of proprietary intelligence
repositories as well as open-source intelligence (OSINT) tools and techniques to
perform reconnaissance of the target environment.
• Mandiant attempts to gain initial access to the target environment by exploiting
vulnerabilities or conducting a social engineering attack. Mandiant leverages
techniques used by real-world attackers to gain privileged access to these
systems.
• Once access is gained, the red team attempts to escalate privileges to establish
and maintain persistence within the environment by deploying a command and
control infrastructure, just like an attacker would.
• After persistence and command and control systems are established within the
environment, the red team attempts to accomplish its objectives through any
non-disruptive means necessary
26/06/2021
Red Team Operations
Red Team Operations are recommended for organizations that want
to:
• Test detection and response capabilities. Security teams prepare for
real world incidents, but you need to confirm that they can respond
properly — without real risk.
• Raise awareness and show impact. The Mandiant red team behaves
like realworld attacker, working n compromise your environment from
the Internet by using information only available to the Internet.
Successful red team engagements can help justify increased security
budgets and identify gaps that require further investment.
26/06/2021
Red Team Operations – Attack Lifecycle
6/26/2021
Conhecendo o Mitre Att&ck
e o Cyber Kill Chain
Joas Antonio
6/26/2021
Mitre Att&ck
6/26/2021
• O MITRE introduziu o ATT&CK (Adversarial Tatics, Techniques & Common
Knowledge) em 2013 como uma forma de descrever e categorizar os
comportamentos adversários baseado em observações reais do cenário
global. o ATT&CK é uma lista estruturada de comportamentos conhecidos
de atacantes que foram compilados em táticas e técnicas, expressados em
uma série de matrizes assim como em STIX/TAXII.
• Por ser uma representação compreensiva de comportamentos que os
atacantes empregam quando estão comprometendo as redes, tornou-se
muito útil para mensurar medidas de defesa e ofensivas.
• O framework ATT&CK é valoroso para uma série de configurações.
Qualquer atividade de defesa pode se beneficiar de aplicar as diretrizes do
framework. Além de oferecer uma linguagem comum para os profissionais,
o ATT&CK também fornece a fundação para atividades de pentest e Red
Team. Isso dá a ambas as equipes um padrão comum de comunicação ao
se falar sobre os comportamentos adversários.
Mitre Att&ck
6/26/2021
Cyber Kill Chain
Desenvolvido pela Lockheed Martin, a estrutura
Cyber Kill Chain® faz parte do modelo Intelligence
Driven Defense® para identificação e prevenção de
atividades de intrusões cibernéticas. O modelo
identifica o que os adversários devem completar para
atingir seu objetivo.
https://www.lockheedmartin.com/en-
us/capabilities/cyber/cyber-kill-chain.html
6/26/2021
Cyber Kill Chain
A cadeia de eventos, ou cadeia de destruição, pela qual um invasor externo deve passar é definida no CKC em um
nível tático, conforme mostrado:
•
Reconhecimento: Atividades de reconhecimento passivo ou ativo para identificar alvos para potenciais
fraquezas. Avaliação de cada inteligência possível em relação ao melhor curso de ação.
•
Armamento: criação ou localização de malware de acesso remoto adequado para explorar potenciais fraquezas
ou vulnerabilidades, acoplando-o em cargas úteis (como os tipos de arquivo mais usados)
•
Entrega: entrega a carga útil ao ambiente de destino. Principalmente combinado com quaisquer outras fraquezas
descobertas na fase de reconhecimento. Aqui, o vetor de ataque pode ser incluído em e-mails, usando sites mal-
intencionados ou hackeados ou usando USB, etc.
•
Exploração: está provocando a execução da carga útil. Ele pode ser disparado automaticamente, como a
execução de um programa de download ou a execução de arquivos em USB ou técnicas mais avançadas, como
ataque direcionado usando engenharia social, etc., são possíveis.
•
Instalação: instalação de carga útil para criar um canal consistente entre a vítima e o invasor. Principalmente o
backdoor é implantado para manter a presença neste ponto.
•
Comando e Controle: Estabelecendo um canal C&C. Isso permite que os invasores tenham um ponto central
para direcionar e alcançar os objetivos no ambiente de destino.
•
Ação em Objetivos: Rodada final para atingir os objetivos originais, o impacto é máximo, como exfiltração de
dados confidenciais ou comprometimento da integridade ou disponibilidade dos sistemas.
26/06/2021
Mitre Kill Chain
•
Cyber ​Intrusion Kill Chain, também conhecido como Kill
Chain, foi adaptado de conceitos militares. Os
engenheiros de Locked Martin foram os primeiros a
adaptá-lo à área de segurança cibernética. O núcleo da
estrutura surgiu da estrutura de ataque. Ele descreve um
processo ponta a ponta, ou toda a cadeia de eventos,
que é necessário para realizar um ataque bem-sucedido.
•
O Kill Chain pode ser usado tanto para conduzir um
ataque quanto para detectar, bem como defender um
ataque. Quando a defesa está em ação, estamos falando
sobre quebrar a cadeia de morte de um oponente,
tornando um ataque malsucedido. O modelo CKC da
Lockheed Martin serve como o primeiro e o ponto de
partida para analisar ataques de APT e malware. De
acordo com os pesquisadores da Lockheed Martin, a
cadeia de destruição completa pode ser definida como "o
agressor deve desenvolver uma carga útil para violar um
limite confiável, estabelecer uma presença dentro de um
ambiente confiável e, a partir dessa presença, agir em
direção aos seus objetivos"
26/06/2021
Como funciona o processo
de Adversary Emulation?
Joas Antonio
6/26/2021
Adversary Emulation
26/06/2021
• Para aqueles que não estão familiarizados com isso, a emulação do
adversário é um tipo de engajamento da equipe vermelha que imita
uma ameaça conhecida a uma organização, combinando inteligência
de ameaças para definir quais ações e comportamentos a equipe
vermelha usa. Isso é o que diferencia a emulação do adversário dos
testes de penetração e outras formas de formação de equipes
vermelhas. Emuladores de adversários constroem um cenário para
testar certos aspectos das táticas, técnicas e procedimentos (TTPs) de
um adversário. A equipe vermelha então segue o cenário enquanto
opera em uma rede alvo a fim de testar como as defesas podem se
sair contra um adversário emulado.
Adversary
Emulation
• Como a ATT&CK é uma grande base de
conhecimento dos comportamentos
adversários do mundo real, não é
preciso muita imaginação para
estabelecer uma conexão entre os
comportamentos do adversário ou da
equipe vermelha e a ATT&CK. Vamos
explorar como as equipes de
segurança podem utilizar ATT&CK para
emulação de adversário para ajudar a
melhorar sua organização!
26/06/2021
Adversary
Emulation – Nivel
1
• Equipes pequenas e aquelas
voltadas principalmente para a
defesa podem obter muitos
benefícios com a emulação do
adversário, mesmo que não
tenham acesso a um Red Team.
• Atomic Red Team , um projeto de
código aberto mantido pela Red
Canary, é uma coleção de scripts
que pode ser usada para testar
como você pode detectar certas
técnicas e procedimentos
mapeados para técnicas ATT&CK.
26/06/2021
Adversary Emulation – Nivel 1
26/06/2021
• O Atomic Red Team pode ser usado para testar técnicas e
procedimentos individuais para verificar se a análise comportamental
e os recursos de monitoramento estão funcionando conforme o
esperado.
• O repositório Atomic Red Team tem muitos testes, cada um com um
diretório dedicado à técnica ATT&CK que é testada. Você pode
visualizar o repositório completo no formato ATT&CK Matrix .
• https://github.com/redcanaryco/atomic-red-
team/blob/master/atomics/Indexes/Indexes-Markdown/index.md
APT 3 Emulation Plan - Example
Joas Antonio
6/26/2021
Adversary Emulation – Nivel 2
26/06/2021
• Para aqueles de vocês que já têm recursos de Red Team, você pode tirar
muito proveito da integração da ATT & CK com seus compromissos
existentes. O mapeamento das técnicas usadas em uma contratação de
equipe vermelha para a ATT & CK fornece uma estrutura comum ao
escrever relatórios e discutir mitigações.
• Para começar, você pode pegar uma ferramenta ou operação planejada
existente que você usa e mapeá-la para a ATT & CK. O mapeamento dos
procedimentos do Red Team para a ATT & CK é semelhante ao
mapeamento da inteligência sobre ameaças para a ATT & CK.
• Outro recurso útil para começar a mapear os procedimentos da equipe
vermelha para ATT&CK é o APT3 Adversary Emulation Field Manual , que
apresenta ações de comando por comando que o APT3 usou, todas
mapeadas para ATT&CK.
Adversary
Emulation – Nivel
3
•
Nesse ponto, seu Red Team está integrando a ATT & CK nas operações e encontrando valor na comunicação com a equipe azul. Para avançar
suas equipes e o impacto que estão tendo ainda mais, você pode colaborar com a equipe de CTI de sua organização para ajustar os
compromissos em relação a um adversário específico usando os dados que coletam criando seu próprio plano de emulação de adversário.
•
A criação de seu próprio plano de emulação de adversário baseia-se na maior força de combinar equipe vermelha com sua própria inteligência
de ameaças: os comportamentos são vistos por adversários do mundo real mirando em você! O Red Team pode transformar essa informação
em testes eficazes para mostrar quais defesas funcionam bem e onde os recursos são necessários para melhorar. Há um nível de impacto
muito mais alto quando as lacunas de visibilidade e controles são expostas por testes de segurança, quando você pode mostrar uma alta
probabilidade de que elas foram aproveitadas por um adversário conhecido. Vincular seu próprio CTI aos esforços de emulação do adversário
aumentará a eficácia dos testes e os resultados para que a liderança sênior promova a mudança.
26/06/2021
Adversary Emulation – Service Process
26/06/2021
Adversary Emulation – Tools Examples
26/06/2021
• MITRE CALDERA - An automated adversary emulation system that performs post-
compromise adversarial behavior within Windows Enterprise
networks. https://github.com/mitre/caldera
• APTSimulator - A Windows Batch script that uses a set of tools and output files to make a
system look as if it was compromised. https://github.com/NextronSystems/APTSimulator
• Atomic Red Team - Small and highly portable detection tests mapped to the Mitre
ATT&CK Framework. https://github.com/redcanaryco/atomic-red-team
• Network Flight Simulator - flightsim is a lightweight utility used to generate malicious
network traffic and help security teams to evaluate security controls and network
visibility. https://github.com/alphasoc/flightsim
• Metta - A security preparedness tool to do adversarial
simulation. https://github.com/uber-common/metta
• Red Team Automation (RTA) - RTA provides a framework of scripts designed to allow blue
teams to test their detection capabilities against malicious tradecraft, modeled after
MITRE ATT&CK. https://github.com/endgameinc/RTA
Usando o Mitre Att&ck Navigator para estruturar TTPs
Joas Antonio
6/26/2021
Fleury Revil -
Example
• https://mitre-
attack.github.io/attack-navigator/
• https://github.com/CyberSecurity
UP/TTPs-Mitre-Attack
26/06/2021
Cracking the Perimeter
ou Cracking The Bridge
Joas Antonio
6/26/2021
Cracking the Perimeter ou Cracking The
Bridge – O que é?
• O Cracking The Perimeter foca em testar os controles de segurança de defesa de várias formas, sabemos
que 0day é constante e uma equipe preparada para validar se seu ambiente está suscetível a ataques
dessas ameaças desconhecidas, trabalhando em conjunto com a equipe de Threat Intelligence e Threat
Hunter para coletar inteligência de ameaças, novos CVEs, 0days vendidos ao mercado e PoCs de
vulnerabilidade. A equipe de quebra de perímetro é precisamente treinada para testar os controles de
segurança e se aprofundar na busca de 0days.
https://github.com/CyberSecurityUP/Cracking-The-Perimeter-Framework/blob/main/CTP%20-
%20Framework%201.0%20-%20Portugues%20Version.pdf
26/06/2021
Conclusão
26/06/2021
https://www.linkedin.com/in/joas-antonio-dos-santos
Referências
• https://www.packetlabs.net/red-team-vs-blue-team/
• https://searchsecurity.techtarget.com/answer/Penetration-testing-vs-red-team-Whats-the-difference
• https://www.appknox.com/blog/penetration-testing-vs-red-team-what-is-the-difference
• https://www.fireeye.com/content/dam/fireeye-www/services/pdfs/pf/ms/ds-red-team-operations.pdf
• https://medium.com/mitre-attack/getting-started-with-attack-red-29f074ccf7e3
• https://realprotect.net/o-que-e-o-mitre-attck-e-como-ele-pode-melhorar-sua-cybersecurity/
• https://www.anomali.com/pt/resources/what-mitre-attck-is-and-how-it-is-useful
• https://www.mcafee.com/enterprise/pt-br/security-awareness/cybersecurity/what-is-mitre-attack-
framework.html
• https://www.rapid7.com/fundamentals/mitre-attack/
• https://www.threatq.com/mitre-attack/
• https://www.kaspersky.com/enterprise-security/mitre-attack
• https://www.redteamsecure.com/approach/red-teaming-methodology
26/06/2021
