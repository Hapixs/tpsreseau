# TP4 : TCP, UDP et services réseau

Dans ce TP on va explorer un peu les protocoles TCP et UDP. 

**La première partie est détente**, vous explorez TCP et UDP un peu, en vous servant de votre PC.

La seconde partie se déroule en environnement virtuel, avec des VMs. Les VMs vont nous permettre en place des services réseau, qui reposent sur TCP et UDP.  
**Le but est donc de commencer à mettre les mains de plus en plus du côté administration, et pas simple client.**

Dans cette seconde partie, vous étudierez donc :

- le protocole SSH (contrôle de machine à distance)
- le protocole DNS (résolution de noms)
  - essentiel au fonctionnement des réseaux modernes

![TCP UDP](./pics/tcp_udp.jpg)

# Sommaire

- [TP4 : TCP, UDP et services réseau](#tp4--tcp-udp-et-services-réseau)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. First steps](#i-first-steps)
- [II. Mise en place](#ii-mise-en-place)
  - [1. SSH](#1-ssh)
  - [2. Routage](#2-routage)
- [III. DNS](#iii-dns)
  - [1. Présentation](#1-présentation)
  - [2. Setup](#2-setup)
  - [3. Test](#3-test)

# 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. On va en faire plusieurs, n'hésitez pas à diminuer la RAM (512Mo ou 1Go devraient suffire). Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Si vous voyez un 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu

➜ **L'emoji 🖥️ indique une VM à créer**. Pour chaque VM, vous déroulerez la checklist suivante :

- [x] Créer la machine (avec une carte host-only)
- [ ] Définir une IP statique à la VM
- [ ] Donner un hostname à la machine
- [ ] Vérifier que l'accès SSH fonctionnel
- [ ] Vérifier que le firewall est actif
- [ ] Remplir votre fichier `hosts`, celui de votre PC, pour accéder au VM avec un nom
- [ ] Dès que le routeur est en place, n'oubliez pas d'ajouter une route par défaut aux autres VM pour qu'elles aient internet

> Toutes les commandes pour réaliser ces opérations sont dans [le mémo Rocky](../../cours/memo/rocky_network.md). Aucune de ces étapes ne doit figurer dan le rendu, c'est juste la mise en place de votre environnement de travail.

# I. First steps

Faites-vous un petit top 5 des applications que vous utilisez sur votre PC souvent, des applications qui utilisent le réseau : un site que vous visitez souvent, un jeu en ligne, Spotify, j'sais po moi, n'importe.

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

- avec Wireshark, on va faire les chirurgiens réseau
- déterminez, pour chaque application :
  - IP et port du serveur auquel vous vous connectez
  - le port local que vous ouvrez pour vous connecter

> Dès qu'on se connecte à un serveur, notre PC ouvre un port random. Une fois la connexion TCP ou UDP établie, entre le port de notre PC et le port du serveur qui est en écoute, on parle de tunnel TCP ou de tunnel UDP.

```
[alexandre@alexandre-bouritos ~]$ sudo tcpdump -i wlan0 udp 
[sudo] Mot de passe de alexandre : 
Désolé, essayez de nouveau.
[sudo] Mot de passe de alexandre : 
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on wlan0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
11:21:54.988347 IP alexandre-bouritos.38366 > _gateway.domain: 3456+ A? gitlab.com. (28)
11:21:54.988395 IP alexandre-bouritos.38366 > _gateway.domain: 49284+ AAAA? gitlab.com. (28)
11:21:55.011958 IP alexandre-bouritos.57621 > _gateway.domain: 19219+ A? gitlab.com. (28)
11:21:55.012005 IP alexandre-bouritos.57621 > _gateway.domain: 32271+ AAAA? gitlab.com. (28)
11:21:55.012926 IP _gateway.domain > alexandre-bouritos.38366: 3456 1/0/0 A 172.65.251.78 (44)
11:21:55.012926 IP _gateway.domain > alexandre-bouritos.38366: 49284 1/0/0 AAAA 2606:4700:90:0:f22e:fbec:5bed:a9b9 (56)
11:21:55.014264 IP alexandre-bouritos.46772 > _gateway.domain: 2989+ A? gitlab.com. (28)
11:21:55.014303 IP alexandre-bouritos.46772 > _gateway.domain: 54688+ AAAA? gitlab.com. (28)
11:21:55.015129 IP _gateway.domain > alexandre-bouritos.57621: 19219 1/0/0 A 172.65.251.78 (44)
11:21:55.015130 IP _gateway.domain > alexandre-bouritos.57621: 32271 1/0/0 AAAA 2606:4700:90:0:f22e:fbec:5bed:a9b9 (56)
11:21:55.017113 IP _gateway.domain > alexandre-bouritos.46772: 2989 1/0/0 A 172.65.251.78 (44)
11:21:55.017114 IP _gateway.domain > alexandre-bouritos.46772: 54688 1/0/0 AAAA 2606:4700:90:0:f22e:fbec:5bed:a9b9 (56)
11:21:55.417594 IP alexandre-bouritos.34791 > _gateway.domain: 20391+ A? snowplow.trx.gitlab.net. (41)
11:21:55.417652 IP alexandre-bouritos.34791 > _gateway.domain: 31167+ AAAA? snowplow.trx.gitlab.net. (41)
11:21:55.471727 IP _gateway.domain > alexandre-bouritos.34791: 20391 4/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com., A 52.54.178.155, A 3.218.125.188, A 3.213.18.157 (159)
11:21:55.483202 IP _gateway.domain > alexandre-bouritos.34791: 31167 1/1/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com. (198)
11:21:57.725938 IP alexandre-bouritos.60331 > _gateway.domain: 8282+ A? snowplow.trx.gitlab.net. (41)
11:21:57.725980 IP alexandre-bouritos.60331 > _gateway.domain: 50000+ AAAA? snowplow.trx.gitlab.net. (41)
11:21:57.726629 IP alexandre-bouritos.60600 > _gateway.domain: 6433+ A? snowplow.trx.gitlab.net. (41)
11:21:57.730661 IP _gateway.domain > alexandre-bouritos.60331: 8282 4/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com., A 3.213.18.157, A 3.218.125.188, A 52.54.178.155 (159)
11:21:57.730662 IP _gateway.domain > alexandre-bouritos.60331: 50000 1/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com. (111)
11:21:57.730662 IP _gateway.domain > alexandre-bouritos.60600: 6433 4/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com., A 52.54.178.155, A 3.213.18.157, A 3.218.125.188 (159)
11:21:57.739318 IP alexandre-bouritos.39810 > _gateway.domain: 40169+ A? snowplow.trx.gitlab.net. (41)
11:21:57.739371 IP alexandre-bouritos.39810 > _gateway.domain: 5364+ AAAA? snowplow.trx.gitlab.net. (41)
11:21:57.742495 IP _gateway.domain > alexandre-bouritos.39810: 40169 4/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com., A 3.218.125.188, A 52.54.178.155, A 3.213.18.157 (159)
11:21:57.742496 IP _gateway.domain > alexandre-bouritos.39810: 5364 1/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com. (111)
11:21:58.188825 IP alexandre-bouritos.37428 > _gateway.domain: 12908+ A? snowplow.trx.gitlab.net. (41)
11:21:58.188869 IP alexandre-bouritos.37428 > _gateway.domain: 48211+ AAAA? snowplow.trx.gitlab.net. (41)
11:21:58.192333 IP _gateway.domain > alexandre-bouritos.37428: 12908 4/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com., A 3.213.18.157, A 3.218.125.188, A 52.54.178.155 (159)
11:21:58.192333 IP _gateway.domain > alexandre-bouritos.37428: 48211 1/0/0 CNAME snowplownlb-d9830d6cd70bfcf5.elb.us-east-1.amazonaws.com. (111)
11:22:02.381707 IP _gateway.ssdp > 239.255.255.250.ssdp: UDP, length 378
11:22:02.381707 IP _gateway.ssdp > 239.255.255.250.ssdp: UDP, length 323
11:22:02.381707 IP _gateway.ssdp > 239.255.255.250.ssdp: UDP, length 314
11:22:02.381707 IP _gateway.ssdp > 239.255.255.250.ssdp: UDP, length 388
11:22:02.442788 IP alexandre-bouritos.57481 > _gateway.domain: 58608+ PTR? 250.255.255.239.in-addr.arpa. (46)
11:22:02.465963 IP _gateway.domain > alexandre-bouritos.57481: 58608 NXDomain 0/1/0 (119)
11:22:10.948849 IP alexandre-bouritos.33239 > _gateway.domain: 27992+ A? safebrowsing.googleapis.com. (45)
11:22:10.948892 IP alexandre-bouritos.33239 > _gateway.domain: 52819+ AAAA? safebrowsing.googleapis.com. (45)
11:22:10.949564 IP alexandre-bouritos.34764 > _gateway.domain: 65197+ A? safebrowsing.googleapis.com. (45)
11:22:10.972811 IP _gateway.d
```


> Aussi, TCP ou UDP ? Comment le client sait ? Il sait parce que le serveur a décidé ce qui était le mieux pour tel ou tel type de trafic (un jeu, une page web, etc.) et que le logiciel client est codé pour utiliser TCP ou UDP en conséquence.

🌞 **Demandez l'avis à votre OS**

- votre OS est responsable de l'ouverture des ports, et de placer un programme en "écoute" sur un port
- il est aussi responsable de l'ouverture d'un port quand une application demande à se connecter à distance vers un serveur
- bref il voit tout quoi
- utilisez la commande adaptée à votre OS pour repérer, dans la liste de toutes les connexions réseau établies, la connexion que vous voyez dans Wireshark, pour chacune des 5 applications

**Il faudra ajouter des options adaptées aux commandes pour y voir clair. Pour rappel, vous cherchez des connexions TCP ou UDP.**

```
# MacOS
$ netstat

# GNU/Linux
$ ss

# Windows
$ netstat
```

🦈🦈🦈🦈🦈 **Bah ouais, captures Wireshark à l'appui évidemment.** Une capture pour chaque application, qui met bien en évidence le trafic en question.

# II. Mise en place

## 1. SSH

🖥️ **Machine `node1.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.11/24`

Connectez-vous en SSH à votre VM.

🌞 **Examinez le trafic dans Wireshark**

- **déterminez si SSH utilise TCP ou UDP**
  - pareil réfléchissez-y deux minutes, logique qu'on utilise pas UDP non ?
- **repérez le *3-Way Handshake* à l'établissement de la connexion**
  - c'est le `SYN` `SYNACK` `ACK`
- **repérez du trafic SSH**
- **repérez le FIN ACK à la fin d'une connexion**
- entre le *3-way handshake* et l'échange `FIN`, c'est juste une bouillie de caca chiffré, dans un tunnel TCP

> **SUR WINDOWS, pour cette étape uniquement**, utilisez Git Bash et PAS Powershell. Avec Powershell il sera très difficile d'observer le FIN ACK.


🌞 **Demandez aux OS**

- repérez, avec une commande adaptée (`netstat` ou `ss`), la connexion SSH depuis votre machine
- ET repérez la connexion SSH depuis votre VM


```
[alexandre@alexandre-bouritos ~]$ sudo ss -t -u -p | grep ssh
tcp   ESTAB 0      0                10.4.1.0:38132        10.4.1.11:ssh    users:(("ssh",pid=6095,fd=3))  
```

```
[hd0@node1 ~]$ sudo ss -t -u | grep ssh
[sudo] password for hd0: 
tcp   ESTAB 0      0          10.4.1.11:ssh      10.4.1.0:38132 
```

🦈 **Je veux une capture clean avec le 3-way handshake, un peu de trafic au milieu et une fin de connexion [ici](ssh_handcheck.pcapng)**

## 2. Routage

Ouais, un peu de répétition, ça fait jamais de mal. On va créer une machine qui sera notre routeur, et **permettra à toutes les autres machines du réseau d'avoir Internet.**

🖥️ **Machine `router.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.254/24` sur sa carte host-only
- ajoutez-lui une carte NAT, qui permettra de donner Internet aux autres machines du réseau
- référez-vous au TP précédent

> Rien à remettre dans le compte-rendu pour cette partie.

# III. DNS

## 1. Présentation

Un serveur DNS est un serveur qui est capable de répondre à des requêtes DNS.

Une requête DNS est la requête effectuée par une machine lorsqu'elle souhaite connaître l'adresse IP d'une machine, lorsqu'elle connaît son nom.

Par exemple, si vous ouvrez un navigateur web et saisissez `https://www.google.com` alors une requête DNS est automatiquement effectuée par votre PC pour déterminez à quelle adresse IP correspond le nom `www.google.com`.

> La partie `https://` ne fait pas partie du nom de domaine, ça indique simplement au navigateur la méthode de connexion. Ici, c'est HTTPS.

Dans cette partie, on va monter une VM qui porte un serveur DNS. Ce dernier répondra aux autres VMs du LAN quand elles auront besoin de connaître des noms. Ainsi, ce serveur pourra :

- résoudre des noms locaux
  - vous pourrez `ping node1.tp4.b1` et ça fonctionnera
  - mais aussi `ping www.google.com` et votre serveur DNS sera capable de le résoudre aussi

*Dans la vraie vie, il n'est pas rare qu'une entreprise gère elle-même ses noms de domaine, voire gère elle-même son serveur DNS. C'est donc du savoir ré-utilisable pour tous qu'on voit ici.*

> En réalité, ce n'est pas votre serveur DNS qui pourra résoudre `www.google.com`, mais il sera capable de *forward* (faire passer) votre requête à un autre serveur DNS qui lui, connaît la réponse.

![Haiku DNS](./pics/haiku_dns.png)

## 2. Setup

🖥️ **Machine `dns-server.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.201/24`

Installation du serveur DNS :

```bash
# assurez-vous que votre machine est à jour
$ sudo dnf update -y

# installation du serveur DNS, son p'tit nom c'est BIND9
$ sudo dnf install -y bind bind-utils
```

La configuration du serveur DNS va se faire dans 3 fichiers essentiellement :

- **un fichier de configuration principal**
  - `/etc/named.conf`
  - on définit les trucs généraux, comme les adresses IP et le port où on veu écouter
  - on définit aussi un chemin vers les autres fichiers, les fichiers de zone
- **un fichier de zone**
  - `/var/named/tp4.b1.db`
  - je vous préviens, la syntaxe fait mal
  - on peut y définir des correspondances `IP ---> nom`
- **un fichier de zone inverse**
  - `/var/named/tp4.b1.rev`
  - on peut y définir des correspondances `nom ---> IP`

➜ **Allooooons-y, fichier de conf principal**

```bash
# éditez le fichier de config principal pour qu'il ressemble à :
$ sudo cat /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
[...]
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        recursion yes;
[...]
# référence vers notre fichier de zone
zone "tp4.b1" IN {
     type master;
     file "tp4.b1.db";
     allow-update { none; };
     allow-query {any; };
};
# référence vers notre fichier de zone inverse
zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};
```

➜ **Et pour les fichiers de zone**

```bash
# Fichier de zone pour nom -> IP

$ sudo cat /var/named/tp4.b1.db

$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```

```bash
# Fichier de zone inverse pour IP -> nom

$ sudo cat /var/named/tp4.b1.rev

$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```

➜ **Une fois ces 3 fichiers en place, démarrez le service DNS**

```bash
# Démarrez le service tout de suite
$ sudo systemctl start named

# Faire en sorte que le service démarre tout seul quand la VM s'allume
$ sudo systemctl enable named

# Obtenir des infos sur le service
$ sudo systemctl status named

# Obtenir des logs en cas de probème
$ sudo journalctl -xe -u named
```

🌞 **Dans le rendu, je veux**

- un `cat` des fichiers de conf
- un `systemctl status named` qui prouve que le service tourne bien
- une commande `ss` qui prouve que le service écoute bien sur un port


``` bash
[hd0@dns-server ~]$ sudo cat /etc/named.conf 
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; };
        allow-query-cache { localhost; any; };

        /* 
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable 
           recursion. 
         - If your recursive DNS server has a public IP address, you MUST enable access 
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification 
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface 
        */
        recursion yes;

        dnssec-validation yes;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

zone "tp4.b1" IN {
        type master;
        file "tp4.b1.db";
        allow-update { none; };
        allow-query { any; };
};

zone "1.4.10.in-addr.arpa" IN {
        type master;
        file "tp4.b1.rev";
        allow-update { none; };
        allow-query { any; };
};
```

```bash
[hd0@dns-server ~]$ sudo cat /var/named/tp4.b1.db
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```

```bash 
[hd0@dns-server ~]$ sudo cat /var/named/tp4.b1.rev
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.

```

```bash
[hd0@dns-server ~]$ sudo systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Fri 2022-11-04 17:41:12 CET; 3min 41s ago
   Main PID: 42014 (named)
      Tasks: 5 (limit: 5905)
     Memory: 15.3M
        CPU: 270ms
     CGroup: /system.slice/named.service
             └─42014 /usr/sbin/named -u named -c /etc/named.conf
```

```bash
[hd0@dns-server ~]$ sudo ss -l -p | grep 42014
nl    UNCONN 0      0                                            rtnl:named/42014                    *                                                                                                   
nl    UNCONN 0      0                                            rtnl:named/42014                    *                                                                                                   
u_dgr UNCONN 0      0                                               * 57962                         * 11719 users:(("named",pid=42014,fd=3))                                                             
udp   UNCONN 0      0                                      10.4.1.201:domain                  0.0.0.0:*     users:(("named",pid=42014,fd=19))                                                            
udp   UNCONN 0      0                                       127.0.0.1:domain                  0.0.0.0:*     users:(("named",pid=42014,fd=16))                                                            
udp   UNCONN 0      0                                           [::1]:domain                     [::]:*     users:(("named",pid=42014,fd=22))                                                            
tcp   LISTEN 0      10                                     10.4.1.201:domain                  0.0.0.0:*     users:(("named",pid=42014,fd=21))                                                            
tcp   LISTEN 0      10                                      127.0.0.1:domain                  0.0.0.0:*     users:(("named",pid=42014,fd=17))                                                            
tcp   LISTEN 0      4096                                    127.0.0.1:rndc                    0.0.0.0:*     users:(("named",pid=42014,fd=24))                                                            
tcp   LISTEN 0      10                                          [::1]:domain                     [::]:*     users:(("named",pid=42014,fd=23))                                                            
tcp   LISTEN 0      4096                                        [::1]:rndc                       [::]:*     users:(("named",pid=42014,fd=25)) 
```

🌞 **Ouvrez le bon port dans le firewall**

- grâce à la commande `ss` vous devrez avoir repéré sur quel port tourne le service
  - vous l'avez écrit dans la conf aussi toute façon :)
- ouvrez ce port dans le firewall de la machine `dns-server.tp4.b1` (voir le mémo réseau Rocky)

## 3. Test

🌞 **Sur la machine `node1.tp4.b1`**

- configurez la machine pour qu'elle utilise votre serveur DNS quand elle a besoin de résoudre des noms
- assurez vous que vous pouvez :
  - résoudre des noms comme `node1.tp4.b1` et `dns-server.tp4.b1`
  - mais aussi des noms comme `www.google.com`

🌞 **Sur votre PC**

- utilisez une commande pour résoudre le nom `node1.tp4.b1` en utilisant `10.4.1.201` comme serveur DNS

> Le fait que votre serveur DNS puisse résoudre un nom comme `www.google.com`, ça s'appelle la récursivité et c'est activé avec la ligne `recursion yes;` dans le fichier de conf.

🦈 **Capture d'une requête DNS vers le nom `node1.tp4.b1` ainsi que la réponse**
