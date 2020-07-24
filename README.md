# Sistema di controllo wireless e monitoraggio remoto di un dispositivo IoT Linux-based
## Autori: Paula Mihalcea, Abdullah Chaudhry
#### Università degli Studi di Firenze - Corso di Laurea Magistrale in Ingegneria Informatica

---

![](https://img.shields.io/github/contributors/chabdullah/Lego-Ev3-Python?color=light%20green) ![](https://img.shields.io/github/repo-size/chabdullah/Lego-ev3-Python)

![](https://img.shields.io/github/size/chabdullah/lego-ev3-python/client.py?color=light%20green&label=client%20script%20size) ![](https://img.shields.io/github/size/chabdullah/lego-ev3-python/server.py?color=light%20green&label=server%20script%20size)

Questo progetto realizza un **sistema di controllo remoto** atto a guidare a distanza un dispositivo di tipo **IoT Linux-based** attraverso un **gamepad**, in modo intuitivo ed efficiente. L’implementazione presentata all’esame in oggetto lo applica ad un robot **LEGO MINDSTORMS EV3** (estensivamente studiato ai fini del progetto), ma per la sua natura modulare ed il codice ben strutturato può essere **facilmente riadattata ad un qualunque dispositivo IoT** basato su Linux ed in grado di collegarsi in modo wireless ad una rete locale, **anche – e soprattutto - a bassa potenza di calcolo**.

Il codice sorgente qui presente include:

- `Programmazione Python di un dispositivo
LEGO MINDSTORMS EV3.pdf`, la documentazione esaustiva presentata in sede d'esame durante la discussione del progetto nell'ambito del corso di _Laboratory of Automatic Control_ con il prof. Michele Basso;
- `client.py` e `server.py`, i due programmi principali del sistema di controllo remoto;
- `auto_nav_micro.py` e `auto_nav_python.py`, due script di navigazione autonoma ideati per confrontare le prestazioni dei due sistemi operativi supportati dal robot ([LEGO MINDSTORMS EV3 MicroPython](https://education.lego.com/en-us/downloads/mindstorms-ev3/software#MicroPython) ed [ev3dev](https://www.ev3dev.org));
- `plot.py`, uno script per la generazione di grafici a partire dai dati di logging, assieme ad alcuni plot esemplificativi da esso creati (cartella `plots`);
- `log.json`, un file di log di esempio;
- `demo.mp4`, un breve video dimostrativo realizzato durante lo sviluppo del progetto in laboratorio.

Il sistema si avvale delle librerie [SocketServer](https://docs.python.org/3/library/socketserver.html) e [inputs](https://pypi.org/project/inputs/).
