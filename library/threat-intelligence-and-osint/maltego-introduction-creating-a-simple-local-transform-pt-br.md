---
id: ckb-00baa6b3df5a
title: Maltego Introduction Creating a Simple Local Transform Pt Br
category: threat-intelligence-and-osint
format: guide
language: pt
tags: [firewall, git, osint, python, tls, web-security]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.75
---

Maltego Introduction –
Creating a simple local Transform

Author
Joas Antonio dos Santos
https://www.linkedin.com/in/joas-antonio-dos-santos/

AUTHOR

1                    E S C R I T O  P O R  J O A S  A  S A N T O S
TABELA DE
CONTEÚDO
01
O QUE É O MALTEGO
05
BIBLIOTECAS E FRAMEWORKS
DO MALTEGO
09
CRIANDO UM SIMPLES
TRANSFORM LOCAL

1                    E S C R I T O  P O R  J O A S  A  S A N T O S
O que é o
maltego
INTRODUÇÃO
Maltego é uma ferramenta avançada de inteligência de código aberto e análise
forense, amplamente usada para coletar e conectar informações durante
investigações cibernéticas. É especialmente popular entre profissionais de segurança
da informação para análise de redes e vulnerabilidades, bem como para a coleta
de informações sobre alvos específicos, como organizações ou indivíduos.
Na minha jornada como profissional de Red Team, o maltego é uma ferramenta que
utilizo frequentemente, não só para OSINT, mas para projetos de Threat Intelligence e
pesquisas que faço no meu tempo livre, apenas como passa tempo. E durante
alguns estudos estava desenvolvendo um Transform para auxiliar em investigações
de tráfico humano e pessoas desaparecidas e resolvi criar esse simples PDF para que
outros entusiastas consigam criar seus próprios Transforms e não depender somente
dos pagos ou que estão no Transform Hub.
Funcionalidades do Maltego:
1. Transforms: As transformações são a principal característica do Maltego,
permitindo que os usuários processem informações de várias fontes de dados
e gerem gráficos interativos. As transformações podem extrair, correlacionar
e visualizar dados a partir de fontes públicas ou privadas.
2. Integração com fontes externas: O Maltego pode integrar-se com uma
ampla variedade de fontes de dados, incluindo registros públicos, bases de
dados WHOIS, redes sociais, APIs de localização geográfica, e mais. Isso
permite que os usuários obtenham uma grande quantidade de informações
sem precisar manualmente visitar cada fonte.
3. Visualização de dados: O Maltego é altamente eficaz na visualização de
complexas redes de informações. Os dados são exibidos em um formato
gráfico que mostra as conexões entre entidades como pessoas, grupos,
domínios da internet, e outros.

2                    E S C R I T O  P O R  J O A S  A  S A N T O S
Servidor Comms
Um servidor Comms no Maltego permite que múltiplos usuários trabalhem
interativamente em um gráfico compartilhado em tempo real. Os usuários podem
interagir através de um mensageiro de chat integrado e também enviar links para
partes selecionadas do gráfico. Os gráficos compartilhados são mantidos privados
com uma chave de sessão que criptografa o tráfego de comunicação usando
criptografia AES de 128/256 bits. As sessões de gráfico compartilhado são
compatíveis entre diferentes plataformas, permitindo que todos os quatro clientes
diferentes se juntem ao mesmo gráfico compartilhado.
O que é CTAS
O CTAS (Commercial Transform Application Server) é um servidor que hospeda todas
as transformações padrão do Maltego e executa essas transformações conforme
solicitado através do cliente de desktop do Maltego. Ele é projetado para empresas
que desejam manter suas solicitações de transformação privadas, hospedando-as
internamente. Isso é útil para investigações sensíveis onde é preferível que os dados
não transitem pela infraestrutura do Maltego. O servidor CTAS é entregue como uma
imagem Docker e requer acesso à Internet para conectar-se a várias fontes online.
O que é TDS e iTDS
O TDS (Transform Distribution Server) público é um servidor localizado na infraestrutura
do Maltego, disponível gratuitamente e usado para escrever transformações
remotas. O iTDS (internal Transform Distribution Server), por outro lado, oferece a
mesma funcionalidade que o TDS público, mas pode ser hospedado internamente
na infraestrutura própria de uma organização. Isso é ideal para lidar com dados
internos sensíveis que não devem passar pela Internet ou pela infraestrutura externa.
Sobre o TDS
Um Servidor de Distribuição de Transformações (TDS) no Maltego permite combinar
transformações, entidades, máquinas e suas configurações em um único item que
pode ser distribuído e instalado por diferentes usuários do Maltego. Isso facilita o
compartilhamento de transformações e configurações personalizadas entre uma
equipe de analistas ou com o mundo, se desejar. No TDS, você pode gerenciar
transformações personalizadas, configurações, entidades e realizar backups. É útil
para quem deseja integrar seus dados no Maltego criando transformações
personalizadas.
Como ele trabalha?
Este diagrama mostra a arquitetura do Maltego e como ele interage com diferentes
fontes de dados e servidores. Os usuários finais utilizam várias versões do Maltego
(Classic, XL, CE) que se conectam ao servidor interno TDS (iTDS) através de uma API.
O iTDS permite que os administradores e desenvolvedores gerenciem transformações
personalizadas e configurações. Estas transformações podem consultar fontes de
dados públicas (como DNS, redes sociais, motores de busca) ou dados internos da
organização (APIs internas, logs de sistema, servidores internos). As configurações e

