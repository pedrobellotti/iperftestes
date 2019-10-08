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
    x = float(np.random.exponential(media))
    if x >= 0:
        return x
    else:
        return valorExponencial(media)

def valorNormal (media, desvio):
    x = float(np.random.normal(media, desvio))
    if x >= 0:
        return x
    else:
        return valorNormal(media,desvio)

def valorUniforme (min, max):
    return float(np.random.uniform(min,max))

#Portas
porta = 4001
portacliente = 8501
#IPs
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
#Informacoes do iperf
minDuracao = 5.0
maxDuracao = 100.0
quantidade = 500
mediaBanda = 1910.0
mediaTempoInicio = 0.5
metodo = "Par/Impar"
#metodo = "SW->HW"
f = open("info.txt","w+")
f.write("Metodo: %s\nSeed: %d\nQuant: %d\nDuracao(min): %d\nDuracao(max): %d\nBanda(media): %d\nTempoIni(media): %d\n" % (metodo, seed, quantidade, minDuracao, maxDuracao, mediaBanda, mediaTempoInicio))
f.close()
#Arquivo para salvar os dados dos iperfs
f = open("iperfs.txt","w+")
f.write("Inicio(seg)\tDuracao(seg)\tBanda(Kbps)\tPCli\tPServ\n")
#Inicia o ping
idP1 = pingSW()
idP2 = pingHW()
maiorDuracao = 0.0
tempoSoma = 0.0
#Inicia os iperfs
for i in range (quantidade): #Quantos iperfs vao ser gerados
    duracao = valorUniforme(minDuracao,maxDuracao) #Duracao
    banda = valorExponencial(mediaBanda) #Tamanho de cada iperf
    unidade = 'Kbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%d -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(mediaTempoInicio) #Tempo ate o inicio
    tempoSoma += tempo
    t = Timer(tempoSoma, executa, [cmd])
    t.start() # Executa depois do tempo
    f.write("%f\t%f\t%f\t%d\t%d\n" % (tempoSoma, duracao, banda, portacliente, porta)) #Escreve os dados no arquivo
    porta += 1
    portacliente += 1
    soma = duracao+tempoSoma
    if (soma > maiorDuracao):
        maiorDuracao = soma
#Fecha o arquivo dos iperfs
f.write("Maior duracao (segundos): %d" % (maiorDuracao))
f.close()
#Fecha os pings depois do maior tempo de duracao de iperf
tp = Timer(maiorDuracao+3, killPing, [idP1, idP2])
tp.start()
