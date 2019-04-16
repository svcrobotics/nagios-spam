# Nagios SPAM

Afin de réagir en cas de campagne de SPAM sur les commentaires de votre site web, 
mettez en place une sonde permettant de remonter une alerte "warning" dès que 4 commentaires ou plus ont été postés dans les 4 dernières heures, 
une alerte "critical" dès que 10 commentaires ou plus ont été postés dans les 4 dernières heures.

## Mise en place

récuperer le fichier mon_script.py et placer le dans le répertoire des scripts Nagios
dans mon cas de figure une Debian based, il sagit du répertoire /usr/local/nagios/libexec/ 

puis il vous faudra definir:

## command

```
define command {
	command_name wordpress
	command_line $USER1$/mon_script.py
}
```

## service

```
define service {
    service_description WordPress Comments
    host_name WordPress Server
    check_command wordpress
    max_check_attempts 3
    check_period 24x7
    notification_period 24x7
    check_interval 240
}
```

Vous devrez modifier le host_name  est mettre le nom de votre serveur web, check_interval est ici configuré sur 4 heures.