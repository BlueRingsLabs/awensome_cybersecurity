---
id: ckb-c626cdefaa77
title: Comprehensive Guide on Tshark
category: network-and-wireless-security
format: guide
language: en
tags: [networking, python, reporting, tls, web-security, wireless]
authors: [unknown]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.66
---

Page | 1

www.hackingarticles.in

Page | 2

www.hackingarticles.in
Table of Contents

Abstract ........................................................... 4
Network Traffic .................................................... 5
Introduction to TShark ............................................. 5
List Interfaces .................................................... 7
Capture Traffic .................................................... 7
Promiscuous mode ................................................... 8
Packet Count ....................................................... 9
Read and Write a File ............................................. 10
Verbose Mode ...................................................... 11
Output Formats .................................................... 12
PDML ............................................................ 12
PS .............................................................. 13
PSML ............................................................ 13
JSON ............................................................ 14
EK .............................................................. 15
Text ............................................................ 15
Tabs ............................................................ 16
Difference between decoded and encoded packets .................... 16
Converting PDML file to HTML Page ................................. 17
Capturing Packets of a Particular Port ............................ 18
Display Filter .................................................... 18
Statistical Options ............................................... 19
Protocol Hierarchy Statistics ..................................... 20
Read Filter Analysis .............................................. 21
Endpoint Analysis ................................................. 22
Conversation Analysis ............................................. 23
Expert Mode Analysis .............................................. 23
Packet Distribution Tree .......................................... 24
Packet Length Tree ................................................ 25
Colour Based Output Analysis ...................................... 25
Ring Buffer Analysis .............................................. 26

Page | 3

www.hackingarticles.in
Autostop .......................................................... 27
Duration ........................................................ 27
File size ....................................................... 27
Data-link Types ................................................... 28
Version Information ............................................... 28
Reporting Options ................................................. 29
Column Formats .................................................. 29
Decodes ......................................................... 30
Dissector Tables ................................................ 31
Elastic Mapping ................................................. 32
Field Count ..................................................... 32
Fields .......................................................... 33
Fundamental Types ............................................... 33
Heuristic Decodes ............................................... 34
Plugins ......................................................... 35
Protocols ....................................................... 36
Values .......................................................... 36
Preferences ..................................................... 37
Folders ......................................................... 37
PyShark ........................................................... 38
Installation .................................................... 38
Live Capture .................................................... 39
Pretty Representation ........................................... 39
Captured Length Field ........................................... 41
Layers, Src and Dst Fields ...................................... 41
Promisc Capture ................................................... 42
References ........................................................ 43
About Us .......................................................... 44

Page | 4

www.hackingarticles.in
Abstract

In this article, we will learn about TShark which is a well-known network
protocol analyser. It lets us capture the data packets, from the live network. It also
allows us, to read or analyse the previously captured data packets of a saved file.

Here we will the understand the Statistical Functionalities of TShark and the
different ways in which we can sort our traffic capture so that we can analyse it
faster and effectively.

We will understand the reporting functionalities and some additional tricks that
we found while tinkering with TShark.

Page | 5

www.hackingarticles.in
Network Traffic

As we know, network traffic or data traffic is the amount of data transferring across the network
at some given point of time. Network data, in computer networks, is in the form of network
data packets. Analysing these network packets provides network security as it helps us to
monitor traffic. As a benefit, if there is some unusual amount of data traffic in a network which
is a possible sign of an attack then TShark can help us know before it too late and the attack
can be terminated as data traffic reports provide insights into preventing some good attacks.

Traffic volume is a term which comes under network traffic analysing. Network traffic volume
is the measure of the total work done. It is defined as the average data traffic intensity and time
period of its network data packet study.

Introduction to TShark

TShark, a well-known and powerful command-line tool and is used as a network analyser. It is
developed by Wireshark. It’s working structure is quite similar to Tcpdump, but it has some
powerful decoders and filters. TShark is capable of capturing the data packets information of
different network layers and display them in different formats.

TShark is a command-line based tool, which can do anything that Wireshark does. So, let us
start our learning process with TShark and therefore launch this tool and explore its options.
To check out all the parameters, use the following command:

