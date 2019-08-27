import numpy as np
import os
from threading import Timer

#Seed global
np.random.seed (10)

#Cabecalho
print ("Timestamp,IpOri,PortaOri,IpDest,PortaDest,?,Tempo,BitsEnv,Banda,Jitter,PctPerdido,PctEnv,%Perda,ForaOrdem")

def ping():
    os.system("ping 10.1.0.1 -c 5 >> ping.txt")
    #print("ping 10.1.0.1 -c 5 >> ping.txt")
    t = Timer(10, ping)
    t.start()

def executa(comando):
    os.system(comando)
    #print (comando)

def valorExponencial (media):
    x = int(np.random.exponential(media))
    return x if x>0 else valorExponencial(media)

def valorNormal (media, desvio):
    x = int(np.random.normal(media, desvio))
    return x if x>0 else valorNormal(media,desvio)

porta = 5001
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
for i in range (100):
    portacliente = str(porta+500)
    duracao = '10'
    numeroBytes = valorNormal(600,500)
    numeroPacotes = valorExponencial(100)
    banda = (numeroBytes * numeroPacotes)/125
    #banda = valorNormal(bandaTotal, 500)
    unidade = 'Mbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%s -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(30)
    #print ('Executando em %d segundos, banda %d%s, bytes %d, pacotes %d' % (tempo, banda, unidade, numeroBytes, numeroPacotes))
    t = Timer(tempo, executa, [cmd])
    t.start() # Executa depois do tempo
    porta += 1

#Inicia o ping apos 5 segundos
t = Timer(5, ping)
t.start()
