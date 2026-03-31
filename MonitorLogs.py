import random
import datetime

def menu():
    NomeDoArquivo = 'log.txt'
    while True:
        print('Monitor LogPy')
        print('1 - Gerar Logs')
        print('2 - Analisar Logs')
        print('3 - Gerar e Analisar Logs')
        print('4 - Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            try:
                Quantidade = int(input('Quantidade de Logs'))
                GerarArquivo(NomeDoArquivo, Quantidade)
            except:
                print('Quantidade incorreta')
        elif opcao == '2':
            AnalisarLog(NomeDoArquivo)
        elif opcao == '3':
            try:
                Quantidade = int(input('Quantidade de Logs'))
                GerarArquivo(NomeDoArquivo, Quantidade)
                AnalisarLog(NomeDoArquivo)
            except: 
                print('Quantidade Incorreta')
        elif opcao == '4':
            print('Tchau')
            break
        else:
            print('Opção Errada')

def GerarArquivo(NomeDoArquivo, Quantidade):
    with open(NomeDoArquivo, 'w', encoding='UTF-8') as arq:
        for i in range(Quantidade):
            arq.write(MontarLog(i) + '\n')
        print('Logs Gerados')

def MontarLog(i):
    Data = GerarDataHora(i)
    Ip = GerarIp(i)
    Recurso = GerarRecurso(i)
    Metodo = GerarMetodo(i)
    Status = GerarStatus(i)
    Tempo = GerarTempo(i)
    Agente = GerarAgente(i)
    return f'[{Data}] {Ip} - {Metodo} - {Status} - {Recurso} - {Tempo}ms - 500mb - HTTP/1.1 - {Agente} - /home'

def GerarDataHora(i):
    Base = datetime.datetime(2026, 3, 30, 22,8,0)
    Data = datetime.timedelta(seconds=i * random.randint(5,20))
    return (Base + Data).strftime('%d %m %Y %H:%M:%S')

def GerarIp(i):
    Random = random.randint(1, 6)
    
    if i >= 20 and i <= 30:
        return '444.3.871.888'
    
    return f'{random.randint(10,255)}.{random.randint(1, 255)}.{random.randint(1,255)}.{random.randint(1, 255)}'