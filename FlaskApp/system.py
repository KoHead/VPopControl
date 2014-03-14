# -*- coding: utf-8 -*-
import os
import os.path
import subprocess
import crypt
from os.path import join, getsize
liste_dir = []
dovecot_mailbox_path="/home/dovecot/"

def return_listdir():
  """
  Retourne une liste des repertoires contenu dans dovecot_mailbox_path ainsi que leur taille
  """
  for filename in os.listdir(dovecot_mailbox_path):
    name_sub_dir=dovecot_mailbox_path+filename
    try:
        size = subprocess.Popen(['du', '-hs', name_sub_dir],stdout=subprocess.PIPE).communicate()[0].split()[0]
    except:
        size = "Recuperation valeur impossible"
    liste_dir.append(name_sub_dir)
    liste_dir.append(size)
  return liste_dir

def delete_mailbox(mailbox_name):
  """
  Prend en parametre le nom d une mailbox et supprime le contenu du repertoire MailDir correspondant
  """
  path_mailbox="/home/dovecot/%s/Maildir/" % (mailbox_name)
  try:
    command="sudo rm -rf %s*" % (path_mailbox)
    os.system(command)
  except:
    return "impossible de supprimer %s" % (name)

  return "La boite mail %s a bien ete supprimee" % (mailbox_name)

def create_mailbox(mailbox_name):
    """
    Créer une boite mail en prenant en paramètre mailbox_name
    """
    try:
        username=mailbox_name.split('@', 1 )[0];
        domaine=mailbox_name.split('@', 2 )[1];
        os.system("echo -e %s \"\t\"%s >> /etc/postfix/virtual" % (mailbox_name,username))
        os.system("sudo /usr/sbin/postmap /etc/postfix/virtual")
        os.system("sudo /etc/init.d/postfix restart")
        password = "W5t0XR6KhJ"
        encPass = crypt.crypt(password,"22")
        subprocess_line="/home/dovecot/%s" % username
        sub = subprocess.Popen(['sudo', '/usr/sbin/useradd', '-d', subprocess_line, '-m', '-s', '/sbin/false', username, '-p', encPass, '--gid', 'apache'])
        #os.system("sudo /bin/chmod -R 775 /home/dovecot/%s" % (username))
        return "La boite mail %s a bien ete cree" % (mailbox_name)
    except:
        return "La boite mail %s n'a pas pu etre cree" % (mailbox_name)

def create_domain(domain_name):
    """
    Créer un domaine en prenant en paramètre domain_name
    """
    try:
        subprocess_line="s/^virtual_alias_domains =/& %s/" % domain_name
        sub = subprocess.Popen(['sed', '-i', subprocess_line, "/etc/postfix/main.cf"],
        stdout=subprocess.PIPE).communicate()
        os.system("/etc/init.d/postfix restart")
        return "Le domaine %s a bien ete cree" % domain_name
    except:
        return "La domaine %s n'a pas pu etre cree" % (mailbox_name)