TShark is used to analyse real-time network traffic and it can read
.pcap files to analyse the information, dig into the details of those
connections, helping security professionals to identify their network
problem.

Page | 6

www.hackingarticles.in

tshark -h

Page | 7

www.hackingarticles.in
List Interfaces

TShark prints a list of the interfaces whose traffic it can capture. Each interface is referred to
by their serial number and as you can see it is followed by a text description of the network
interface. These interfaces can be specified using -i parameter; which is used to specify the
network whose traffic we want to capture. And to check out these interfaces you can use
the parameter -D as shown in the image below:

Capture Traffic

Let’s now try to capture traffic, we have various choice of interface to capture traffic and
therefore one can choose whichever depending on their needs and requirement. But in our
scenario, the interface which we are going to use is “eth0”. In order to capture traffic, we need
to initiate one too as we are testing on a controlled network and for that use ping command and
then to capture traffic, we have to just specify the interface name by using -i parameter as
shown in the image below:

As we can clearly see it is performing its three-way handshake, then starts the process of
ICMP request and reply.

tshark -D
ping www.hackingarticles.in
tshark -i eth0

Page | 8

www.hackingarticles.in

Promiscuous mode

In the networking, promiscuous mode is used as an interface controller that causes tshark to
pass all the traffic it receives to the CPU rather than passing the frames to the promiscuous
mode is normally used for packet sniffing that can take place on a router or on a computer
connected to a wired network or a part of LAN.

When using this mode, we will need to configure it with the help of ifconfig so that it let us
capture the data packets of the whole network. Therefore, we will start by pinging a website
and try to capture its data packets.

Page | 9

www.hackingarticles.in

Now, configure the promiscuous mode by following these commands and try to capture the
packets.

Packet Count

Tshark has amazing features with which we can work more efficiently and we can access these
features using various parameters. One such parameter is ‘-c’, it lets us capture the exact
amount of data that we require and it will display only those. This option helps us to refine the
outcome of captured traffic.

ifconfig eth0 promisc
tshark -i eth0

Page | 10

www.hackingarticles.in

As we can clearly see in the image above that it stops after the 10 counts.
Read and Write a File

In Tshark we can write and read into .pcap file. Write option (-w) allows us to write raw packet
data output to a standard .pcap file whereas read option (-r) help us to read that raw output data
packets in our desired manner. To write the packets into a .pcap file use the following
command:

And to read the said .pcap file use the following command:

tshark -i eth0 -c 10
tshark -i eth0 -c 10 -w packets.pcap
tshark -r packets.pcap

Page | 11

www.hackingarticles.in
Verbose Mode
The verbose mode provides us with additional details of a packet in traffic. Using the verbose
mode, we can see the information that each packet contains and for this option we can use
the parameter -V.

tshark -r packets.pcap -V

Page | 12

www.hackingarticles.in
Output Formats

For our convenience, in tshark, we have -T option that lets us save decoded packets in various
output formats. It can set the format of the output in the way that it becomes easy to understand.
To see all the available options, type the following command:

PDML

PDML stands for Packet Details Mark-Up Language which is an XML based. This
information is quite equivalent to the verbose mode which we used earlier. And to have output
in this format type the following command:

\
tshark -T x
tshark -r packets.pcap -T pdml

Page | 13

www.hackingarticles.in

PS

PS stands for PostScript. This output is in a form of one-liner summary of each data packets
or multi-line detail view of each data packets depending upon each data packet specification.
These one-liners are very quick to understand as well as reliable. For this, use the following
command:

PSML

PSML stands for Packet Summary Mark-Up Language. It is also an XML based format like
PDML which summarises the detailed information of the packets. And for this format type:

tshark -r packets.pcap -T ps
tshark -r packets.pcap -T psml

Page | 14

www.hackingarticles.in

JSON

JSON stands for Java-Script Object Notation. It is an open standard file format that displays
text in a readable form. The information in this format is fully documented and referred at
wolfram. To see that packets in this format, type:

tshark -r packets.pcap -T json

Page | 15

www.hackingarticles.in
EK

