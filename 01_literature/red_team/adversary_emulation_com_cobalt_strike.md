[[ PAGE 1 ]]
Introdução ao 
Adversary Emulation
com Cobalt Strike
Joas A Santos
[[ PAGE 2 ]]
Whoami
• Red Team Leader, Instructor and Ambassador for 
HackerSec, contributor and researcher for Mitre, with 30 
CVEs currently reported, holding 90 international 
certifications, speaking at major companies and national 
and international events, author of books and offensive 
security researcher at Synack Red Team.
[[ PAGE 3 ]]
Spoiler
[[ PAGE 4 ]]
O que é Adversary Emulation?
• Utiliza-se táticas, técnicas e procedimentos de adversários, coletados 
pelo time de Threat Intelligence, para criar um teste de segurança 
baseado em campanhas de intrusão do mundo real;
• O foco é saber aonde priorizar os recursos de segurança e identificar 
as lacunas do ambiente;
• Mapeando grupos de ameaça (APT) e utilizando como base para criar 
modelos de ameaças para testes;
[[ PAGE 5 ]]
Plano de Threat
Emulation
• Os planos de emulação de 
adversários descrevem o 
comportamento de grupos de 
ameaças persistentes 
mapeados para ATT&CK . Eles 
são usados ​por equipes de 
emulação adversárias para 
testar a segurança de rede e 
os produtos de segurança de 
uma organização contra 
ameaças específicas.
[[ PAGE 6 ]]
Ferramentas utilizadas para Adversary
Emulation
[[ PAGE 7 ]]
Sobre o Cobalt Strike
• Cobalt Strike é uma plataforma para simulações de adversários 
e operações de Red Team. O produto foi projetado para 
executar ataques direcionados e emular as ações pós-
exploração de agentes de ameaças avançadas. Usando o 
principal framework de mercado Cyber Kill Chain como base.
[[ PAGE 8 ]]
Processo de Simulação com o Cobalt Strike
Reconhecimento 
Armamento (Doc 
Maliciosos, DLLs, 
Scrips e etc)
Entrega (Phishing)
Controle da rede e 
dos ativos através do 
Beacon
Realização de 
Escalação de 
Privilégios usando 
scripts inclusos
Realização de 
Movimentação 
Lateral
Exfiltração dos 
dados
[[ PAGE 9 ]]
Encriptação e Decriptação de Dados -
Exemplo
[[ PAGE 10 ]]
Cobalt Strike - Comunicação
[[ PAGE 11 ]]
C2 Profile
• A configuração primária da ferramenta Cobalt Strike é especificada 
usando um arquivo de perfil. A ferramenta usa os valores presentes 
no perfil para gerar a carga útil do Beacon, e os usuários criam o perfil 
e definem seus valores com uma linguagem de domínio chamado 
Maleable Command and Control (C2).
• Dentro de um perfil, as opções são divididas em opções globais e 
opções locais. 
• As opções globais atualizam as configurações globais do Beacon.
• Enquanto as opções locais são específicas da Requisição, conforme é 
a interação com o beacon. 
[[ PAGE 12 ]]
Configuração de Profile
•
http-stager : O Beacon é um payload preparado. O stager baixa 
o arquivo e o injeta na memória. Os valores listados nesta 
transação estão customizando a comunicação HTTP para 
download do beacon.
•
http-get: O processo http-get personaliza a comunicação HTTP 
entre o Beacon e o servidor Cobalt. O Beacon começa 
enviando a solicitação HTTP com metadados sobre o sistema 
comprometido. Se o servidor do cobalt tiver tarefas a serem 
executadas, o servidor enviará uma resposta HTTP.
•
http-post: Uma vez que o Beacon executa as tarefas enviadas 
pelo servidor, a saída da tarefa é transferida na requisição http-
post . Os valores listados nesta transação afetam a 
comunicação HTTP quando a saída da tarefa é enviada para o 
servidor.
•
https-certificate: Se o Beacon for encarregado de se comunicar 
por HTTPS, o servidor cobalt gerará um certificado 
autoassinado. O servidor usa valores de requisição http-
get e http-post para criar solicitações e respostas HTTP 
reais. Esta transação de perfil pode ajudar a especificar os 
diferentes parâmetros para certificados SSL.
[[ PAGE 13 ]]
Kit de Artefatos
• O Cobalt Strike usa o Artifact Kit para gerar seus executáveis ​e DLLs. O 
Artifact Kit, qcontém uma coleção de kits com uma estrutura de 
código-fonte para criar executáveis ​e DLLs que ajudam na evasão de 
alguns AV/EDR;
• Existem várias formas de você modificar os Artifact Kits para evasão:
• Implementando syscall criando um payload customizado
• Entendendo o comportamento e definindo o ponto de alteração usando 
PEZor ou qualquer outra ferramenta manipulação de shellcode
• Alterando chamadas de API do Windows e seus respectivos valores (Ex
comum: Alteração das Api de alocação de memória como VirtualAlloc e 
HeapAlloc)
[[ PAGE 14 ]]
Projetando seu C2
• Projetar uma infraestrutura C2 robusta envolve a criação de várias 
camadas de Comando e Controle. Estes podem ser descritos como 
níveis. Cada camada oferece um nível de capacidade e cobertura. A 
ideia de usar vários níveis é o mesmo que não colocar todos os ovos 
na mesma cesta. Se C2 for detectado e bloqueado, ter um backup 
permitirá que as operações continuem.
• Os níveis C2 geralmente se enquadram em três categorias: Interativo, 
Curto Curso e Longo Curso. Às vezes, eles são rotulados como Nível 1, 
2 ou 3. Não há nada exclusivo para cada nível além de como eles 
devem ser usados.
[[ PAGE 15 ]]
Projetando seu C2 - Níveis
Joas A Santos
Based on Red Team Guide
[[ PAGE 16 ]]
Níveis do C2
Interativo (N3)
• Usado para comandos gerais, enumeração, varredura, exfiltração de dados, etc.
• Este nível tem a maior interação e está em maior risco de exposição.
• Planeje a perda de acesso por falha de comunicação, falha do agente ou ações do Blue Team.
• Execute sessões interativas suficientes para manter o acesso. Embora interativo, isso não significa 
explodir o cliente com pacotes. Use o bom senso para minimizar a interação apenas o suficiente para 
executar uma ação.
Short Haul (N2)
• Usado como backup para restabelecer as sessões interativas.
• Use comunicações secretas que se misturem com o alvo.
• Tempos de retorno de chamada lentos. Tempos de retorno de chamada em 1–24 horas.
Long Haul (N1)
• O mesmo que o Short Haul, mas ainda mais baixo e lento.
• Tempos de retorno de chamada lentos. Tempos de retorno de chamada de mais de 24 horas são 
comuns.
[[ PAGE 17 ]]
Criando um plano de Emulação
• Um plano de emulação de ameaças é uma estratégia abrangente projetada para 
simular ataques cibernéticos do mundo real e avaliar a eficácia dos controles de 
segurança e procedimentos de resposta a incidentes de uma organização. O 
objetivo de um plano de emulação de ameaças é identificar pontos fracos na 
postura de segurança de uma organização e melhorar sua postura geral de 
segurança por meio de testes e avaliações proativos.
• Aqui estão as etapas para criar um plano de emulação de ameaças:
1.
Identifique potenciais agentes de ameaças e cenários de ataque
2.
Defina o escopo do teste
3.
Desenvolva o plano de teste
4.
Realize os testes
5.
Avalie os resultados
6.
Desenvolva um plano de correção
7.
Repita o processo
[[ PAGE 18 ]]
Cobalt Strike Emulation - Phishing
Fake US Example
[[ PAGE 19 ]]
Cobalt Strike Emulation - Phishing
Russian Bank APT Group
[[ PAGE 20 ]]
Cobalt Strike Emulation - Execução
[[ PAGE 21 ]]
Cobalt Strike Emulation - Evasion (Mortar 
Loader)
Objetivo:
•
Oculta chamadas de API 
do Windows;
•
Codificação de strings
maliciosas usadas em 
indicadores de 
comprometimento 
(CreateProcess, 
VirtualAlloc e etc);
•
Gerando um Shellcode
encriptado e técnicas de 
injeção de processo;
[[ PAGE 22 ]]
Cobalt Strike Emulation - Evasion (Mortar 
Loader)
•
Exemplo: Gerando um 
Shellcode com 
msfvenom e usando o 
mortar para encriptar o 
shellcode.
[[ PAGE 23 ]]
Cobalt Strike Emulation - Evasion (DONUT)
•
Donut é uma ferramenta de 
geração de shellcode que cria 
cargas úteis de shellcode x86 ou 
x64 a partir de .NET Assemblies. 
Esse shellcode pode ser usado 
para injetar o Assembly em 
processos arbitrários do 
Windows.
•
De qualquer forma, o .NET 
Assembly é criptografado com a 
cifra de bloco Chaskey e uma 
chave de 128 bits gerada 
aleatoriamente. Depois que o 
Assembly é carregado por meio 
do CLR, a referência original é 
apagada da memória para 
impedir os scanners de memória.
[[ PAGE 24 ]]
Cobalt Strike Emulation – Pós Exploração
[[ PAGE 25 ]]
Ferramentas adicionais
https://github.com/CyberSecurityUP/Red-Team-Management/tree/main/Adversary%20Emulation/Tools
[[ PAGE 26 ]]
Cobalt Strike Emulation – Privilege Escalation
[[ PAGE 27 ]]
Cobalt Strike Emulation – Movimentação Lateral
[[ PAGE 28 ]]
Cobalt Strike Emulation – Persistência
[[ PAGE 29 ]]
Cobalt Strike – Exfiltração de Dados
[[ PAGE 30 ]]
OBRIGADO!
https://www.linkedin.com/in/joas-antonio-dos-santos