3                    E S C R I T O  P O R  J O A S  A  S A N T O S
transformações são gerenciadas através de uma interface de servidor, que também
pode ser usada para fazer backups.
Arquitetura do Maltego Server

Figura 1 – Arquitetura do servidor (docs.maltego.com)
A arquitetura do servidor Maltego ilustrada na imagem detalha como diferentes
componentes interagem dentro de um ambiente de rede protegido por firewall.
Inclui:
•
Zonas de Rede: Diferentes zonas como a zona de rede do cliente
Maltego, zona de rede do servidor Maltego, e zonas de rede de
aplicação e dados internos.
•
iTDS e CTAS: iTDS serve como servidor de distribuição de transformações
internas, e o CTAS (Commercial Transform Application Server) hospeda as
transformações padrão do Maltego. Ambos operam sob HTTPS para
segurança.
•
TRX e APIs Públicas: O TRX gerencia APIs internas e públicas para
integração de dados, acessíveis também por outros serviços de
colaboração e verificação de licença.
•
Proxies e Firewalls: Existem mecanismos de segurança como firewalls e
proxies internos de internet que regulam o tráfego de dados.
•
Servidores Públicos do Maltego: Incluem servidores para ativação de
licenças, colaboração pública e distribuição de transformações, todos

4                    E S C R I T O  P O R  J O A S  A  S A N T O S
comunicando-se sobre HTTPS, exceto o servidor de colaboração que usa
TCP/5222.
Esta arquitetura permite uma comunicação segura e eficiente entre os usuários
do Maltego e os recursos de dados, tanto internos quanto externos.

5                    E S C R I T O  P O R  J O A S  A  S A N T O S
Bibliotecas e
frameworks do
maltego
INTRODUÇÃO
Os que desenvolvem os transform para Maltego são responsáveis por criar a lógica
que traduz solicitações de transformação em dados acessíveis. Estes dados podem
vir de diversas fontes, como bancos de dados ou APIs. A aplicação de desktop do
Maltego simplifica a gestão de grafos interligados, permitindo que os
desenvolvedores se concentrem em extrair e consultar dados. Para facilitar esse
processo, existe bibliotecas que ajuda a hospedar um servidor HTTP, traduzir
solicitações XML e gerenciar respostas, tornando a interação com os objetos mais
eficiente.
Bibliotecas e Frameworks
Bibliotecas e frameworks disponíveis para o desenvolvimento de transformações no
Maltego, utilizando diferentes linguagens de programação:
•
Canari3 (Python): Um framework para o desenvolvimento rápido de
transformações locais e remotas no Maltego, permitindo prototipagem,
empacotamento e distribuição eficientes. Suporta tanto transformações
locais quanto no iTDS.
•
MaltegoGo (Go): Esta biblioteca é uma tradução da biblioteca TDS do
Maltego para Go, permitindo a criação de transformações extremamente
rápidas para iTDS, mas não suporta transformações locais.
•
TransNet (.NET): Uma biblioteca .Net Standard que facilita a criação de
transformações no Maltego, compatível apenas com iTDS, não suporta
transformações locais.
•
MaltegoLocal (GoLang): Wrapper local para desenvolvimento de
transformações no Maltego, permitindo implementações rápidas em
ambiente local, mas não é compatível com iTDS.

