from iqoptionapi.stable_api import IQ_Option
from configparser import ConfigParser
import time
from datetime import datetime
from dateutil import tz
from colorama import init, Fore, Back
import sys


def timestamp_converter(x): 
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora.astimezone(tz.gettz('America/Sao Paulo')))[:-6]

def paridadesAbertas():
    global API
    par = API.get_all_open_time()
    for paridade in par['digital']:
        if par['digital'][paridade]['open'] == True:
            print(paridade)

def mhiMinoria(par,winrate):
    global API
    nome = '  MHI - Minoria  '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                    qtdDogi += 1

                elif (corVelas[i] == 'vermelho' and direcao == 'put' ) or (corVelas[i] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+1)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+1)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))
    
    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')
    
def mhiMaioria(par,winrate):
    global API
    nome = '  MHI - Maioria  '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])

    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            
            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('dogi') > 0 : 
                direcao = ''

            try:   
                if direcao == '': 
                    qtdDogi += 1
                elif (corVelas[i] == 'vermelho' and direcao == 'put' ) or (corVelas[i] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+1)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+1)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def mhi2Minoria(par,winrate):
    global API
    nome = ' MHI 2 - Minoria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i]) 

    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                    qtdDogi += 1

                elif (corVelas[i+1] == 'vermelho' and direcao == 'put' ) or (corVelas[i+1] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+3)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+3)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def mhi2Maioria(par,winrate):
    global API
    nome = ' MHI 2 - Maioria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                    qtdDogi += 1

                elif (corVelas[i+1] == 'vermelho' and direcao == 'put' ) or (corVelas[i+1] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+3)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+3)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def mhi3Minoria(par,winrate):
    global API
    nome = ' MHI 3 - Minoria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('dogi') > 0 : 
                direcao = ''

            try:   
                if direcao == '': 
                    qtdDogi += 1
                elif (corVelas[i+2] == 'vermelho' and direcao == 'put' ) or (corVelas[i+2] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+3)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+3)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+4)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+4)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def mhi3Maioria(par,winrate):
    global API
    nome = ' MHI 3 - Maioria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
           
            cores = corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('dogi') > 0 : 
                direcao = ''

            try:   
                if direcao == '': 
                    qtdDogi += 1

                elif (corVelas[i+2] == 'vermelho' and direcao == 'put' ) or (corVelas[i+2] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+3)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+3)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+4)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+4)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padrao23(par,winrate):
    global API
    nome = '    Padrão 23    '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            try:   
                if corVelas[i] == 'dogi': 
                    qtdDogi += 1

                elif (corVelas[i+1] == 'vermelho' and corVelas[i] == 'vermelho') or (corVelas[i+1] == 'verde' and corVelas[i] == 'verde' ) : 
                    mf += 1
                elif (corVelas[i+2] == 'vermelho' and corVelas[i] == 'vermelho') or (corVelas[i+2] == 'verde' and corVelas[i] == 'verde' ) :
                    mg1 += 1
                elif (corVelas[i+3] == 'vermelho' and corVelas[i] == 'vermelho') or (corVelas[i+3] == 'verde' and corVelas[i] == 'verde' ) :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def milhaoMinoria(par,winrate):
    global API
    nome = 'Milhão - Minoria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-5]  + ' / ' + corVelas[i-4]  + ' / ' + corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  


            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                    qtdDogi += 1
                elif (corVelas[i] == 'vermelho' and direcao == 'put' ) or (corVelas[i] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+1)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+1)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def milhaoMaioria(par,winrate):
    global API
    nome = 'Milhão - Maioria '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
           
            cores = corVelas[i-5]  + ' / ' + corVelas[i-4]  + ' / ' + corVelas[i-3]  + ' / ' + corVelas[i-2]  + ' / ' + corVelas[i-1]  


            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                    qtdDogi += 1
                elif (corVelas[i] == 'vermelho' and direcao == 'put' ) or (corVelas[i] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+1)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+1)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+2)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+2)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def melhorDe3(par,winrate):
    global API
    nome = '   Melhor de 3   '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:

            cores = corVelas[i-4]  + ' / ' + corVelas[i-3]  + ' / ' + corVelas[i-2]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('dogi') > 0 : 
                direcao = ''

            try:   
                if direcao == '': 
                    qtdDogi += 1
                elif (corVelas[i+2] == 'vermelho' and direcao == 'put' ) or (corVelas[i+2] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[int(i+3)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+3)] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[int(i+4)] == 'vermelho' and direcao == 'put' ) or (corVelas[int(i+4)] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def torreGemeas(par,winrate):
    global API
    nome = '   Torre Gêmeas  '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            try:   
                if corVelas[i-5] == 'dogi': 
                    qtdDogi += 1
                elif (corVelas[i-1] == 'vermelho' and corVelas[i-5] == 'vermelho') or (corVelas[i-1] == 'verde' and corVelas[i-5] == 'verde') : 
                    mf += 1
                elif (corVelas[i] == 'vermelho' and corVelas[i-5] == 'vermelho') or (corVelas[i] == 'verde' and corVelas[i-5] == 'verde') : 
                    mg1 += 1
                elif (corVelas[i+1] == 'vermelho' and corVelas[i-5] == 'vermelho') or (corVelas[i+1] == 'verde' and corVelas[i-5] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def tresMosqueteiros(par,winrate):
    global API
    nome = 'Três Mosqueteiros'
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            try:   
                if corVelas[i-3] == 'dogi': 
                    qtdDogi += 1
                elif (corVelas[i-2] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i-2] == 'verde' and corVelas[i-3] == 'verde') : 
                    mf += 1
                elif (corVelas[i-1] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i-1] == 'verde' and corVelas[i-3] == 'verde') : 
                    mg1 += 1
                elif (corVelas[i] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i] == 'verde' and corVelas[i-3] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padraoImpar(par,winrate):
    global API
    nome = '   Padrão Ímpar  '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            
            try:   
                if corVelas[i-3] == 'dogi': 
                    qtdDogi += 1
                elif (corVelas[i] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i] == 'verde' and corVelas[i-3] == 'verde') : 
                    mf += 1
                elif (corVelas[i+2] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i+2] == 'verde' and corVelas[i-3] == 'verde') : 
                    mg1 += 1
                elif (corVelas[i+4] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i+4] == 'verde' and corVelas[i-3] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padraoC3(par,winrate):
    global API
    nome = '    Padrão C3    '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
            try:   
                if corVelas[i-5] == 'dogi': 
                    qtdDogi += 1
                elif (corVelas[i] == 'vermelho' and corVelas[i-5] == 'vermelho') or (corVelas[i] == 'verde' and corVelas[i-5] == 'verde') : 
                    mf += 1
                elif (corVelas[i+2] == 'vermelho' and corVelas[i-3] == 'vermelho') or (corVelas[i+2] == 'verde' and corVelas[i-3] == 'verde') : 
                    mg1 += 1
                elif (corVelas[i+4] == 'vermelho' and corVelas[i-1] == 'vermelho') or (corVelas[i+4] == 'verde' and corVelas[i-1] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padrao3x1(par,winrate):
    global API
    nome = '    Padrão 3x1   '
    qtdVela = 120 + (int(datetime.now().strftime('%M'))%5)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%5))):
        if i%5 == 4:
           
            cores = corVelas[i-5]  + ' / ' + corVelas[i-4]  + ' / ' + corVelas[i-3]  

            if cores.count('verde') > cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'put'
            if cores.count('verde') < cores.count('vermelho') and cores.count('dogi') == 0 : direcao = 'call'
            if cores.count('dogi') > 0 : 
                direcao = ''
            
            try:   
                if direcao == '': 
                     qtdDogi += 1
                elif (corVelas[i-1] == 'vermelho' and direcao == 'put' ) or (corVelas[i-1] == 'verde' and direcao == 'call') : 
                    mf += 1
                elif (corVelas[i] == 'vermelho' and direcao == 'put' ) or (corVelas[i] == 'verde' and direcao == 'call') : 
                    mg1 += 1
                elif (corVelas[i+1] == 'vermelho' and direcao == 'put' ) or (corVelas[i+1] == 'verde' and direcao == 'call') : 
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss)),2))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padraoR7(par,winrate):
    global API
    nome = '    Padrão R7    '
    qtdVela = 240 + (int(datetime.now().strftime('%M'))%10)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%10))):
        if i%10 == 9:

            try:   
                if corVelas[i-2] == '': 
                    qtdDogi += 1
                elif (corVelas[i+6] == 'vermelho' and corVelas[i-2] == 'vermelho') or (corVelas[i+6] == 'verde' and corVelas[i-2] == 'verde') : 
                    mf += 1
                elif (corVelas[i+7] == 'vermelho' and corVelas[i-2] == 'vermelho') or (corVelas[i+7] == 'verde' and corVelas[i-2] == 'verde') :
                    mg1 += 1
                elif (corVelas[i+8] == 'vermelho' and corVelas[i-2] == 'vermelho') or (corVelas[i+8] == 'verde' and corVelas[i-2] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')

def padraoSevenWick(par,winrate):
    global API
    nome = 'Padrão Seven Wick'
    qtdVela = 240 + (int(datetime.now().strftime('%M'))%10)
    velas = API.get_candles(par, 60, qtdVela, time.time())
    corVelas = []
    horaVelas = []
    mf = 0
    mg1 = 0
    mg2 = 0
    qtdDogi = 0
    loss = 0
    for i in range(qtdVela):
        horaVelas.append(timestamp_converter(velas[i]['from']))
        velas[i] = 'verde' if velas[i]['open'] < velas[i]['close'] else 'vermelho' if velas[i]['open'] > velas[i]['close'] else 'dogi'
        corVelas.append(velas[i])
    
    for i in range(int(qtdVela - (int(datetime.now().strftime('%M'))%10))):
        if i%10 == 9:
           
            try:   
                if corVelas[i+6] == '': 
                    qtdDogi += 1
                elif (corVelas[i+7] == 'vermelho' and corVelas[i+6] == 'vermelho') or (corVelas[i+7] == 'verde' and corVelas[i+6] == 'verde') : 
                    mf += 1
                elif (corVelas[i+8] == 'vermelho' and corVelas[i+6] == 'vermelho') or (corVelas[i+8] == 'verde' and corVelas[i+6] == 'verde') :
                    mg1 += 1
                elif (corVelas[i+9] == 'vermelho' and corVelas[i+6] == 'vermelho') or (corVelas[i+9] == 'verde' and corVelas[i+6] == 'verde') :
                    mg2 += 1
                else:
                    loss += 1
            except: pass

    winrateMF = float(round(100*((mf)/(mf+mg1+mg2+loss))))
    winrateMG1 = float(round(100*((mf+mg1)/(mf+mg1+mg2+loss))))
    winrateMG2 = float(round(100*((mf+mg1+mg2)/(mf+mg1+mg2+loss))))

    nomePar = par
    if int(len(nomePar)) == 6: nomePar = '  '+nomePar+'  '
    elif int(len(nomePar)) != 6: nomePar = nomePar 
    
    if int(cfg_catalogacao['qtd_martingale']) == 0 and winrateMF >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMF, end='')
        if winrateMF != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 1 and winrateMG1 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG1, end='')
        if winrateMG1 != 100: print ('%      |')
        else: print ('%     |')
    elif int(cfg_catalogacao['qtd_martingale']) == 2 and winrateMG2 >= winrate:
        print('|',nomePar,'|', nome, '|    ',winrateMG2, end='')
        if winrateMG2 != 100: print ('%      |')
        else: print ('%     |')