It is newline delimited JSON format function for bulk import into the elastic search option. And for
this format use the following command:

Text

Text is a human-readable one lines summary of each of the packets. This is the simplest of the
formats. And for this, use the following command:

tshark -r packets.pcap -T ek
tshark -r packets.pcap -T text

Page | 16

www.hackingarticles.in
Tabs
This option is quite similar to the text except, it includes an ASCII horizontal tab (oxo9) character as
the delimiter between each column. To try this, type:

Difference between decoded and
encoded packets

When we try to write the live data packets in a .pcap format file; we compress all that data
packets in smaller segments. To better understand these data packets, we need to decode them
which leads to a difference in the size of the file and to check the size of any given file at the
given moment use the following command:

Like we discussed there is a huge difference in these files, that’s why we use decoding
techniques to extract this information.

tshark -r packets.pcap -T tabs
ls -lh packets.p*

Page | 17

www.hackingarticles.in
Converting PDML file to HTML Page

The only difference between the Wireshark and tshark is that Wireshark is a GUI based tool
and tshark is a command-line based tool. But with the help of some external source, we can
also view our data packets in HTML. So, to achieve that first, we need to save our data packets
in PDML format and then convert it into an XML file using the following command:

The XML file will be saved at location /usr/share/wireshark/pdml2html.xsl. So, we are
going to use xsltproc tool to execute this file it which will help us to create our HTML page.
Creating the HTML page will format all the unnecessary information and only let us view the
usable data. To create the HTML use following command.
To open the HTML page in the browser, refer to the image and use the following command:

tshark -r packets.pcap -T pdml > packets.xml
xsltproc /usr/share/wireshark/pdml2html.xsl packets.xml
> packets.html
firefox packets.html &

Page | 18

www.hackingarticles.in
Capturing Packets of a Particular Port

A lot of times we use Wireshark on a dedicated port. And by using the -f option we can capture
data packets of a particular port. It helps us to better analyze the data packets of the network.
We are using this feature to capture TCP port 80 and the command for this is:

Display Filter

Display filter was introduced by Wireshark. It helps us to filter the captured data packets or
live data packets. With the help of this filter, we can request for any kind of filter that we want
to capture in the live environment.
In our scenario, we apply the GET request filter to capture only GET request from the traffic
and for, use the following command:

tshark -i eth0 -c 5 -f "tcp port 80"
tshark -i eth0 -c 5 -f "tcp port 80" -Y
'http.request.method == "GET" '

Page | 19

www.hackingarticles.in
Statistical Options

TShark collects different types of Statistics and displays their result after finishing the reading
of the captured file. To accomplish this, we will be using the “-z” parameter with TShark.
Initially, to learn about all the different options inside the “-z” parameter, we will be running
the TShark with the “-z” parameter followed by the help keyword. This gives us an exhaustive
list of various supported formats as shown in the image given below.

Page | 20

www.hackingarticles.in
Protocol Hierarchy Statistics

Using the TShark we can create a Protocol based Hierarchy Statistics listing the number of
packets and bytes using the “io,phs” option in the “-z” parameter. In the case where no filter is
given after the “io,phs” option, the statistics will be calculated for all the packets in the scope.
But if a specific filter is provided than the TShark will calculate statistics for those packets that
match the filter provided by the user. For our demonstration, we first captured some traffic and
wrote the contents on a pcap file using the techniques that we learned in part 1 of this article
series. Then we will be taking the traffic from the file, and then sort the data into a Protocol
Hierarchy.  Here we can observe that we have the frames count, size of packets in bytes and
the Protocol used for the transmission.

tshark  -r wlan.pcap -z io,phs

Page | 21

www.hackingarticles.in
Read Filter Analysis

During the first pass analysis of the packet, the specified filter (which uses the syntax of
read/display filters, rather than that of capture filters) has to be applied. Packets which are
not matching the filter are not considered for future passes. This parameter makes sense with
multiple passes. Note that forward-looking fields such as ‘response in frame #’ cannot be used
with this filter since they will not have been calculated when this filter is applied. The “-2”
parameter performs a two-pass analysis. This causes TShark to buffer output until the entire
first pass is done, but allows it to fill in fields that require future knowledge, it also permits
reassembly frame dependencies to be calculated correctly. Here we can see two different
analysis one of them is first-pass analysis and the latter is the two-pass analysis.

