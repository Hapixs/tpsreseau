


```bash
[hd0@node1 ~]$ sudo systemctl status sshd
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-01-02 18:06:27 CET; 1min 28s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 689 (sshd)
      Tasks: 1 (limit: 5905)
     Memory: 5.6M
        CPU: 548ms
     CGroup: /system.slice/sshd.service
             └─689 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
[...]
```


```bash
[hd0@node1 ~]$ sudo ps -axf | grep sshd
    689 ?        Ss     0:00 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
    859 ?        Ss     0:00  \_ sshd: hd0 [priv]
    863 ?        S      0:00      \_ sshd: hd0@pts/0
   1157 pts/0    S+     0:00              \_ grep --color=auto sshd
```


```bash
[hd0@node1 ~]$ sudo ss -petn | grep ssh
ESTAB 0      0       192.168.56.8:22   192.168.56.4:48682 users:(("sshd",pid=863,fd=4),("sshd",pid=859,fd=4)) timer:(keepalive,103min,0) ino:19442 sk:2a cgroup:/system.slice/sshd.service <->
```

```bash 
[hd0@node1 ~]$ sudo journalctl | tail
Jan 02 18:27:22 node1.tp2.linux sudo[1217]: pam_unix(sudo:session): session opened for user root(uid=0) by hd0(uid=1000)
Jan 02 18:27:23 node1.tp2.linux sudo[1217]: pam_unix(sudo:session): session closed for user root
Jan 02 18:27:30 node1.tp2.linux sudo[1220]:      hd0 : TTY=pts/0 ; PWD=/home/hd0 ; USER=root ; COMMAND=/bin/ls -la /var/log/private/
Jan 02 18:27:30 node1.tp2.linux sudo[1220]: pam_unix(sudo:session): session opened for user root(uid=0) by hd0(uid=1000)
Jan 02 18:27:30 node1.tp2.linux sudo[1220]: pam_unix(sudo:session): session closed for user root
Jan 02 18:29:34 node1.tp2.linux sudo[1246]:      hd0 : TTY=pts/0 ; PWD=/home/hd0 ; USER=root ; COMMAND=/bin/journalctl
Jan 02 18:29:34 node1.tp2.linux sudo[1246]: pam_unix(sudo:session): session opened for user root(uid=0) by hd0(uid=1000)
Jan 02 18:29:42 node1.tp2.linux sudo[1246]: pam_unix(sudo:session): session closed for user root
Jan 02 18:29:46 node1.tp2.linux sudo[1250]:      hd0 : TTY=pts/0 ; PWD=/home/hd0 ; USER=root ; COMMAND=/bin/journalctl
Jan 02 18:29:46 node1.tp2.linux sudo[1250]: pam_unix(sudo:session): session opened for user root(uid=0) by hd0(uid=1000)
```

```bash
[hd0@node1 ~]$ sudo cat /etc/ssh/sshd_config | grep Port
Port 53
```

```bash
[hd0@node1 ~]$ sudo firewall-cmd --add-port=53/tcp
success
[hd0@node1 ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s8 enp0s9
  sources: 
  services: cockpit dhcpv6-client ssh
  ports: 53/tcp
  [...]
```

// TODO: ssh conf
// TODO: HTTP 