config = ConfigParser()
config.read('cfg.txt')
cfg_login = dict(config['LOGIN'])
cfg_catalogacao = dict(config['CATALOGACAO'])

API = IQ_Option(cfg_login['login'], cfg_login['senha'])
API.connect()
API.change_balance('PRACTICE')
init(convert=True, autoreset=True)

if API.check_connect():
    
    print(Fore.CYAN+'\n********************************', 'Catalogador Automático', Fore.CYAN +'*************************************\n')
    print(Fore.YELLOW + '->','O status de conexão é :', Fore.GREEN + 'Conectado\n')
    print(Fore.YELLOW + '->','E-mail: ', cfg_login['login'])

    print(Fore.CYAN+'\n*****************************', 'Configurações de Catalogação', Fore.CYAN +'**********************************\n')
    print(Fore.YELLOW + '->','Quantidade de Martingale: ', cfg_catalogacao['qtd_martingale'], '\n')
    print(Fore.YELLOW + '->','Taxa de acerto mínima: ', cfg_catalogacao['winrate'], '%')
        
    # par = API.get_all_open_time()
    # for paridade in par['digital']:
    #     if par['digital'][paridade]['open'] == True:
    #         print(paridade)


    print(Fore.CYAN+'\n*****************************', 'Selecionar Estratégia', Fore.CYAN +'**********************************\n')
    while True:
        while True:
            try:
                print('\nDigite 1', Fore.YELLOW + ' ->','Estratégia MHI - Minoria')
                print('Digite 2', Fore.YELLOW + ' ->','Estratégia MHI - Maioria')
                print('Digite 3', Fore.YELLOW + ' ->','Estratégia MHI 2 - Minoria')
                print('Digite 4', Fore.YELLOW + ' ->','Estratégia MHI 2 - Maioria')
                print('Digite 5', Fore.YELLOW + ' ->','Estratégia MHI 3 - Minoria')
                print('Digite 6', Fore.YELLOW + ' ->','Estratégia MHI 3 - Maioria')
                print('Digite 7', Fore.YELLOW + ' ->','Estratégia Padrão 23')
                print('Digite 8', Fore.YELLOW + ' ->','Estratégia do Milhão - Minoria')
                print('Digite 9', Fore.YELLOW + ' ->','Estratégia do Milhão - Maioria')
                print('Digite 10', Fore.YELLOW + '->','Estratégia Melhor de Três')
                print('Digite 11', Fore.YELLOW + '->','Estratégia Torre Gêmeas')
                print('Digite 12', Fore.YELLOW + '->','Estratégia Três Mosqueteiros')
                print('Digite 13', Fore.YELLOW + '->','Estratégia Padrão Impar')
                print('Digite 14', Fore.YELLOW + '->','Estratégia Padrão C3')
                print('Digite 15', Fore.YELLOW + '->','Estratégia Padrão 3x1')
                print('Digite 16', Fore.YELLOW + '->','Estratégia Padrão R7')
                print('Digite 17', Fore.YELLOW + '->','Estratégia Padrão Seven Wick')
                print('Digite 18', Fore.YELLOW + '->','Catalogar Todas as estratégias\n')
                print(Fore.YELLOW + ':: ', end='')
                tipo = int(input('')) 
                if tipo > 0 : break 
            except: 
                print('\n')
                print(Fore.RED + 35*'*')
                print(Fore.RED + '*','Favor digitar um número válido!', Fore.RED + '*')
                print(Fore.RED + 35*'*')

        print(Fore.CYAN+'\n**************************************', 'Resultados', Fore.CYAN +'*******************************************\n')
        print('+',10*'-','+',17*'-','+',14*'-','+')
        print('|  Paridade  |     Estratégia    | Taxa de Acerto |')
        print('+',10*'-','+',17*'-','+',14*'-','+')
        
        if tipo == 1 :
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhiMinoria(paridade,0)
        elif tipo == 2: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhiMaioria(paridade,0)
        elif tipo == 3: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhi2Minoria(paridade,0)
        elif tipo == 4: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhi2Maioria(paridade,0)
        elif tipo == 5: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhi3Minoria(paridade,0)
        elif tipo == 6: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhi3Maioria(paridade,0)
        elif tipo == 7: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padrao23(paridade,0)
        elif tipo == 8: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    milhaoMinoria(paridade,0)
        elif tipo == 9: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    milhaoMaioria(paridade,0)
        elif tipo == 10: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    melhorDe3(paridade,0)
        elif tipo == 11: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    torreGemeas(paridade,0)
        elif tipo == 12: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    tresMosqueteiros(paridade,0)
        elif tipo == 13: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padraoImpar(paridade,0)
        elif tipo == 14: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padraoC3(paridade,0)
        elif tipo == 15: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padrao3x1(paridade,0)
        elif tipo == 16: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padraoR7(paridade,0)
        elif tipo == 17: 
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    padraoSevenWick(paridade,0)
        elif tipo == 18:
            par = API.get_all_open_time()
            for paridade in par['digital']:
                if par['digital'][paridade]['open'] == True:
                    mhiMinoria(paridade,int(cfg_catalogacao['winrate']))
                    mhiMaioria(paridade,int(cfg_catalogacao['winrate']))
                    mhi2Minoria(paridade,int(cfg_catalogacao['winrate']))
                    mhi2Maioria(paridade,int(cfg_catalogacao['winrate']))
                    mhi3Minoria(paridade,int(cfg_catalogacao['winrate']))
                    mhi3Maioria(paridade,int(cfg_catalogacao['winrate']))
                    padrao23(paridade,int(cfg_catalogacao['winrate']))
                    milhaoMinoria(paridade,int(cfg_catalogacao['winrate']))
                    milhaoMaioria(paridade,int(cfg_catalogacao['winrate']))
                    melhorDe3(paridade,int(cfg_catalogacao['winrate']))
                    torreGemeas(paridade,int(cfg_catalogacao['winrate']))
                    tresMosqueteiros(paridade,int(cfg_catalogacao['winrate']))
                    padraoImpar(paridade,int(cfg_catalogacao['winrate']))
                    padraoC3(paridade,int(cfg_catalogacao['winrate']))
                    padrao3x1(paridade,int(cfg_catalogacao['winrate']))
                    padraoR7(paridade,int(cfg_catalogacao['winrate']))
                    padraoSevenWick(paridade,int(cfg_catalogacao['winrate']))

        print('+',10*'-','+',17*'-','+',14*'-','+')
        print(Fore.YELLOW + '\n->','Deseja Catalogar novamente ? (y -> sim / n -> não)', end='')
        if input(' ::') != 'y': break
         
else: 
    print(Fore.CYAN+'\n********************************', 'Catalogador Automático', Fore.CYAN +'*************************************\n')
    print(Fore.YELLOW + '->','O status de conexão é :', Fore.RED + 'Não Conectado\n')
    print(Fore.RED + 72*'*')
    print(Fore.RED + '*','Problemas na conexão, verifique seus dados de login ou sua internet.', Fore.RED + '*')
    print(Fore.RED + 72*'*')
    time.sleep(10)
    sys.exit()