tshark -r wlan.pcap -z io,phs,udp -q
tshark -r wlan.pcap -z io,phs -q -2 -R udp

Page | 22

www.hackingarticles.in
Endpoint Analysis

Our next option which helps us with the statistics is the “endpoints”. It will create a table that
will list all endpoints that could be seen in the capture. The type function which can be used
with the endpoint option will specify the endpoint type for which we want to generate the
statistics.

The list of Endpoints that are supported by TShark is:
Sr.no.
Filter
Description
1
“bluetooth”
Bluetooth Addresses
2
“eth”
Ethernet Addresses
3
“fc”
Fiber Channel Addresses
4
“fddi”
FDDI Addresses
5
“ip”
IPv4 Addresses
6
“ipv6”
IPv6 Addresses
7
“ipx”
IPX Addresses
8
“jxta”
JXTS Addresses
9
“ncp”
NCP Addresses
10
“rsvp”
RSVP Addresses
11
“sctp”
SCTP Addresses
12
“tcp”
TCP/IP socket pairs Both IPv4 and IPv6
supported
13
“tr”
Token Ring Addresses
14
“usb”
USB Addresses
15
“udp”
UDP/IP socket pairs Both IPv4 and IPv6
supported
16
“wlan”
IEEE 802.11 addresses

In case that we have specified the filter option then the statistics calculations are done for
that particular specified filter. The table like the one generated in the image shown below is
generated by picking up single line form each conversation and displayed against the number
of packets per byte in each direction as well as the total number of packets per byte. This
table is by default sorted according to the total number of frames.

tshark -r wlan.pcap -z endpoints,wlan -q | head

Page | 23

www.hackingarticles.in

Conversation Analysis

Let’s move on to the next option which is quite similar to the previous option. It helps us with
the statistics is the “conversation”. It will create a table that will list all conversation that could
be seen in the capture. The type function which can be used with the conversation option will
specify the conversation type for which we want to generate the statistics.
If we have specified the filter option then the statistics calculations are done for that particular
specified filter. The table generated by picking up single line form each conversation and
displayed against the number of packets per byte in each direction, the total number of packets
per byte as well as the direction of the conversation travel. This table is by default sorted
according to the total number of frames.

Expert Mode Analysis

The TShark Statistics Module have an Expert Mode. It collects a huge amount of data based
on Expert Info and then prints this information in a specific order. All this data is grouped in
the sets of severity like Errors, Warnings, etc., We can use the expert mode with a particular
protocol as well. In that case, it will display all the expert items of that particular protocol.

tshark -r wlan.pcap -z conv,wlan -q | head
tshark -r wlan.pcap -z expert -q | head

Page | 24

www.hackingarticles.in

Packet Distribution Tree

In this option, we take the traffic form a packet and then drive it through the “http,tree”
option under the “-z” parameter to count the number of the HTTP requests, their mods as
well as the status code. This is a rather modular approach that is very easy to understand and
analyse. Here in our case, we took the packet that we captured earlier and then drove it
through the tree option that gave us the Information that a total of 126 requests were
generated out of which 14 gave back the “200 OK”. It means that the rest of them either gave
back an error or were redirected to another server giving back a 3XX series status code.

tshark -r wlan.pcap -z http,tree -q

Page | 25

www.hackingarticles.in
Packet Length Tree

As long as we are talking about the Tree option, let’s explore it a bit. We have a large variety
of ways in which we can use the tree option in combination with other option. To demonstrate
that, we decided to use the packet length option with the tree option. This will sort the data on
the basis of the size of the packets and then generate a table with it. Now, this table will not
only consist of the length of the packets, but it will also have the count of the packet. The
minimum value of the length in the range of the size of the packets. It will also calculate the
size as well as the Percentage of the packets inside the range of packet length

Colour Based Output Analysis