6                    E S C R I T O  P O R  J O A S  A  S A N T O S
•
JavaMaltego (Java): Biblioteca desenvolvida em Java para criar
transformações locais no Maltego, focada em desenvolvimentos que não
necessitam de integração com iTDS.
•
Maltego-TRX: A biblioteca Maltego TRX é uma ferramenta Python destinada
ao desenvolvimento de transformações no Maltego. Ela facilita a criação de
servidores de transformações que podem interagir com dados de fontes
externas como bancos de dados SQL ou APIs REST. Com a Maltego TRX,
desenvolvedores podem gerar rapidamente transformações e hospedá-las
em um servidor que comunica via HTTP/XML. A biblioteca também permite
criar e gerenciar projetos de transformações de maneira organizada,
incluindo um servidor de desenvolvimento que recarrega automaticamente
ao modificar o código.
Como criar um servidor de transform?
Para criar um servidor de transformação no Maltego, o servidor deve estar em uma
rede que possa acessar os dados necessários, como um servidor SQL ou APIs REST.
Qualquer servidor ou máquina virtual que exponha a porta 8080 (ou 80) e permita
tráfego HTTP (XML) pode funcionar como um servidor de transformação. O Maltego
TRX, uma biblioteca Python, requer Python 3 e pode ser instalada via PIP. Após a
instalação, você pode criar um novo projeto e adicionar transformações à pasta
correspondente. Para iniciar o servidor em modo de desenvolvimento.
Comandos para criação do servidor:
$ pip install maltego-trx
Faz a instalação da biblioteca maltego-trx no python
$ maltego-trx start <project name>
 Configure um novo projeto para o maltego e os transforms vão estar na
pasta com o respectivo nome
$ python Project.py runserver
O comando acima inicia o modo desenvolvedor.
Estrutura de código de um Transform
Ao criar um Transform para o Maltego em Python, a estrutura do código não
é tão complexa.
1. Importação de Bibliotecas
Primeiramente, importe todas as bibliotecas necessárias. Normalmente,
incluirá o framework maltego_trx para integração com o Maltego, e
qualquer outra biblioteca necessária para a funcionalidade do Transform,

7                    E S C R I T O  P O R  J O A S  A  S A N T O S
como requests para chamadas de API ou beautifulsoup4 para parsing de
HTML.
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
2. Definição da Classe do Transform
Defina uma classe que herde de DiscoverableTransform ou Transform. Esta
classe será o núcleo do seu Transform, contendo toda a lógica necessária
para executar a tarefa pretendida
class ExampleTransform(DiscoverableTransform):
3. Método para Criar Entidades
Implemente um método chamado create_entities que é chamado pelo
framework do Maltego. Este método receberá a mensagem de entrada do
Maltego (MaltegoMsg) e a resposta do transform (MaltegoTransform), que
você usará para adicionar entidades ao gráfico do Maltego.
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response:
MaltegoTransform):
        # Lógica para processar a entrada e adicionar entidades à resposta.
4. Lógica Específica do Transform
Dentro do método create_entities, implemente a lógica específica do seu
Transform. Isso pode incluir chamar APIs externas, processar dados, e criar e
configurar entidades Maltego para serem retornadas ao usuário.
        input_value = request.Value  # Obter o valor de entrada
        data = requests.get(f"https://api.example.com/data/{input_value}")  #
Chamada de API
        if data.status_code == 200:
            json_data = data.json()
            entity = response.addEntity('maltego.ExampleEntity',
json_data['name'])
            entity.addProperty('detail', 'Detail', 'strict', json_data['detail'])

