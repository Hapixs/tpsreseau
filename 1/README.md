# TP1 - Premier pas réseau

Le terme *réseau* désigne au sens large toutes les fonctionnalités d'un PC permettant de se connecter à d'autres machines.  

Le protocole IP est très important, il est central dans l'utilisation du réseau moderne.

> On va voir IPv4 en cours, il existe aussi IPv6, plus récent, qui fonctionne sur les mêmes principes. Nous en parlerons aussi en cours.

---

Lorsque l'on parle de réseau, on désigne souvent par le terme *client* tout équipement qui porte une adresse IP.

Donc vos PCs sont des *clients*, et on va explorer leur *réseau* dans ce TP.

![Big Deal](./pics/bigdeal.jpg)

# Sommaire
- [TP1 - Premier pas réseau](#tp1---premier-pas-réseau)
- [Sommaire](#sommaire)
- [Déroulement et rendu du TP](#déroulement-et-rendu-du-tp)
- [I. Exploration locale en solo](#i-exploration-locale-en-solo)
  - [1. Affichage d'informations sur la pile TCP/IP locale](#1-affichage-dinformations-sur-la-pile-tcpip-locale)
    - [En ligne de commande](#en-ligne-de-commande)
    - [En graphique (GUI : Graphical User Interface)](#en-graphique-gui--graphical-user-interface)
  - [2. Modifications des informations](#2-modifications-des-informations)
    - [A. Modification d'adresse IP (part 1)](#a-modification-dadresse-ip-part-1)
- [II. Exploration locale en duo](#ii-exploration-locale-en-duo)
  - [1. Prérequis](#1-prérequis)
  - [2. Câblage](#2-câblage)
  - [Création du réseau (oupa)](#création-du-réseau-oupa)
  - [3. Modification d'adresse IP](#3-modification-dadresse-ip)
  - [4. Utilisation d'un des deux comme gateway](#4-utilisation-dun-des-deux-comme-gateway)
  - [5. Petit chat privé](#5-petit-chat-privé)
  - [6. Firewall](#6-firewall)
- [III. Manipulations d'autres outils/protocoles côté client](#iii-manipulations-dautres-outilsprotocoles-côté-client)
  - [1. DHCP](#1-dhcp)
  - [2. DNS](#2-dns)
- [IV. Wireshark](#iv-wireshark)
- [Bilan](#bilan)

# Déroulement et rendu du TP

- Groupe de 2 jusqu'à 4 personnes. Il faut au moins deux PCs avec une prise RJ45 (Ethernet) par groupe
- Un câble RJ45 (fourni) pour connecter les deux PCs
- **Un compte-rendu par personne**
  - vu que vous travaillez en groupe, aucun problème pour copier/coller les parties à faire à plusieurs (tout le [`II.`](#ii-exploration-locale-en-duo))
  - une bonne partie est à faire de façon individuelle malgré tout (tout le [`I.`](#i-exploration-locale-en-solo) et le [`III.`](#iii-manipulations-dautres-outilsprotocoles-côté-client))
- Le rendu doit :
  - comporter des réponses aux questions explicites
  - comporter la marche à suivre pour réaliser les étapes demandées :
    - en ligne de commande, copier/coller des commandes et leurs résultat : **JE NE VEUX AUCUN SCREEN DE LIGNE DE COMMANDE**
    - en interface graphique, screenshots ou nom des menus où cliquer (sinon ça peut vite faire 1000 screenshots)
  - par exemple, pour la partie `1.A.` je veux le la commande tapée et le résultat
  - de façon générale, tout ce que vous faites et qui fait partie du TP, vous me le mettez :)

**⚠️ ⚠️ Désactivez votre firewall pour ce TP. ⚠️ ⚠️**

# I. Exploration locale en solo

## 1. Affichage d'informations sur la pile TCP/IP locale

### En ligne de commande

En utilisant la ligne de commande (CLI) de votre OS :

**🌞 Affichez les infos des cartes réseau de votre PC**

```
[alexandre@alexandre-bouritos tpsreseau]$ ip a 
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
link/ether c8:21:58:93:d8:f2 brd ff:ff:ff:ff:ff:ff
inet 192.168.21.158/24 brd 192.168.21.255 scope global dynamic noprefixroute wlan0
    valid_lft 3321sec preferred_lft 3321sec
inet6 2a01:cb01:3019:d60:7eea:ee2b:cf2d:a1c7/64 scope global dynamic noprefixroute 
    valid_lft 3325sec preferred_lft 3325sec
inet6 fe80::549:1ba3:9bcc:9004/64 scope link noprefixroute 
    valid_lft forever preferred_lft forever
```
```
2: eno1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
link/ether c8:d3:ff:ee:4a:cb brd ff:ff:ff:ff:ff:ff
altname enp9s0
```

**🌞 Affichez votre gateway**

```
[alexandre@alexandre-bouritos tpsreseau]$ ip r | grep default
default via 192.168.21.108 dev wlan0 proto dhcp src 192.168.21.158 metric 600 
```

**🌞 Déterminer la MAC de la passerelle**

``` 
[alexandre@alexandre-bouritos tpsreseau]$ arp | grep _gateway
_gateway                 ether   62:19:a2:88:41:93   C                     wlan0
```

### En graphique (GUI : Graphical User Interface)

En utilisant l'interface graphique de votre OS :  

**🌞 Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**

En tant qu'utilisateur KDE, pas possible d'avoir les infos avec le GUI.

*(L'interface graphique c'est pour les MAC, nous on mange du cli au petit dej)*

## 2. Modifications des informations

### A. Modification d'adresse IP (part 1)  

🌞 Utilisez l'interface graphique de votre OS pour **changer d'adresse IP** :

```
[alexandre@alexandre-bouritos tpsreseau]$ sudo ip a add 192.168.21.200/24 dev wlan0 ; ip a | grep wlan0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    inet 192.168.21.158/24 brd 192.168.21.255 scope global dynamic noprefixroute wlan0
    inet 192.168.21.200/24 scope global secondary wlan0
```

🌞 **Il est possible que vous perdiez l'accès internet.** Que ce soit le cas ou non, expliquez pourquoi c'est possible de perdre son accès internet en faisant cette opération.
>Si vous utilisez la même IP que quelqu'un d'autre, il se passerait la même chose qu'en vrai avec des adresses postales :
>  - deux personnes habitent au même numéro dans la même rue, mais dans deux maisons différentes
>  - quand une de ces personnes envoie un message, aucun problème, l'adresse du destinataire est unique, la lettre sera reçue
>  - par contre, pour envoyer un message à l'une de ces deux personnes, le facteur sera dans l'impossibilité de savoir dans quelle boîte aux lettres il doit poser le message
>  - ça marche à l'aller, mais pas au retour 

## II. Exploration locale en duo (Test avec Maxance Ferran)
### 3. Modification d'adresse IP
##### 🌞 Modifiez l'IP des deux machines pour qu'elles soient dans le même réseau
![](https://i.imgur.com/z3FqGi9.png)

##### 🌞 Vérifier à l'aide d'une commande que votre IP a bien été changée
```
PS C:\Users\alanw> ipconfig /all

Carte Ethernet Ethernet :

   Adresse IPv4. . . . . . . . . . . . . .: 10.10.10.69(préféré)

```
##### 🌞 Vérifier que les deux machines se joignent
```
PS C:\Users\alanw> ping 10.10.10.96

Envoi d’une requête 'Ping'  10.10.10.96 avec 32 octets de données :
Réponse de 10.10.10.96 : octets=32 temps=1 ms TTL=128
Réponse de 10.10.10.96 : octets=32 temps=1 ms TTL=128
Réponse de 10.10.10.96 : octets=32 temps=1 ms TTL=128
Réponse de 10.10.10.96 : octets=32 temps=1 ms TTL=128

Statistiques Ping pour 10.10.10.96:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 1ms, Maximum = 1ms, Moyenne = 1ms
```
##### 🌞 Déterminer l'adresse MAC de votre correspondant
```
PS C:\Users\alanw> arp -a


Interface : 10.10.10.69 --- 0x5
  Adresse Internet      Adresse physique      Type
  10.10.10.96           d8-bb-c1-aa-c0-e7     dynamique   <---
  10.10.11.255          ff-ff-ff-ff-ff-ff     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique
```

### 4. Utilisation d'un des deux comme gateway
##### 🌞Tester l'accès internet

```
PS C:\Users\maxfe> ping 1.1.1.1

Envoi d’une requête 'Ping'  1.1.1.1 avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=28 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=25 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=25 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=28 ms TTL=54

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 25ms, Maximum = 28ms, Moyenne = 26ms
```


##### 🌞 Prouver que la connexion Internet passe bien par l'autre PC

```
PS C:\Users\maxfe> tracert 192.168.137.1

Détermination de l’itinéraire vers TelosGVNG [192.168.137.1]
avec un maximum de 30 sauts :

  1     1 ms     1 ms     1 ms  TelosGVNG [192.168.137.1]

Itinéraire déterminé.
```

### 5. Petit chat privé
##### 🌞 sur le PC serveur : 
```
PS C:\Users\alanw\netcat-1.11> .\nc.exe -l -p 8888
```
##### 🌞 sur le PC client: 
```
PS C:\Users\maxfe\Desktop\netcat-win32-1.11\netcat-1.11> .\nc.exe 192.168.137.1 8888
```
#### CONVERSATION : 
```
[fmaxance] : Salut !
[balan] : Salut
[balan] : ça dit quoi ?
[fmaxance] : rien de spécial mise à part que j'aime les pommes et toi ?
[balan] : bah écoute j'aime les pommes aussi
[fmaxance] : SUPER en revoir
```
##### 🌞 Visualiser la connexion en cours

```
PS C:\Users\alanw> netstat -a -n -b

  TCP    192.168.137.1:8888     192.168.137.2:56320    ESTABLISHED
 [nc.exe]
```
##### 🌞 Pour aller un peu plus loin

IP non définie : 
```
PS C:\Users\alanw\netcat-1.11> ./nc.exe -l -p 8888

PS C:\Users\alanw> netstat -a -n -b | Select-String 8888

  TCP    0.0.0.0:8888           0.0.0.0:0              LISTENING
```
N'importe qui peut se connecter sur le serveur car l'IP est non définie.


IP définie : 
```
PS C:\Users\alanw\netcat-1.11> ./nc.exe -l -p 8888 -s 192.168.137.1
PS C:\Users\alanw> netstat -a -n -b | Select-String 8888

  TCP    192.168.137.1:8888     0.0.0.0:0              LISTENING
```
### 6. Firewall
#### 🌞 Activez et configurez votre firewall


![](https://i.imgur.com/XNnmoOO.png)
# III. Manipulations d'autres outils/protocoles côté client

## 1. DHCP

Bon ok vous savez définir des IPs à la main. Mais pour être dans le réseau YNOV, vous l'avez jamais fait.  

C'est le **serveur DHCP** d'YNOV qui vous a donné une IP.

Une fois que le serveur DHCP vous a donné une IP, vous enregistrer un fichier appelé *bail DHCP* qui contient, entre autres :

- l'IP qu'on vous a donné
- le réseau dans lequel cette IP est valable

🌞**Exploration du DHCP, depuis votre PC**

```
[alexandre@alexandre-bouritos ~]$ cat /var/lib/dhclient/dhclient.leases 
lease {
  interface "wlan0";
  fixed-address 10.33.16.120;
  option subnet-mask 255.255.252.0;
  option dhcp-lease-time 86400;
  option routers 10.33.19.254;
  option dhcp-message-type 5;
  option dhcp-server-identifier 10.33.19.254;
  option domain-name-servers 8.8.8.8,8.8.4.4,1.1.1.1;
  renew 3 2022/10/05 18:46:16;
  rebind 4 2022/10/06 04:34:14;
  expire 4 2022/10/06 07:34:14;
}
```

## 2. DNS

Le protocole DNS permet la résolution de noms de domaine vers des adresses IP. Ce protocole permet d'aller sur `google.com` plutôt que de devoir connaître et utiliser l'adresse IP du serveur de Google.  

Un **serveur DNS** est un serveur à qui l'on peut poser des questions (= effectuer des requêtes) sur un nom de domaine comme `google.com`, afin d'obtenir les adresses IP liées au nom de domaine.  

Si votre navigateur fonctionne "normalement" (il vous permet d'aller sur `google.com` par exemple) alors votre ordinateur connaît forcément l'adresse d'un serveur DNS. Et quand vous naviguez sur internet, il effectue toutes les requêtes DNS à votre place, de façon automatique.

```
[alexandre@alexandre-bouritos ~]$ cat /etc/resolv.conf 
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver 1.1.1.1
```

```
[alexandre@alexandre-bouritos ~]$ dig google.com
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             242     IN      A       216.58.215.46

;; Query time: 26 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
```

```
[alexandre@alexandre-bouritos ~]$ dig ynov.com

;; QUESTION SECTION:
;ynov.com.                      IN      A

;; ANSWER SECTION:
ynov.com.               300     IN      A       172.67.74.226
ynov.com.               300     IN      A       104.26.11.233
ynov.com.               300     IN      A       104.26.10.233

;; Query time: 36 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
```

```
[alexandre@alexandre-bouritos ~]$ dig -x 78.73.21.21

;; QUESTION SECTION:
;21.21.73.78.in-addr.arpa.      IN      PTR

;; ANSWER SECTION:
21.21.73.78.in-addr.arpa. 3600  IN      PTR     78-73-21-21-no168.tbcn.telia.com.

;; Query time: 36 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
```

```
[alexandre@alexandre-bouritos ~]$ dig -x 22.146.54.58

;; QUESTION SECTION:
;58.54.146.22.in-addr.arpa.     IN      PTR

;; AUTHORITY SECTION:
in-addr.arpa.           2624    IN      SOA     b.in-addr-servers.arpa. nstld.iana.org. 2022090341 1800 900 604800 3600

;; Query time: 29 msec
;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
```

# IV. Wireshark

**Wireshark est un outil qui permet de visualiser toutes les trames qui sortent et entrent d'une carte réseau.**

On appelle ça un **sniffer**, ou **analyseur de trames.**

![Wireshark](./pics/wireshark.jpg)

Il peut :

- enregistrer le trafic réseau, pour l'analyser plus tard
- afficher le trafic réseau en temps réel

**On peut TOUT voir.**

Un peu austère aux premiers abords, une manipulation très basique permet d'avoir une très bonne compréhension de ce qu'il se passe réellement.

➜ **[Téléchargez l'outil Wireshark](https://www.wireshark.org/).**

🌞 Utilisez le pour observer les trames qui circulent entre vos deux carte Ethernet. Mettez en évidence :

- un `ping` entre vous et votre passerelle
- un `netcat` entre vous et votre mate, branché en RJ45
- une requête DNS. Identifiez dans la capture le serveur DNS à qui vous posez la question.
- prenez moi des screens des trames en question
- on va prendre l'habitude d'utiliser Wireshark souvent dans les cours, pour visualiser ce qu'il se passe

# Bilan

**Vu pendant le TP :**

- visualisation de vos interfaces réseau (en GUI et en CLI)
- extraction des informations IP
  - adresse IP et masque
  - calcul autour de IP : adresse de réseau, etc.
- connaissances autour de/aperçu de :
  - un outil de diagnostic simple : `ping`
  - un outil de scan réseau : `nmap`
  - un outil qui permet d'établir des connexions "simples" (on y reviendra) : `netcat`
  - un outil pour faire des requêtes DNS : `nslookup` ou `dig`
  - un outil d'analyse de trafic : `wireshark`
- manipulation simple de vos firewalls

**Conclusion :**

- Pour permettre à un ordinateur d'être connecté en réseau, il lui faut **une liaison physique** (par câble ou par *WiFi*).  
- Pour réceptionner ce lien physique, l'ordinateur a besoin d'**une carte réseau**. La carte réseau porte une adresse MAC  
- **Pour être membre d'un réseau particulier, une carte réseau peut porter une adresse IP.**
Si deux ordinateurs reliés physiquement possèdent une adresse IP dans le même réseau, alors ils peuvent communiquer.  
- **Un ordintateur qui possède plusieurs cartes réseau** peut réceptionner du trafic sur l'une d'entre elles, et le balancer sur l'autre, servant ainsi de "pivot". Cet ordinateur **est appelé routeur**.
- Il existe dans la plupart des réseaux, certains équipements ayant un rôle particulier :
  - un équipement appelé *passerelle*. C'est un routeur, et il nous permet de sortir du réseau actuel, pour en joindre un autre, comme Internet par exemple
  - un équipement qui agit comme **serveur DNS** : il nous permet de connaître les IP derrière des noms de domaine
  - un équipement qui agit comme **serveur DHCP** : il donne automatiquement des IP aux clients qui rejoigne le réseau
  - **chez vous, c'est votre Box qui fait les trois :)**