We can enable the coloring of packets according to standard Wireshark color filters. On
Windows, colors are limited to the standard console character attribute colors. In this option,
we can set up the colors according to the display filter. This helps in quickly locating a specific
packet in the bunch of similar packets. It also helps in locating Handshakes in communication
traffic. This can be enabled using the following command.

tshark -r wlan.pcap -z plen,tree -q
tshark -r color.pcap --color
Note: Your terminal must support color output in order for this option
to work correctly.

Page | 26

www.hackingarticles.in

Ring Buffer Analysis

By default, the TShark to runs in the “multiple files” mode. In this mode, the TShark writes
into several capture files. When the first capture file fills up to a certain capacity, the TShark
switches to the next file and so on. The file names that we want to create can be stated using
the -w parameter. The number of files, creation data and creation time will be concatenated
with the name provided next to -w parameter to form the complete name of the file.
The files option will fill up new files until the number of files is specified. at that moment the
TShark will discard data in the first file and start writing to that file and so on. If the files option
is not set, new files filled up until one of the captures stops conditions matches or until the disk
is full.
There are a lot of criteria upon which the ring buffer works but, in our demonstration, we used
2 of them. Files and the Filesize.
files: value begin again with the first file after value number of files were written (form a ring
buffer). This value must be less than 100000.
filesize: value switches to the next file after it reaches a size of value kB. Note that the file size
is limited to a maximum value of 2 GiB.

Page | 27

www.hackingarticles.in

Autostop

Under the huge array of the options, we have one option called auto-stop. As the name tells
us that it will stop the traffic capture after the criteria are matched.
Duration

We have a couple of options, in our demonstration, we used the duration criteria. We specified
the duration to 10. This value is in seconds. So, the capture tells us that in the time of 10
seconds, we captured 9 packets.

File size

Now another criterion for the auto-stop option is the file size. The TShark will stop writing to
the specified capture file after it reaches a size provided by the user. In our demonstration, we
tshark -I eth0 -w packetsbuffer.pcap -b filesize:1 –
file:3
tshark -i eth0 -a duration:10

Page | 28

www.hackingarticles.in
set the filesize to 1. This value is in kB. We used the directory listing command to show that
the capture was terminated as soon as the file reached the size of 1 kB.

Data-link Types

At last, we can also modify the statistics of the captured traffic data based on the Data-Link Types.
For that we will have to use an independent parameter, “-L”. In our demonstration, we used the “-L”
parameter to show that we have data links like EN10MB specified for the Ethernet Traffic and
others.

Version Information

Let’s begin with the very simple command so that we can understand and correlate that all the
practicals performed during this article and the previous articles are of the version depicted in
the image given below. This parameter prints the Version information of the installed TShark.

tshark -i eth0 -w 1.pcap -a filesize:1
tshark -L
tshark -v

Page | 29

www.hackingarticles.in

Reporting Options

During any Network capture or investigation, there is a dire need of the reports so that we
can share the findings with the team as well as superiors and have a validated proof of any
activity inside the network. For the same reasons, TShark has given us a beautiful option (-G).
This option will make the TShark print a list of several types of reports that can be generated.
Official Manual of TShark used the word Glossaries for describing the types of reports.

Column Formats

From our previous practicals, we saw that we have the Column Formats option available in the
reporting section of TShark. To explore its contents, we ran the command as shown in the
image given below. We see that it prints a list of wildcards that could be used while generating
tshark -G help

Page | 30

www.hackingarticles.in
a report. We have the VLAN id, Date, Time, Destination Address, Destination Port, Packet
Length, Protocol, etc.

Decodes

This option generates 3 Fields related to Layers as well as the protocol decoded. There is a
restriction enforced for one record per line with this option. The first field that has the
“s1ap.proc.sout” tells us the layer type of the network packets. Followed by that we have the
tshark -G column-formats

Page | 31

www.hackingarticles.in
value of selector in decimal format. At last, we have the decoding that was performed on the
capture. We used the head command as the output was rather big to fit in the screenshot.

Dissector Tables