8                    E S C R I T O  P O R  J O A S  A  S A N T O S
        else:
            response.addUIMessage("No data found or API error",
messageType='PartialError')
5. Execução Condicional
Adicione um bloco if __name__ == "__main__" no final do arquivo para tornar
o script diretamente executável. Isso é útil para testar o Transform
localmente.
if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([ExampleTransform])
6. Configuração do Transform
Depois do código Python, você também precisará configurar o Transform no
Maltego, incluindo especificar o comando, os parâmetros e o caminho do
script. Isso é geralmente feito através do interface do Maltego ou de um
arquivo de configuração JSON.
Esta estrutura básica oferece um esqueleto para desenvolver Transforms

9                    E S C R I T O  P O R  J O A S  A  S A N T O S
CRIANDO UM SIMPLES
TRANSFORM LOCAL
INTRODUÇÃO
Agora vamos criar nosso transform local, não esqueça de ter o maltego
instalado e configurado na sua máquina, além do python3 também e a
biblioteca maltego-trx instalado
Criando um simples Transform para buscar na Rede Tor
Para criar esse transform vou utilizar a linguagem python e o website ahmia
para realizarmos o scraping e fazer as pesquisas através de Entity, nesse caso
o melhor sendo “phrase” dentro do maltego.
O que são Entities
No Maltego, "entities" são os objetos visuais utilizados para representar dados
dentro do ambiente gráfico da ferramenta. Cada entidade pode
representar diferentes tipos de informações, como pessoas, organizações,
endereços de IP, domínios de internet, entre outros. Essas entidades são
conectadas por linhas ou "links" que representam relações ou fluxos de
dados entre elas. As entidades podem ser enriquecidas com dados
adicionais por meio de transformações, que são scripts ou consultas que
extraem informações de bases de dados ou da internet. Essas entidades são
centrais para visualizar e analisar redes complexas de informações dentro do
Maltego.
Colocando em prática:
$ maltego-trx start ahmia2
Vamos criar o projeto com nome Ahmia ou o que preferir.
Agora vamos fazer a importação das bibliotecas para preparar o ambiente
from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests

10                    E S C R I T O  P O R  J O A S  A  S A N T O S
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote
Algumas bibliotecas podem não estar disponíveis, basta fazer a instalação
via PIP
$ pip install requests bs4 maltego-trx
Assim você instala as bibliotecas necessárias para que o nosso código
funcione, detalhando mais sobre as bibliotecas
•
MaltegoMsg e MaltegoTransform: Classes do maltego_trx que são
usadas para manipular a mensagem de entrada do Maltego e
construir a resposta para ser enviada de volta ao Maltego,
respectivamente.
•
DiscoverableTransform: Classe base que facilita a criação de
Transforms que podem ser descobertos e gerenciados pelo framework
maltego_trx.
•
requests: Biblioteca para fazer requisições HTTP de maneira simples e
legível em Python.
•
BeautifulSoup: Biblioteca para fazer parsing de documentos HTML e
XML, usada para extrair informações de páginas web.
•
urlparse, parse_qs, unquote: Funções do módulo urllib.parse que são
usadas para analisar e manipular URLs.
class AhmiaDomainExtractor(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response:
MaltegoTransform):
        search_term = request.getProperty('text')
        html_content = cls.search_ahmia(search_term)
        unique_domains = cls.parse_results(html_content)

        if unique_domains:
            for domain in unique_domains:
                entity = response.addEntity('maltego.Domain', domain)

11                    E S C R I T O  P O R  J O A S  A  S A N T O S
        else:
            entity = response.addEntity('maltego.Phrase', 'No domains found')
            entity.addProperty(fieldName="description",
displayName="Description", value="Search returned no results")
•
Método create_entities: Este método é chamado automaticamente
pelo framework maltego_trx quando o Transform é executado. Ele
processa a mensagem de entrada, realiza a pesquisa no Ahmia e
extrai os domínios, adicionando-os ao gráfico do Maltego ou
indicando que não foram encontrados resultados.
•
Decorador @classmethod: Este decorador indica que o método é um
método de classe, o que significa que ele opera em relação à classe
e não a uma instância específica dela. Isso é útil para operações que
não requerem um objeto da classe para serem executadas.
•
request é um objeto MaltegoMsg que contém todos os dados da
mensagem enviada pelo cliente Maltego. Ele permite acessar
propriedades e valores que foram passados pela interface do
Maltego.
•
response é um objeto MaltegoTransform que é usado para construir a
resposta do Transform. Aqui você adiciona entidades ao gráfico do
Maltego, configura mensagens de erro ou informação, entre outros.
•
cls.search_ahmia(search_term): Chama o método estático
search_ahmia que realiza uma requisição HTTP ao site Ahmia usando
o termo de pesquisa. Retorna o conteúdo HTML da página de
resultados.
•
cls.parse_results(html_content): Analisa o conteúdo HTML retornado
para extrair os domínios das URLs encontradas, usando a função
parse_results.

