import numpy as np
import os
from threading import Timer

#Seed global
np.random.seed (5)

#Cabecalho
print ("Timestamp,IpOri,PortaOri,IpDest,PortaDest,?,Tempo,BitsEnv,Banda,Jitter,PctPerdido,PctEnv,%Perda,ForaOrdem")

def ping(id):
    #os.system("ping 10.1.0.1 -c 5 >> ping_%d.txt" % (id))
    print("ping 10.1.0.1 -c 5 >> ping_%d.txt" % (id))
    t = Timer(10, ping, [id+1])
    t.start()

def executa(comando):
    #os.system(comando)
    print (comando)

def valorExponencial (media):
    return int(np.random.exponential(media))

def valorNormal (media, desvio):
    return int(np.random.normal(media, desvio))

if __name__ == "__main__":
    porta = 5001
    ipserver = '10.1.0.1'
    ipcliente = '10.1.0.2'
    for i in range (10):
        portacliente = str(porta+500)
        duracao = '10'
        banda = str(valorNormal(700,150))
        if (int(portacliente) % 2 == 0):
            unidade = 'Mbits/sec'
        else:
            unidade = 'Kbits/sec'
        cmd = ('iperf -u -c %s --bind %s:%s -p %s -b %s%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
        tempo = valorExponencial(10)
        print ('Executando em %d segundos, banda %s%s' % (tempo, banda, unidade))
        t = Timer(tempo, executa, [cmd])
        t.start() # Executa depois do tempo
        porta += 1
    #Inicia o ping apos 5 segundos
    t = Timer(5, ping, [1])
    t.start()