Most of the users reading this article are already familiar with the concept of Dissector. If not,
in simple words Dissector is simply a protocol parser. The output generated by this option
consists of 6 fields. Starting from the Dissector Table Name then the name is used for the
dissector table in the GUI format. Next, we have the type and the base for the display and the
Protocol Name. Lastly, we have the decode as a format.

tshark -G decodes | head
tshark -G dissector-tables

Page | 32

www.hackingarticles.in
Elastic Mapping

Mapping is the outline of the documents stored in the index. Elasticsearch supports different
data types for the fields in a document. The elastic-mapping option of the TShark prints out the
data stored inside the ElasticSearch mapping file. Due to a large amount of data getting printed,
we decided to use the head command as well.

Field Count

There are times in a network trace, where we need to get the count of the header fields travelling
at any moment. In such scenarios, TShark got our back. With the fieldcount option, we can
print the number of header fields with ease. As we can observe in the image given below that
we have 2522 protocols and 215000 fields were pre-allocated.

tshark -G elastic-mapping | head
tshark -G fieldcount

Page | 33

www.hackingarticles.in
Fields

TShark can also get us the contents of the registration database. The output generated by this
option is not as easy to interpret as the others. For some users, they can use any other parsing
tool for generating a better output. Each record in the output is a protocol or a header file. This
can be differentiated by the First field of the record. If the Field is P then it is a Protocol and if
it is F then it’s a header field. In the case of the Protocols, we have 2 more fields. One tells us
about the Protocol and other fields show the abbreviation used for the said protocol. In the case
of Header, the facts are a little different. We have 7 more fields. We have the Descriptive Name,
Abbreviation, Type, Parent Protocol Abbreviation, Base for Display, Bitmask, Blurb
Describing Field, etc.

Fundamental Types

TShark also helps us generate a report centralized around the fundamental types of network
protocol. This is abbreviated as ftype. This type of report consists of only 2 fields. One for the
FTYPE and other for its description.

tshark -G fields | head
tshark -G ftypes

Page | 34

www.hackingarticles.in

Heuristic Decodes

Sorting the Dissectors based on the heuristic decodes is one of the things that need to be easily
and readily available. For the same reason, we have the option of heuristic decodes in TShark.
This option prints all the heuristic decodes which are currently installed. It consists of 3 fields.
First, one representing the underlying dissector, the second one representing the name of the
heuristic decoded and the last one talks about the status of the heuristic. It will be T in case it
is heuristics and F otherwise.

tshark -G heuristic-decodes

Page | 35

www.hackingarticles.in

Plugins

Plugins are a very important kind of option that was integrated with Tshark Reporting options.
As the name states it prints the name of all the plugins that are installed. The field that this
report consists of is made of the Plugin Library, Plugin Version, Plugin Type and the path
where the plugin is located.

tshark –G plugins

Page | 36

www.hackingarticles.in
Protocols

If the users want to know the details about the protocols that are recorded in the registration
database then, they can use the protocols parameter. This output is also a bit less readable so
that the user can take the help of any third party tool to beautify the report. This parameter
prints the data in 3 fields. We have the protocol name, short name, and the filter name.

Values

Let’s talk about the values report. It consists of value strings, range strings, true/false strings.
There are three types of records available here. The first field can consist of one of these three
characters representing the following:
V: Value Strings
R: Range Strings
T: True/False Strings
Moreover, in the value strings, we have the field abbreviation, integer value, and the string. In
the range strings, we have the same values except it holds the lower bound and upper bound
values.

tshark –G protocols | head
tshark –G values | head

Page | 37

www.hackingarticles.in
Preferences

In case the user requires to revise the current preferences that are configured on the system,
they can use the currentprefs options to read the preference saved in the file.

Folders

Suppose the user wants to manually change the configurations or get the program information
or want to take a look at the lua configuration or some other important files. The users need the
path of those files to take a peek at them. Here the folders option comes a little handy.

tshark –G currentprefs | head
tshark –G folders

Page | 38

www.hackingarticles.in
Since we talked so extensively about TShark, It won’t be justice if we won’t talk about the tool
that is heavily dependent on the data from TShark. Let’s talk about PyShark.
PyShark

