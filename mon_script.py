#!/usr/bin/python
# coding: utf8
import re,sys,commands

# Afin de réagir en cas de campagne de SPAM sur les commentaires de votre site web, 
# mettez en place une sonde permettant de remonter une alerte "warning" dès que 4 commentaires 
# ou plus ont été postés dans les 4 dernières heures, 
# une alerte "critical" dès que 10 commentaires 
# ou plus ont été postés dans les 4 dernières heures.

# On va demander à Nagios de se connecter à la machine distante (svcrobotics.com) 
# soit le serveur web hébergent notre WordPress grace à l'instruction check_by_ssh 
# puis une fois sur la machine distante, nous allons éxécuter le plugin check_log 
# (il faut au préalable installer les plugins Nagios sur la machine distante)
# Ce plugin a besoin que l'on lui fournisse un fichier de log à analyser,
# il fait une copie du fichier original (oldlog) puis il cherche l'expression 
# 'POST /wp-comments-post.php HTTP/1.1'
# -w 9 veut dire en dessous de 9 afficher WARNING au dessus afficher CRITICAL
# -p 22 port ssh

command = "/usr/local/nagios/libexec/check_by_ssh -H svcrobotics.com -C '/usr/local/nagios/libexec/check_log -F /var/log/apache2/access.log -O oldlog -q 'POST /wp-comments-post.php HTTP/1.1' -w 9' -p 22"

#Determine state to pass to Nagios
#CRITICAL = 2
#WARNING = 1
#OK = 0

# On exécute la comande "command" et on récupere le resultat sous forme d'un "tuple"
# soit une suite de données immuables séparer par des virgules
# exemple: (0, 'Log check ok - 0 pattern matches found|match=0;;;0')
result = commands.getstatusoutput(command)

# On va "search" l'expression "match=0;;;0" dans le tuple à l'index 1
# c'est à dire dans 'Log check ok - 0 pattern matches found|match=0;;;0'
# le premier zero dans match=0 veut dire aucun POST trouvé
# Les résulats seront stocké sous forme de boolean True or False
result0 = bool(re.search("match=0;;;0", result[1]))
result1 = bool(re.search("match=1;;;0", result[1]))
result2 = bool(re.search("match=2;;;0", result[1]))
result3 = bool(re.search("match=3;;;0", result[1]))
result4 = bool(re.search("match=4;;;0", result[1]))
result5 = bool(re.search("match=5;;;0", result[1]))
result6 = bool(re.search("match=6;;;0", result[1]))
result7 = bool(re.search("match=7;;;0", result[1]))
result8 = bool(re.search("match=8;;;0", result[1]))
result9 = bool(re.search("match=9;;;0", result[1]))


# Si un de ces résultats est True alors afficher dans l'interface web de Nagios
# de 0 à 3 commentaires en moins de 4 heures Nagios affichera OK
if result0 or result1 or result2 or result3:
    print("OK:")
    print("moins de 4 commentaires") 
    print("ces 4 dernières heures.")
    sys.exit(0)
# de 4 à 9 commentaires en moins de 4 heures Nagios affichera WARNING
elif result4 or result5 or result6 or result7 or result8 or result9:
    print("WARNING")
    print("entre 4 et 9 commentaires")
    print("ces 4 dernières heures.")
    sys.exit(1)
# 10 ou plus Nagios affichera CRITICAL
else:
    print("CRITICAL")
    print("plus de 10 commentaires")
    print("ces 4 dernières heures.")
    sys.exit(2)

