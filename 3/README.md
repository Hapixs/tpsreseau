# TP3 : On va router des trucs

Au menu de ce TP, on va revoir un peu ARP et IP histoire de **se mettre en jambes dans un environnement avec des VMs**.

Puis on mettra en place **un routage simple, pour permettre à deux LANs de communiquer**.

![Reboot the router](./pics/reboot.jpeg)

## Sommaire

- [TP3 : On va router des trucs](#tp3--on-va-router-des-trucs)
  - [Sommaire](#sommaire)
  - [0. Prérequis](#0-prérequis)
  - [I. ARP](#i-arp)
    - [1. Echange ARP](#1-echange-arp)
    - [2. Analyse de trames](#2-analyse-de-trames)
  - [II. Routage](#ii-routage)
    - [1. Mise en place du routage](#1-mise-en-place-du-routage)
    - [2. Analyse de trames](#2-analyse-de-trames-1)
    - [3. Accès internet](#3-accès-internet)
  - [III. DHCP](#iii-dhcp)
    - [1. Mise en place du serveur DHCP](#1-mise-en-place-du-serveur-dhcp)
    - [2. Analyse de trames](#2-analyse-de-trames-2)

## 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. 1Go RAM c'est large large. Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Vous aurez besoin de deux réseaux host-only dans VirtualBox :

- un premier réseau `10.3.1.0/24`
- le second `10.3.2.0/24`
- **vous devrez désactiver le DHCP de votre hyperviseur (VirtualBox) et définir les IPs de vos VMs de façon statique**

➜ Les firewalls de vos VMs doivent **toujours** être actifs (et donc correctement configurés).

➜ **Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

## I. ARP

Première partie simple, on va avoir besoin de 2 VMs.

| Machine  | `10.3.1.0/24` |
|----------|---------------|
| `john`   | `10.3.1.11`   |
| `marcel` | `10.3.1.12`   |

```schema
   john               marcel
  ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     │
  └─────┘    └───┘    └─────┘
```

> Référez-vous au [mémo Réseau Rocky](../../cours/memo/rocky_network.md) pour connaître les commandes nécessaire à la réalisation de cette partie.

### 1. Echange ARP

🌞**Générer des requêtes ARP**

- effectuer un `ping` d'une machine à l'autre
- observer les tables ARP des deux machines
- repérer l'adresse MAC de `john` dans la table ARP de `marcel` et vice-versa
- prouvez que l'info est correcte (que l'adresse MAC que vous voyez dans la table est bien celle de la machine correspondante)
  - une commande pour voir la MAC de `marcel` dans la table ARP de `john`
  - et une commande pour afficher la MAC de `marcel`, depuis `marcel`

```
[hd0@john ~]$ ping -c 1 marcel; ip -s n s | grep 10.3.1.12; ip a | grep link/ether 
PING marcel (10.3.1.12) 56(84) bytes of data.
64 bytes from 10.3.1.12: icmp_seq=1 ttl=64 time=1.62 ms

10.3.1.12 dev enp0s8 lladdr 08:00:27:10:e0:e7 ref 1 used 0/0/0 probes 4 REACHABLE

link/ether 08:00:27:8d:20:b3 brd ff:ff:ff:ff:ff:ff
```

```
[hd0@marcel ~]$ ping -c 1 john; ip -s neigh s | grep 10.3.1.11; ip a | grep link/ether
PING john (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=64 time=0.900 ms

10.3.1.11 dev enp0s8 lladdr 08:00:27:8d:20:b3 ref 1 used 0/115/0 probes 4 DELAY

link/ether 08:00:27:10:e0:e7 brd ff:ff:ff:ff:ff:ff
```

### 2. Analyse de trames

🌞**Analyse de trames**

- utilisez la commande `tcpdump` pour réaliser une capture de trame
- videz vos tables ARP, sur les deux machines, puis effectuez un `ping`

``` 
[hd0@marcel ~]$ ping -c 1 john
PING john (10.3.1.11) 56(84) bytes of data.
64 bytes from john (10.3.1.11): icmp_seq=1 ttl=64 time=1.26 ms
```

```
[hd0@marcel ~]$ sudo tcpdump -i enp0s8 arp
14:13:31.351801 ARP, Request who-has 10.3.1.11 tell marcel, length 28
14:13:31.352745 ARP, Reply 10.3.1.11 is-at 08:00:27:8d:20:b3 (oui Unknown), length 46
```

🦈 **Capture réseau `tp3_arp.pcapng`** qui contient un ARP request et un ARP reply

> **Si vous ne savez pas comment récupérer votre fichier `.pcapng`** sur votre hôte afin de l'ouvrir dans Wireshark, et me le livrer en rendu, demandez-moi.

## II. Routage

Vous aurez besoin de 3 VMs pour cette partie. **Réutilisez les deux VMs précédentes.**

| Machine  | `10.3.1.0/24` | `10.3.2.0/24` |
|----------|---------------|---------------|
| `router` | `10.3.1.254`  | `10.3.2.254`  |
| `john`   | `10.3.1.11`   | no            |
| `marcel` | no            | `10.3.2.12`   |

> Je les appelés `marcel` et `john` PASKON EN A MAR des noms nuls en réseau 🌻

```schema
   john                router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └───┘    └─────┘    └───┘    └─────┘
```

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

> Cette étape est nécessaire car Rocky Linux c'est pas un OS dédié au routage par défaut. Ce n'est bien évidemment une opération qui n'est pas nécessaire sur un équipement routeur dédié comme du matériel Cisco.


```
[hd0@rooter ~]$ sudo firewall-cmd --add-masquerade --zone=public --permanent; sudo firewall-cmd --reload; sudo firewall-cmd --list-all | grep public
success
success
public (active)
```

🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

- il faut taper une commande `ip route add` pour cela, voir mémo
- il faut ajouter une seule route des deux côtés
- une fois les routes en place, vérifiez avec un `ping` que les deux machines peuvent se joindre

```
[hd0@rooter network-scripts]$ cat /etc/sysconfig/network-scripts/route-enp0s*
10.3.1.0/24 via 10.3.1.254 dev enp0s8
10.3.2.0/24 via 10.3.2.254 dev enp0s9
```

```
[hd0@marcel ~]$ ping -c 3 john
PING john (10.3.1.11) 56(84) bytes of data.
64 bytes from john (10.3.1.11): icmp_seq=1 ttl=63 time=1.98 ms
64 bytes from john (10.3.1.11): icmp_seq=2 ttl=63 time=2.06 ms
64 bytes from john (10.3.1.11): icmp_seq=3 ttl=63 time=2.13 ms

--- john ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
```

```
[hd0@john ~]$ ping -c 3 marcel
PING marcel (10.3.2.12) 56(84) bytes of data.
64 bytes from marcel (10.3.2.12): icmp_seq=1 ttl=63 time=2.30 ms
64 bytes from marcel (10.3.2.12): icmp_seq=2 ttl=63 time=2.09 ms
64 bytes from marcel (10.3.2.12): icmp_seq=3 ttl=63 time=2.16 ms

--- marcel ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
```

![THE SIZE](./pics/thesize.png)

### 2. Analyse de trames

🌞**Analyse des échanges ARP**

- videz les tables ARP des trois noeuds
- effectuez un `ping` de `john` vers `marcel`
- regardez les tables ARP des trois noeuds
- essayez de déduire un peu les échanges ARP qui ont eu lieu
- répétez l'opération précédente (vider les tables, puis `ping`), en lançant `tcpdump` sur `marcel`
- **écrivez, dans l'ordre, les échanges ARP qui ont eu lieu, puis le ping et le pong, je veux TOUTES les trames** utiles pour l'échange

Par exemple (copiez-collez ce tableau ce sera le plus simple) :

| ordre | type trame  | IP source | MAC source              | IP destination | MAC destination            |
|-------|-------------|-----------|-------------------------|----------------|----------------------------|
| 1     | Requête ARP | 10.3.2.254         | router <br> `08:00:25:fe:8e:95`  | 10.3.2.12              | Broadcast <br> `FF:FF:FF:FF:FF` |
| 2     | Réponse ARP | 10.3.2.12         | marcel <br> `08:00:27:10:e0:e7`                       | 10.3.2.254              | router <br> `08:00:25:fe:8e:95`    |             |                            |
| 3     | Ping        | 10.3.2.254         | `08:00:25:fe:8e:95`                       | 10.3.2.12              |                          `08:00:27:10:e0:e7` |
| 4     | Pong        |  10.3.2.12        | `08:00:27:10:e0:e7`                       | 10.3.2.254              | `08:00:25:fe:8e:95`                         |

> Vous pourriez, par curiosité, lancer la capture sur `john` aussi, pour voir l'échange qu'il a effectué de son côté.

🦈 **Capture réseau [`tp3_routage_marcel.pcapng`](tp3_routage_marcel.pcapng)**

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

- ajoutez une carte NAT en 3ème inteface sur le `router` pour qu'il ait un accès internet
- ajoutez une route par défaut à `john` et `marcel`
  - vérifiez que vous avez accès internet avec un `ping`
  - le `ping` doit être vers une IP, PAS un nom de domaine
- donnez leur aussi l'adresse d'un serveur DNS qu'ils peuvent utiliser
  - vérifiez que vous avez une résolution de noms qui fonctionne avec `dig`
  - puis avec un `ping` vers un nom de domaine


🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`
- capturez le ping depuis `john` avec `tcpdump`
- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source              | IP destination | MAC destination |     |
|-------|------------|--------------------|-------------------------|----------------|-----------------|-----|
| 1     | ping       | `john` `10.3.1.11` | `john` `08:00:27:8d:20:b3` | `8.8.8.8`      | `08:00:27:e8:b0:e0`             |     |
| 2     | pong       |  `8.8.8.8`               | `08:00:27:e8:b0:e0`                     | `10.3.1.11`            | `08:00:27:8d:20:b3`             

🦈 **Capture réseau [tp3_routage_internet.pcapng](tp3_routage_internet.pcap)**

## III. DHCP

On reprend la config précédente, et on ajoutera à la fin de cette partie une 4ème machine pour effectuer des tests.

| Machine  | `10.3.1.0/24`              | `10.3.2.0/24` |
|----------|----------------------------|---------------|
| `router` | `10.3.1.254`               | `10.3.2.254`  |
| `john`   | `10.3.1.11`                | no            |
| `bob`    | oui mais pas d'IP statique | no            |
| `marcel` | no                         | `10.3.2.12`   |

```schema
   john               router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └─┬─┘    └─────┘    └───┘    └─────┘
   john        │
  ┌─────┐      │
  │     │      │
  │     ├──────┘
  └─────┘
```

### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** (go Google "rocky linux dhcp server").

- installation du serveur sur `john`
- créer une machine `bob`
- faites lui récupérer une IP en DHCP à l'aide de votre serveur

> Il est possible d'utilise la commande `dhclient` pour forcer à la main, depuis la ligne de commande, la demande d'une IP en DHCP, ou renouveler complètement l'échange DHCP (voir `dhclient -h` puis call me et/ou Google si besoin d'aide).

```
[hd0@john ~]$ sudo cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#


default-lease-time 900;
max-lease-time 10800;

option domain-name-servers 8.8.8.8;

authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
        range dynamic-bootp 10.3.1.200 10.3.1.250;
        option broadcast-address 10.3.1.255;
        option routers 10.3.1.254;
}
```

```
[hd0@bob ~]$ ip a | grep enp0s8
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.3.1.200/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
```


```
[hd0@bob ~]$ sudo dhclient -v  enp0s8
Listening on LPF/enp0s8/08:00:27:83:df:2a
Sending on   LPF/enp0s8/08:00:27:83:df:2a
Sending on   Socket/fallback
DHCPDISCOVER on enp0s8 to 255.255.255.255 port 67 interval 4 (xid=0x25777236)
DHCPOFFER of 10.3.1.201 from 10.3.1.11
DHCPREQUEST for 10.3.1.201 on enp0s8 to 255.255.255.255 port 67 (xid=0x25777236)
DHCPACK of 10.3.1.201 from 10.3.1.11 (xid=0x25777236)
bound to 10.3.1.201 -- renewal in 352 seconds.
```
🌞**Améliorer la configuration du DHCP**

- ajoutez de la configuration à votre DHCP pour qu'il donne aux clients, en plus de leur IP :
  - une route par défaut
  - un serveur DNS à utiliser
```
[hd0@john ~]$ sudo cat /etc/dhcp/dhcpd.conf
default-lease-time 900;
max-lease-time 10800;

option domain-name-servers 8.8.8.8;

authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
        range dynamic-bootp 10.3.1.200 10.3.1.250;
        option broadcast-address 10.3.1.255;
        option routers 10.3.1.254;
}
```
- récupérez de nouveau une IP en DHCP sur `bob` pour tester :
  - `bob` doit avoir une IP
    - vérifier avec une commande qu'il a récupéré son IP
    - vérifier qu'il peut `ping` sa passerelle
```
[hd0@bob ~]$ ip a | grep enp0s8; ping -c 1 10.3.1.0
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    inet 10.3.1.200/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
    inet 10.3.1.201/24 brd 10.3.1.255 scope global secondary dynamic enp0s8

PING 10.3.1.0 (10.3.1.0) 56(84) bytes of data.
64 bytes from 10.3.1.0: icmp_seq=1 ttl=64 time=0.620 ms

--- 10.3.1.0 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```
  - il doit avoir une route par défaut
    - vérifier la présence de la route avec une commande
    - vérifier que la route fonctionne avec un `ping` vers une IP
```
[hd0@bob ~]$ ip r s; ping -c 1 10.3.2.12
default via 10.3.1.254 dev enp0s8 
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.200 metric 100 
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.200 metric 100 

PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=2.20 ms

--- 10.3.2.12 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```
  - il doit connaître l'adresse d'un serveur DNS pour avoir de la résolution de noms
    - vérifier avec la commande `dig` que ça fonctionne
    - vérifier un `ping` vers un nom de domaine

```
[hd0@bob ~]$ dig google.com; ping -c 1 google.com
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.179.78

;; SERVER: 8.8.8.8#53(8.8.8.8)

PING google.com (142.250.179.78) 56(84) bytes of data.
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=1 ttl=61 time=25.9 ms

--- google.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
```

### 2. Analyse de trames

🌞**Analyse de trames**

- lancer une capture à l'aide de `tcpdump` afin de capturer un échange DHCP
- demander une nouvelle IP afin de générer un échange DHCP
- exportez le fichier `.pcapng`


```
[hd0@john ~]$ sudo tcpdump -i enp0s8 -w tp3_dhcp.pcapng port 67
```
```
[hd0@bob ~]$ sudo dhclient -v -r enp0s8; sudo dhclient enp0s8
```
🦈 **Capture réseau [tp3_dhcp.pcapng](tp3_dhcp.pcapng)**
