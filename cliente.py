import numpy as np
import os
from threading import Timer
import signal
import subprocess

#Seed global
seed = 10
np.random.seed (seed)

#Cabecalho
print ("Timestamp,IpOri,PortaOri,IpDest,PortaDest,?,Tempo,BitsEnv,Banda,Jitter,PctPerdido,PctEnv,%Perda,ForaOrdem")

def pingSW():
    #Ping na porta par
    f = open("pingSW.txt", "w")
    p1 = subprocess.Popen(["./udpping.py", "10.1.0.1", "7000", "65534"], stdout=f)
    f.close()
    return p1.pid

def pingHW():
    #Ping na porta impar
    f = open("pingHW.txt", "w")
    p2 = subprocess.Popen(["./udpping.py", "10.1.0.1", "7001", "65535"], stdout=f)
    f.close()
    return p2.pid

def killPing(id1, id2):
    os.kill(id1, signal.SIGINT)
    os.kill(id2, signal.SIGINT)

def executa(comando):
    os.system(comando)
    #print (comando)

def valorExponencial (media):
    x = int(np.random.exponential(media))
    if x > 0:
        return x
    else:
        return 0

def valorNormal (media, desvio):
    x = int(np.random.normal(media, desvio))
    if x > 0:
        return x
    else:
        return 0

#Portas
porta = 5001
portacliente = 3501
#IPs
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
#Informacoes do iperf
baseDuracao = 90
desvioDuracao = 30
quantidade = 1000
mediaBanda = 1910
mediaTempoInicio = 15
metodo = "Par/Impar"
#metodo = "SW->HW"
f = open("info.txt","w+")
f.write("Metodo: %s\nSeed: %d\nQuant: %d\nDuracao(base): %d\nDuracao(desvio): %d\nBanda(media): %d\nTempoIni(media): %d\n" % (metodo, seed, quantidade, baseDuracao, desvioDuracao, mediaBanda, mediaTempoInicio))
f.close()
#Arquivo para salvar os dados dos iperfs
f = open("iperfs.txt","w+")
f.write("Inicio(seg) Duracao(seg) Banda(Kbps) PortaCli PortaServ\n")
#Inicia o ping
idP1 = pingSW()
idP2 = pingHW()
maiorDuracao = 0
#Inicia os iperfs
for i in range (quantidade): #Quantos iperfs vao ser gerados
    duracao = valorNormal(baseDuracao,desvioDuracao) #Duracao
    banda = valorExponencial(mediaBanda) #Tamanho de cada iperf
    unidade = 'Kbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%d -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(mediaTempoInicio) #Tempo ate o inicio
    t = Timer(tempo, executa, [cmd])
    t.start() # Executa depois do tempo
    f.write("%d %d %d %d %d\n" % (tempo, duracao, banda, portacliente, porta)) #Escreve os dados no arquivo
    porta += 1
    portacliente += 1
    soma = duracao+tempo
    if (soma > maiorDuracao):
        maiorDuracao = soma
#Fecha o arquivo dos iperfs
f.close()
#Fecha os pings depois do maior tempo de duracao de iperf
tp = Timer(maiorDuracao+3, killPing, [idP1, idP2])
tp.start()