It is essentially a wrapper that is based on Python. Its functionality is that allows the python
packet parsing using the TShark dissectors. Many tools do the same job more or less but the
difference is that this tool can export XMLs to use its parsing. You can read more about it from
its GitHub page.
Installation

As the PyShark was developed using Python 3 and we don’t Python 3 installed on our machine.
We installed Python3 as shown in the image given below.

Since we have the python3 with pip we will install pyshark using pip command. You can also
install PyShark by cloning the git and running the setup.

apt install python3
pip3 install pyshark

Page | 39

www.hackingarticles.in

Live Capture

Now to get started, we need the python interpreter. To get this we write python3 and press
enter. Now that we have the interpreter, the very first thing that we plan on doing is importing
PyShark. Then we define network interface for the capture. Followed by that we will define
the value of the timeout parameter for the capture.sniff function. At last, we will begin the
capture. Here we can see that in the timeframe that we provided PyShark captured 9 packets.

Pretty Representation

There are multiple ways in which PyShark can represent data inside the captured packet. In the
previous practical, we captured 9 packets. Let’s take a look at the first packet that was captured
python3
import pyshark
capture = pyshark.LiveCapture(interface=’eth0’)
capture.sniff(timeout=5)
capture

Page | 40

www.hackingarticles.in
with PyShark. Here we can see that we have a layer-wise analysis with the ETH Layer, IP
Layer, and the TCP Layer.

capture[1].pretty_print()

Page | 41

www.hackingarticles.in
Captured Length Field

In our capture, we saw some data that can consist of multiple attributes. These attributes need
fields to get stored. To explore this field, we will be using the dir function in Python. We took
the packet and then defined the variable named pkt with the value of that packet and saved it.
Then using the dir function we saw explored the fields inside that particular capture. Here we
can see that we have the pretty_print function which we used in the previous practical. We also
have one field called captured_length to read into that we will write the name of the variable
followed by the name of the field with a period (.) in between as depicted in the image below.

Layers, Src and Dst Fields

For our next step, we need the fields of the IP packet. We used the dir function on the IP layer
and then we use src and dst fields here on this layer. We see that we have the IP Address as
this is the IP layer. As the Ethernet layer works on the MAC Addresses they store the MAC
Addresses of the Source and the Destination which changes when we come to the IP Layer.

pkt.layers
pkt.eth.src
pkt.eth.dst
pkt.eth.type
dir(pkt.ip)
pkt.ip.src
pkt.ip.dst
pkt.ip.pretty_print()

Page | 42

www.hackingarticles.in

Similarly, we can use the dir function and the field’s value on any layer of the capture. This
makes the investigation of the capture quite easier.

Promisc Capture

In previous articles we learned about the promisc mode that means that a network interface
card will pass all frames received up to the operating system for processing, versus the
traditional mode of operation wherein only frames destined for the NIC’s MAC address or a
broadcast address will be passed up to the OS. Generally, promiscuous mode is used to “sniff”
all traffic on the wire. But we got stuck when we configured the network interface card to work
on promisc mode. So, while capturing traffic on TShark we can switch between the normal
capture and the promisc capture using the –p parameter as shown in the image given below.

Page | 43

www.hackingarticles.in

References


https://www.hackingarticles.in/beginners-guide-to-tshark-part-1/

https://www.hackingarticles.in/beginners-guide-to-tshark-part-2/

https://www.hackingarticles.in/beginners-guide-to-tshark-part-3/
ifconfig eth0 promisc
ifconfig eth0
tshark -i eth0 -c 10
tshark -i eth0 -c 10 -p
JOIN OUR
TRAINING PROGRAMS
www.ignitetechnologies.in
BEGINNER
Network Pentest
Bug Bounty
Wireless Pentest
Network Security
Essentials
Ethical Hacking
ADVANCED
EXPERT
Burp Suite Pro
CTF
Windows
Linux
Pro
Infrastructure VAPT
APT’s - MITRE Attack Tactics
MSSQL Security Assessment
Active Directory Attack
Red Team Operation
Privilege Escalation
Web
Services-API
Android Pentest
Computer
Forensics
Advanced
Metasploit
CLICK HERE
