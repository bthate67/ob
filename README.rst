README
######

Welcome to OBOT,

OBOT is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel, it can be used to display RSS feeds,
act as a UDP to IRC relay and you can program your own commands for it.

installation is through pypi, use the superuser (sudo)::

 $ pip3 install obot 
 $ cp /usr/local/share/obot/obot.service /etc/systemd/system
 $ systemctl enable obot
 $ systemctl start obot

basic channel/server is #obot on localhost.

OBOT is placed in the Public Domain and has no COPYRIGHT and no LICENSE.

configure
=========

configuration is done with the octl (object control) program, also with sudo::

 $ octl cfg server=botd.io channel=\#obot nick=obot
 ok

if the users option is set in the irc config then users need to be added 
before they can give commands, use the met command to introduce a user::

 $ octl met ~botfather@jsonbot/daddy
 ok

restart the service to take changes into effect::

 $ systemctl restart obot

rss
===

with the use of feedparser you canserve rss feeds in your channel (sudo)::

 $ apt install python3-feedparser

add an url use the rss command with an url::

 $ octl rss https://github.com/bthate/obot/commits/master.atom
 ok

run the fnd (find) command to see what urls are registered::

 $ octl fnd rss
 0 https://github.com/bthate/obot/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds::

 $ octl ftc
 fetched 20

programming
===========

olib modules provides a library you can use to program objects under python3.
It provides a basic BigO Object, that mimics a dict while using attribute access
and provides a save/load to/from json files on disk. Objects can be searched
with a little database module, it uses read-only files to improve persistence
and a type in filename for reconstruction.

basic usage is this::

 >>> from obj import Object
 >>> o = Object()
 >>> o.key = "value"
 >>> o.key
 'value'

objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided as are the basic
methods like get, items, keys, register, set, update, values.

the bot.obj module has the basic methods like load and save as a object
function using an obj as the first argument::

 >>> from obj import Object, cfg
 >>> cfg.wd = "data"
 >>> o = Object()
 >>> o["key"] = "value"
 >>> p = o.save()
 >>> p
 'obj.Object/4b58abe2-3757-48d4-986b-d0857208dd96/2021-04-12/21:15:33.734994
 >>> oo = Object()
 >>> oo.load(p)
 >> oo.key
 'value'

great for giving objects peristence by having their state stored in files.

modules
=======

OBOT's modules are pure python3 modules you can use to program objects
with, uses a JSON in file database with a versioned readonly storage and
reconstructs objects based on type information in the path.

the following modules are provided::

    all            - all modules
    bus            - list of bots
    cfg            - configuration
    clk            - clock/repeater
    clt            - client
    cmd            - command
    cms            - commands
    dbs            - database
    dft            - default
    evt            - event
    hdl            - handler
    irc            - internet relay chat
    krn            - kernel
    lst            - dict of lists
    obj            - objects
    opt            - output
    prs            - parsing
    thr            - threads
    adm            - administrator
    fnd            - find
    log            - log items
    rss            - rich site syndicate
    tdo            - todo items
    udp            - UDP to IRC relay

commands
========

modules are not read from a directory, instead you must include your own
written commands with a updated version of the code. First clone the
repository (as user)::

 $ git clone http://github.com/bthate67/obot
 $ cd obot
 
to program your own commands, open olib/hlo.py (new file) and add the following
code::

    def register(k):
        k.regcmd(hlo)

    def hlo(event):
        event.reply("hello %s" % event.origin)

add the hlo module to the olib/all.py module::

    import hlo

    Kernel.addmod(hlo)

edit the list of modules to load in bin/botd::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,hlo"

then install with python3 (using sudo)::

 $ python3 setup.py install
 $ python3 setup.py install_data

reload the systemd service::

 $ systemctl stop obot
 $ systemctl start obot

now you can type the "hlo" command, showing hello <user>::

 <bart> !hlo
 hello root@console

udp
===

there is also the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed in the channel.
output to the IRC channel is done with the use python3 code to send a UDP
packet to OBOT, it's unencrypted txt send to the bot and displayed in the
joined channels::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

to have the udp relay running, add udp to the all variable in bin/botd::

    all = "adm,cms,fnd,irc,krn,log,rss,tdo,udp"

contact
=======

"contributed back"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots irc.freenode.net


.. toctree::
    :hidden:
    :glob:

    *
