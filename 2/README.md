# TP2 : Ethernet, IP, et ARP

Dans ce TP on va approfondir trois protocoles, qu'on a survolé jusqu'alors :

- **IPv4** *(Internet Protocol Version 4)* : gestion des adresses IP
  - on va aussi parler d'ICMP, de DHCP, bref de tous les potes d'IP quoi !
- **Ethernet** : gestion des adresses MAC
- **ARP** *(Address Resolution Protocol)* : permet de trouver l'adresse MAC de quelqu'un sur notre réseau dont on connaît l'adresse IP

![Seventh Day](./pics/tcpip.jpg)

# Sommaire

- [TP2 : Ethernet, IP, et ARP](#tp2--ethernet-ip-et-arp)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. Setup IP](#i-setup-ip)
- [II. ARP my bro](#ii-arp-my-bro)
- [II.5 Interlude hackerzz](#ii5-interlude-hackerzz)
- [III. DHCP you too my brooo](#iii-dhcp-you-too-my-brooo)

# 0. Prérequis

**Il vous faudra deux machines**, vous êtes libres :

- toujours possible de se connecter à deux avec un câble
- sinon, votre PC + une VM ça fait le taf, c'est pareil
  - je peux aider sur le setup, comme d'hab

> Je conseille à tous les gens qui n'ont pas de port RJ45 de go PC + VM pour faire vous-mêmes les manips, mais on fait au plus simple hein.

---

**Toutes les manipulations devront être effectuées depuis la ligne de commande.** Donc normalement, plus de screens.

**Pour Wireshark, c'est pareil,** NO SCREENS. La marche à suivre :

- vous capturez le trafic que vous avez à capturer
- vous stoppez la capture (bouton carré rouge en haut à gauche)
- vous sélectionnez les paquets/trames intéressants (CTRL + clic)
- File > Export Specified Packets...
- dans le menu qui s'ouvre, cochez en bas "Selected packets only"
- sauvegardez, ça produit un fichier `.pcapng` (qu'on appelle communément "un ptit PCAP frer") que vous livrerez dans le dépôt git

**Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

# I. Setup IP

Le lab, il vous faut deux machines : 

- les deux machines doivent être connectées physiquement
- vous devez choisir vous-mêmes les IPs à attribuer sur les interfaces réseau, les contraintes :
  - IPs privées (évidemment n_n)
  - dans un réseau qui peut contenir au moins 1000 adresses IP (il faut donc choisir un masque adapté)
  - oui c'est random, on s'exerce c'est tout, p'tit jog en se levant c:
  - le masque choisi doit être le plus grand possible (le plus proche de 32 possible) afin que le réseau soit le plus petit possible

🌞 **Mettez en place une configuration réseau fonctionnelle entre les deux machines**

- vous renseignerez dans le compte rendu :
  - les deux IPs choisies, en précisant le masque
  - l'adresse de réseau
  - l'adresse de broadcast
- vous renseignerez aussi les commandes utilisées pour définir les adresses IP *via* la ligne de commande

> Rappel : tout doit être fait *via* la ligne de commandes. Faites-vous du bien, et utilisez Powershell plutôt que l'antique cmd sous Windows svp.

Hote

```
[alexandre@alexandre-bouritos ~]$ ip a | grep vbox
4: vboxnet0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 192.168.56.4/22 brd 192.168.59.255 scope global vboxnet0
[alexandre@alexandre-bouritos ~]$ ipcalc 192.168.56.4/22
Address:   192.168.56.4         11000000.10101000.001110 00.00000100
Netmask:   255.255.252.0 = 22   11111111.11111111.111111 00.00000000
Wildcard:  0.0.3.255            00000000.00000000.000000 11.11111111
=>
Network:   192.168.56.0/22      11000000.10101000.001110 00.00000000
HostMin:   192.168.56.1         11000000.10101000.001110 00.00000001
HostMax:   192.168.59.254       11000000.10101000.001110 11.11111110
Broadcast: 192.168.59.255       11000000.10101000.001110 11.11111111
Hosts/Net: 1022                  Class C, Private Internet

```
VM
```
user@debian:~$ cat /etc/network/interfaces
auto enp0s8
iface enp0s8 inet static
                address 192.168.56.200/22
```
```
user@debian:~$ ip a | grep enp0s8
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.56.200/22 brd 192.168.59.255 scope global enp0s8
user@debian:~$ ipcalc 192.168.56.200/22
Address:   192.168.56.200       11000000.10101000.001110 00.11001000
Netmask:   255.255.252.0 = 22   11111111.11111111.111111 00.00000000
Wildcard:  0.0.3.255            00000000.00000000.000000 11.11111111
=>
Network:   192.168.56.0/22      11000000.10101000.001110 00.00000000
HostMin:   192.168.56.1         11000000.10101000.001110 00.00000001
HostMax:   192.168.59.254       11000000.10101000.001110 11.11111110
Broadcast: 192.168.59.255       11000000.10101000.001110 11.11111111
Hosts/Net: 1022                  Class C, Private Internet

```

🌞 **Prouvez que la connexion est fonctionnelle entre les deux machines**

- un `ping` suffit !

```
[alexandre@alexandre-bouritos ~]$ ping 192.168.56.200
PING 192.168.56.200 (192.168.56.200) 56(84) octets de données.
64 octets de 192.168.56.200 : icmp_seq=1 ttl=64 temps=0.615 ms
64 octets de 192.168.56.200 : icmp_seq=2 ttl=64 temps=0.614 ms
64 octets de 192.168.56.200 : icmp_seq=3 ttl=64 temps=0.582 ms
64 octets de 192.168.56.200 : icmp_seq=4 ttl=64 temps=0.610 ms
```

🌞 **Wireshark it**



- `ping` ça envoie des paquets de type ICMP (c'est pas de l'IP, c'est un de ses frères)
  - les paquets ICMP sont encapsulés dans des trames Ethernet, comme les paquets IP
  - il existe plusieurs types de paquets ICMP, qui servent à faire des trucs différents
- **déterminez, grâce à Wireshark, quel type de paquet ICMP est envoyé par `ping`**
  - pour le ping que vous envoyez
  - et le pong que vous recevez en retour

> Vous trouverez sur [la page Wikipedia de ICMP](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) un tableau qui répertorie tous les types ICMP et leur utilité

🦈 **[PCAP qui contient les paquets ICMP qui vous ont permis d'identifier les types ](./sn_ping.pcapng)**

# II. ARP my bro

ARP permet, pour rappel, de résoudre la situation suivante :

- pour communiquer avec quelqu'un dans un LAN, il **FAUT** connaître son adresse MAC
- on admet un PC1 et un PC2 dans le même LAN :
  - PC1 veut joindre PC2
  - PC1 et PC2 ont une IP correctement définie
  - PC1 a besoin de connaître la MAC de PC2 pour lui envoyer des messages
  - **dans cette situation, PC1 va utilise le protocole ARP pour connaître la MAC de PC2**
  - une fois que PC1 connaît la mac de PC2, il l'enregistre dans sa **table ARP**

🌞 **Check the ARP table**

- utilisez une commande pour afficher votre table ARP
- déterminez la MAC de votre binome depuis votre table ARP
- déterminez la MAC de la *gateway* de votre réseau
  - celle de votre réseau physique, WiFi, genre YNOV, car il n'y en a pas dans votre ptit LAN
  - c'est juste pour vous faire manipuler un peu encore :)

> Il peut être utile de ré-effectuer des `ping` avant d'afficher la table ARP. En effet : les infos stockées dans la table ARP ne sont stockées que temporairement. Ce laps de temps est de l'ordre de ~60 secondes sur la plupart de nos machines.


```
[alexandre@alexandre-bouritos ~]$ arp
Address                  HWtype  HWaddress           Flags Mask            Iface
_gateway                 ether   00:c0:e7:e0:04:4e   C                     wlan0
192.168.56.200           ether   08:00:27:fc:8a:9d   C                     vboxnet0
```


🌞 **Manipuler la table ARP**

- utilisez une commande pour vider votre table ARP
- prouvez que ça fonctionne en l'affichant et en constatant les changements
- ré-effectuez des pings, et constatez la ré-apparition des données dans la table ARP

> Les échanges ARP sont effectuées automatiquement par votre machine lorsqu'elle essaie de joindre une machine sur le même LAN qu'elle. Si la MAC du destinataire n'est pas déjà dans la table ARP, alors un échange ARP 
sera déclenché.

```
[alexandre@alexandre-bouritos ~]$ arp
Address                  HWtype  HWaddress           Flags Mask            Iface
_gateway                 ether   00:c0:e7:e0:04:4e   C                     wlan0
[alexandre@alexandre-bouritos ~]$ ping 192.168.56.200
PING 192.168.56.200 (192.168.56.200) 56(84) octets de données.
64 octets de 192.168.56.200 : icmp_seq=1 ttl=64 temps=1.08 ms
64 octets de 192.168.56.200 : icmp_seq=2 ttl=64 temps=0.541 ms
64 octets de 192.168.56.200 : icmp_seq=3 ttl=64 temps=0.569 ms
64 octets de 192.168.56.200 : icmp_seq=4 ttl=64 temps=0.539 ms
64 octets de 192.168.56.200 : icmp_seq=5 ttl=64 temps=0.654 ms
[alexandre@alexandre-bouritos ~]$ arp
Address                  HWtype  HWaddress           Flags Mask            Iface
_gateway                 ether   00:c0:e7:e0:04:4e   C                     wlan0
192.168.56.200           ether   08:00:27:fc:8a:9d   C                     vboxnet0
```

🌞 **Wireshark it**

- vous savez maintenant comment forcer un échange ARP : il sufit de vider la table ARP et tenter de contacter quelqu'un, l'échange ARP se fait automatiquement
- mettez en évidence les deux trames ARP échangées lorsque vous essayez de contacter quelqu'un pour la "première" fois
  - déterminez, pour les deux trames, les adresses source et destination
  - déterminez à quoi correspond chacune de ces adresses

🦈 **[PCAP qui contient les trames ARP](sn_ping_arp.pcapng)**

> L'échange ARP est constitué de deux trames : un ARP broadcast et un ARP reply.

# II.5 Interlude hackerzz

**Chose promise chose due, on va voir les bases de l'usurpation d'identité en réseau : on va parler d'*ARP poisoning*.**

> On peut aussi trouver *ARP cache poisoning* ou encore *ARP spoofing*, ça désigne la même chose.

Le principe est simple : on va "empoisonner" la table ARP de quelqu'un d'autre.  
Plus concrètement, on va essayer d'introduire des fausses informations dans la table ARP de quelqu'un d'autre.

Entre introduire des fausses infos et usurper l'identité de quelqu'un il n'y a qu'un pas hihi.

---

➜ **Le principe de l'attaque**

- on admet Alice, Bob et Eve, tous dans un LAN, chacun leur PC
- leur configuration IP est ok, tout va bien dans le meilleur des mondes
- **Eve 'lé pa jonti** *(ou juste un agent de la CIA)* : elle aimerait s'immiscer dans les conversations de Alice et Bob
  - pour ce faire, Eve va empoisonner la table ARP de Bob, pour se faire passer pour Alice
  - elle va aussi empoisonner la table ARP d'Alice, pour se faire passer pour Bob
  - ainsi, tous les messages que s'envoient Alice et Bob seront en réalité envoyés à Eve

➜ **La place de ARP dans tout ça**

- ARP est un principe de question -> réponse (broadcast -> *reply*)
- IL SE TROUVE qu'on peut envoyer des *reply* à quelqu'un qui n'a rien demandé :)
- il faut donc simplement envoyer :
  - une trame ARP reply à Alice qui dit "l'IP de Bob se trouve à la MAC de Eve" (IP B -> MAC E)
  - une trame ARP reply à Bob qui dit "l'IP de Alice se trouve à la MAC de Eve" (IP A -> MAC E)
- ha ouais, et pour être sûr que ça reste en place, il faut SPAM sa mum, genre 1 reply chacun toutes les secondes ou truc du genre
  - bah ui ! Sinon on risque que la table ARP d'Alice ou Bob se vide naturellement, et que l'échange ARP normal survienne
  - aussi, c'est un truc possible, mais pas normal dans cette utilisation là, donc des fois bon, ça chie, DONC ON SPAM

![Am I ?](./pics/arp_snif.jpg)

---

➜ J'peux vous aider à le mettre en place, mais **vous le faites uniquement dans un cadre privé, chez vous, ou avec des VMs**

➜ **Je vous conseille 3 machines Linux**, Alice Bob et Eve. La commande `[arping](https://sandilands.info/sgordon/arp-spoofing-on-wired-lan)` pourra vous carry : elle permet d'envoyer manuellement des trames ARP avec le contenu de votre choix.

GLHF.

# III. DHCP you too my brooo

![YOU GET AN IP](./pics/dhcp.jpg)

*DHCP* pour *Dynamic Host Configuration Protocol* est notre p'tit pote qui nous file des IPs quand on arrive dans un réseau, parce que c'est chiant de le faire à la main :)

Quand on arrive dans un réseau, notre PC contacte un serveur DHCP, et récupère généralement 3 infos :

- **1.** une IP à utiliser
- **2.** l'adresse IP de la passerelle du réseau
- **3.** l'adresse d'un serveur DNS joignable depuis ce réseau

L'échange DHCP  entre un client et le serveur DHCP consiste en 4 trames : **DORA**, que je vous laisse chercher sur le web vous-mêmes : D

🌞 **Wireshark it**

- identifiez les 4 trames DHCP lors d'un échange DHCP
  - mettez en évidence les adresses source et destination de chaque trame
- identifiez dans ces 4 trames les informations **1**, **2** et **3** dont on a parlé juste au dessus

🦈 **[PCAP qui contient l'échange DORA](sn_dhclient_request.pcapng)**

> **Soucis** : l'échange DHCP ne se produit qu'à la première connexion. **Pour forcer un échange DHCP**, ça dépend de votre OS. Sur **GNU/Linux**, avec `dhclient` ça se fait bien. Sur **Windows**, le plus simple reste de définir une IP statique pourrie sur la carte réseau, se déconnecter du réseau, remettre en DHCP, se reconnecter au réseau. Sur **MacOS**, je connais peu mais Internet dit qu'c'est po si compliqué, appelez moi si besoin.