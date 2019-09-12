import numpy as np
import os
from threading import Timer

#Seed global
np.random.seed (10)

#Cabecalho
print ("Timestamp,IpOri,PortaOri,IpDest,PortaDest,?,Tempo,BitsEnv,Banda,Jitter,PctPerdido,PctEnv,%Perda,ForaOrdem")

def ping():
    #Ping na porta par
    os.system("./udpping.py 10.1.0.1 7000 65534 >> pingSW.txt &")
    #Ping na porta impar
    os.system("./udpping.py 10.1.0.1 7001 65535 >> pingHW.txt &")

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

#Portas
porta = 5001
portacliente = porta+500
#IPs
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
#Arquivo para salvar os dados dos iperfs
f = open("iperfs.txt","w+")
f.write("Inicio(seg) Duracao(seg) Banda(Kbps) PortaCli PortaServ\n")
#Inicia o ping
ping()
#Inicia os iperfs
for i in range (200): #Quantos iperfs vao ser gerados
    duracao = valorNormal(90,30) #Duracao
    banda = valorExponencial(3000) #Tamanho de cada iperf
    unidade = 'Kbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%d -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(15) #Tempo ate o inicio
    t = Timer(tempo, executa, [cmd])
    t.start() # Executa depois do tempo
    porta += 1
    portacliente += 1
    f.write("%d %d %d %d %d\n" % (tempo, duracao, banda, portacliente, porta)) #Escreve os dados no arquivo
#Fecha o arquivo dos iperfs
f.close()