@staticmethod
def search_ahmia(search_term):
    base_url = "https://ahmia.fi"
    search_url = f"{base_url}/search/?q={search_term}"
    try:
        response = requests.get(search_url)

12                    E S C R I T O  P O R  J O A S  A  S A N T O S
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None
•
Método search_ahmia: Realiza uma requisição GET para o Ahmia
usando o termo de pesquisa fornecido. Se a requisição for bem-
sucedida, retorna o conteúdo HTML da página de resultados. Caso
contrário, captura e imprime exceções relacionadas à requisição
HTTP.
@staticmethod
def parse_results(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    domains = set()
    for result in soup.select('h4 > a'):
        if result.get('href'):
            parsed_href = urlparse(result['href'])
            redirect_params = parse_qs(parsed_href.query)
            redirect_url = redirect_params.get('redirect_url', [None])[0]
            if redirect_url:
                domain = urlparse(unquote(redirect_url)).netloc
                domains.add(domain)
    return domains
•
Método parse_results: Analisa o HTML retornado pelo Ahmia para
extrair URLs de redirecionamento e, subsequentemente, os domínios
das URLs redirecionadas. Usa a biblioteca BeautifulSoup para fazer
parsing do HTML e extrair elementos específicos (h4 > a). Os domínios
são adicionados a um conjunto para evitar duplicatas, e este
conjunto é retornado.

13                    E S C R I T O  P O R  J O A S  A  S A N T O S
Essas explicações descrevem a lógica por trás do código, mostrando como
o Transform interage com o site Ahmia, processa os dados e manipula
resultados dentro do ambiente do Maltego.
Link do código fonte completo:
https://github.com/CyberSecurityUP/AhmiaDomainExtractor-Maltegoce/
Configurando e Instalando o Transform Local no Maltego
Figura 2 – Criando o projeto
Criei o projeto Ahmia com maltego-trx, se tudo der certo ele vai criar o
projeto com sucesso, verifique se você tem as permissões necessárias
Figura 3 – Crie o script do transform e insira na pasta transforms
Acesse a pasta transforms e insira o script, nesse caso ele precisa ter o
mesmo nome da Classe criada para o Transform, no meu caso foi

14                    E S C R I T O  P O R  J O A S  A  S A N T O S
AhmiaDomainExtractor. Após isso execute o script Project.py para ver se foi
detectado o script do Transform.
$ python3 project.py list
O comando acima, verifica a lista dos projetos
Figura 4 – Configurando um novo transform
Ao acessar maltego clique na opção New Local Transform
Figura 5 – Configuração do Transform Local

15                    E S C R I T O  P O R  J O A S  A  S A N T O S
Na criação e gerenciamento de Transforms no Maltego, vários parâmetros e
configurações são importantes para definir como o Transform opera e como
ele é apresentado no Maltego. Aqui está um resumo de cada um dos termos
que você mencionou:
DisplayName
•
DisplayName é o nome do Transform que é exibido no Maltego. Ele é
usado para identificar o Transform na interface do usuário, facilitando
aos usuários entenderem rapidamente o que o Transform faz. Por
exemplo, um DisplayName poderia ser "Buscar Domínios no Ahmia".
Description
•
Description fornece uma descrição detalhada do que o Transform faz.
Esta descrição ajuda o usuário a entender melhor o propósito do
Transform, o que ele busca, que tipo de dados ele retorna, e
quaisquer outras informações relevantes que possam ajudar na sua
utilização.
Transform ID
•
Transform ID é um identificador único para o Transform dentro do
Maltego. Ele é usado para referenciar o Transform de forma
programática e deve ser único em toda a configuração do Maltego.
É crucial para a integração e o gerenciamento dos Transforms,
especialmente quando são distribuídos através de servidores de
transformação ou configurados em ambientes compartilhados.
Author
•
Author refere-se ao criador ou à organização responsável pelo
desenvolvimento do Transform. Este campo é útil para rastreamento,
suporte e crédito das funcionalidades dentro do Maltego.
Input Entity Type
•
Input Entity Type especifica o tipo de entidade que o Transform espera
como entrada. Cada Transform no Maltego é projetado para
trabalhar com certos tipos de entidades (como domínios, endereços
de IP, e-mails, etc.). Este parâmetro define com quais entidades esse
Transform específico pode interagir. Por exemplo, um Transform
projetado para extrair informações de um domínio esperaria uma
entidade do tipo "Domain".
Transform Set
•
Transform Set é uma coleção de Transforms agrupados juntos no
Maltego. Transform Sets são usados para organizar Transforms
relacionados em grupos lógicos, facilitando aos usuários encontrar e

16                    E S C R I T O  P O R  J O A S  A  S A N T O S
utilizar Transforms que se relacionam com tarefas específicas. Por
exemplo, você pode ter um Transform Set chamado "Análise de
Domínios", que inclui vários Transforms relacionados à coleta e análise
de dados de domínios
Figura 6 – Configurando o Command Line
Vamos inserir no Command o interpretador do Python, nesse caso estou no
Linux e por isso coloco o caminho do interpretador /usr/bin/python
Como parâmetros eu defino o script Project.py local “Nome do Transform”
para ele iniciar o transform local ao ser executado.
E por fim o diretório do projeto aonde se localiza o Transform.

17                    E S C R I T O  P O R  J O A S  A  S A N T O S

Figura 7 – Inserindo uma Phrase
Após configurar nosso Transform, insira uma frase e coloque um termo
que deseja pesquisar, nesse caso utilizaremos lockbit.
Figura 8 – Executando Transform

18                    E S C R I T O  P O R  J O A S  A  S A N T O S
Ao executar o AhmiaDomainExtractor, esse é o resultado, ele traz
todos os dominios .onion relacionados ao termo lockbit.
Sendo assim, é um Transform que se torna um complemento para
outros Transforms que são utilizados para investigações em Dark Web
Conclusão
A ferramenta Maltego é uma das mais completas para realização de
OSINT, Intelligence e outros tipos de investigação. Esse script é apenas
um exemplo de um projeto que estou criando para contribuir mais
ainda com iniciativas relacionadas a investigação de Trafico Humano.
Caso você queira se aprofundar mais ainda sobre desenvolvimento
de Transforms e conhecer outros projetos, deixarei alguns links abaixos
para sua pesquisa.
https://www.youtube.com/watch?v=k5oikWy0OLc – Create your Local
Transform by OSINT Dojo
https://github.com/cipher387/maltego-transforms-list - Maltego
Transform List by Cipher387
https://github.com/megadose/holehe-maltego - Holehe Maltego by
megadose
https://github.com/TURROKS/Maltego_WhatsMyName -
WhatsMyName by TURROKS
https://www.youtube.com/watch?v=VRN741CgsOk&pp=ygUebG9jYW
wgdHJhbnNmb3JtIG1hbHRlZ28gY3JlYXRl – Create your own local
Transform in Python by Cylon Null
https://www.youtube.com/watch?v=42KhnNQS8AU - Official Maltego
Tutorial – Writing your own Transforms
Referências Bibliográficas
BUILDING INTEGRATIONS FOR MALTEGO. (n.d.). Retrieved May 12, 2024, from
https://static.maltego.com/cdn/Case%20studies/Building-Integrations-for-
Maltego-Complete-Guide.pdf
Writing Transforms. (n.d.). Maltego Support. Retrieved May 12, 2024, from
https://docs.maltego.com/support/solutions/articles/15000015758-writing-
transforms
ChatGPT 4 para tradução e correção de textos
