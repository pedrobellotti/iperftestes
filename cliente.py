import numpy as np
import os
from threading import Timer

#Seed global
np.random.seed (10)

#Cabecalho
print ("Timestamp,IpOri,PortaOri,IpDest,PortaDest,?,Tempo,BitsEnv,Banda,Jitter,PctPerdido,PctEnv,%Perda,ForaOrdem")

def ping():
    #Ping na porta par
    os.system("./udpping.py 10.1.0.1 7000 65534 >> pingpar.txt &")
    #Ping na porta impar
    os.system("./udpping.py 10.1.0.1 7001 65535 >> pingimpar.txt &")

def executa(comando):
    os.system(comando)
    #print (comando)

def valorExponencial (media):
    x = int(np.random.exponential(media))
    #return x if x>0 else valorExponencial(media)
    if x > 0:
        return x
    else:
        return 0

def valorNormal (media, desvio):
    x = int(np.random.normal(media, desvio))
    #return x if x>0 else valorNormal(media,desvio)
    if x > 0:
        return x
    else:
        return 0

porta = 5001
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
#Inicia o ping
ping()
#Inicia os iperfs
for i in range (100): #Aumentar
    portacliente = str(porta+500)
    duracao = valorNormal(90,30)
    banda = valorExponencial(10000) #Diminuir
    unidade = 'Kbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%s -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(30) #Diminuir
    #print ('Executando em %d segundos, banda %d%s, bytes %d, pacotes %d' % (tempo, banda, unidade, numeroBytes, numeroPacotes))
    t = Timer(tempo, executa, [cmd])
    t.start() # Executa depois do tempo
    porta += 1