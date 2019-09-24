import numpy as np
import os
from threading import Timer

#Seed global
seed = 10
np.random.seed (seed)

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
portacliente = porta+500
#IPs
ipserver = '10.1.0.1'
ipcliente = '10.1.0.2'
#Informacoes do iperf
baseDuracao = 90
desvioDuracao = 30
quantidade = 320
mediaBanda = 1910
mediaTempoInicio = 15
#metodo = "Par/Impar"
metodo = "SW->HW"
f = open("info.txt","w+")
f.write("Metodo: %s\nSeed: %d\nQuant: %d\nDuracao(base):%d\nDuracao(desvio): %d\nBanda(media): %d\nTempoIni(media): %d\n" % (metodo, seed, quantidade, baseDuracao, desvioDuracao, mediaBanda, mediaTempoInicio))
f.close()
#Arquivo para salvar os dados dos iperfs
f = open("iperfs.txt","w+")
f.write("Inicio(seg) Duracao(seg) Banda(Kbps) PortaCli PortaServ\n")
#Inicia o ping
ping()
#Inicia os iperfs
for i in range (quantidade): #Quantos iperfs vao ser gerados
    duracao = valorNormal(baseDuracao,desvioDuracao) #Duracao
    banda = valorExponencial(mediaBanda) #Tamanho de cada iperf
    unidade = 'Kbits/sec'
    cmd = ('iperf -u -c %s --bind %s:%d -p %s -b %d%s -t %s -y C &' % (ipserver, ipcliente, portacliente, porta, banda, unidade, duracao))
    tempo = valorExponencial(mediaTempoInicio) #Tempo ate o inicio
    t = Timer(tempo, executa, [cmd])
    t.start() # Executa depois do tempo
    porta += 1
    portacliente += 1
    f.write("%d %d %d %d %d\n" % (tempo, duracao, banda, portacliente, porta)) #Escreve os dados no arquivo
#Fecha o arquivo dos iperfs
f.close()