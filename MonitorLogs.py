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
                Quantidade = int(input('Quantidade de Logs: '))
                GerarArquivo(NomeDoArquivo, Quantidade)
            except:
                print('Quantidade incorreta')

        elif opcao == '2':
            AnalisarLog(NomeDoArquivo)

        elif opcao == '3':
            try:
                Quantidade = int(input('Quantidade de Logs: '))
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
    Status = GerarStatus(i, Recurso)
    Tempo = GerarTempo(i)
    Agente = GerarAgente(i)
    Tamanho = GerarTamanho()
    Protocolo = GerarProtocolo()

    return f'[{Data}] {Ip} - {Metodo} - {Status} - {Recurso} - {Tempo}ms - {Tamanho}B - {Protocolo} - {Agente} - /home'


def GerarDataHora(i):
    Base = datetime.datetime(2026, 3, 30, 22, 8, 0)
    Data = datetime.timedelta(seconds=i * random.randint(5,20))
    return (Base + Data).strftime('%d/%m/%Y %H:%M:%S')


def GerarIp(i):
    if i >= 20 and i <= 30:
        return '444.3.871.888'
    return f'{random.randint(10,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'


def GerarRecurso(i):
    r = random.randint(1,6)

    if r == 1:
        return '/home'
    elif r == 2:
        return '/login'
    elif r == 3:
        return '/admin'
    elif r == 4:
        return '/produtos'
    elif r == 5:
        return '/config'
    else:
        return '/backup'


def GerarMetodo(i):
    if random.randint(0,1) == 0:
        return 'GET'
    return 'POST'


def GerarStatus(i, Recurso):
    r = random.randint(1,10)

    if Recurso == '/login' and r < 5:
        return 403

    if Recurso == '/admin' and r < 4:
        return 403

    if r == 8:
        return 404

    if r >= 9:
        return 500

    return 200


def GerarTempo(i):
    return random.randint(50,1200)


def GerarAgente(i):
    r = random.randint(1,6)

    if r == 1:
        return 'Chrome'
    elif r == 2:
        return 'Opera'
    elif r == 3:
        return 'Edge'
    elif r == 4:
        return 'Firefox'
    elif r == 5:
        return 'Brave'
    else:
        return 'Safari'


def GerarTamanho():
    return random.randint(200,2000)


def GerarProtocolo():
    r = random.randint(1,3)

    if r == 1:
        return 'HTTP/1.0'
    elif r == 2:
        return 'HTTP/1.1'
    else:
        return 'HTTP/2'


def ExtrairCampo(linha, inicio, fim):
    Texto = ''
    i = inicio

    while i < fim:
        Texto = Texto + linha[i]
        i += 1

    return Texto


def AnalisarLog(NomeDoArquivo):

    Total = 0
    Sucessos = 0
    Erros = 0
    Erros500 = 0

    SomaTempo = 0
    MaiorTempo = 0
    MenorTempo = 999999

    Rapidos = 0
    Normais = 0
    Lentos = 0

    Status200 = 0
    Status403 = 0
    Status404 = 0
    Status500 = 0

    AdminErro = 0

    Brute = 0
    BruteSeq = 0
    UltimoBruteIp = ''

    UltimoIp = ''
    SeqIp = 0
    Bots = 0
    UltimoBotIp = ''

    UltimoTempo = 0
    Aumento = 0
    Degradacao = 0

    Falha500Seq = 0
    FalhaCritica = 0

    Sensiveis = 0
    SensiveisErro = 0

    with open(NomeDoArquivo, 'r', encoding='UTF-8') as arq:

        for linha in arq:

            Total += 1

            Pos1 = linha.find('] ')
            Pos2 = linha.find(' - ', Pos1+2)
            Ip = ExtrairCampo(linha, Pos1+2, Pos2)

            Pos3 = linha.find(' - ', Pos2+3)
            Metodo = ExtrairCampo(linha, Pos2+3, Pos3)

            Pos4 = linha.find(' - ', Pos3+3)
            Status = int(ExtrairCampo(linha, Pos3+3, Pos4))

            Pos5 = linha.find(' - ', Pos4+3)
            Recurso = ExtrairCampo(linha, Pos4+3, Pos5)

            Pos6 = linha.find('ms', Pos5+3)
            Tempo = int(ExtrairCampo(linha, Pos5+3, Pos6))

            SomaTempo += Tempo

            if Tempo > MaiorTempo:
                MaiorTempo = Tempo

            if Tempo < MenorTempo:
                MenorTempo = Tempo

            if Tempo < 200:
                Rapidos += 1
            elif Tempo < 800:
                Normais += 1
            else:
                Lentos += 1

            if Status == 200:
                Sucessos += 1
                Status200 += 1
                Falha500Seq = 0
            else:
                Erros += 1

            if Status == 403:
                Status403 += 1

            if Status == 404:
                Status404 += 1

            if Status == 500:
                Status500 += 1
                Erros500 += 1
                Falha500Seq += 1

                if Falha500Seq == 3:
                    FalhaCritica += 1
                    Falha500Seq = 0

            if Recurso == '/admin' and Status != 200:
                AdminErro += 1

            if Recurso == '/admin' or Recurso == '/backup' or Recurso == '/config' or Recurso == '/private':
                Sensiveis += 1
                if Status != 200:
                    SensiveisErro += 1

            if Recurso == '/login' and Status == 403:
                BruteSeq += 1
                UltimoBruteIp = Ip

                if BruteSeq == 3:
                    Brute += 1
                    BruteSeq = 0
            else:
                BruteSeq = 0

            if Ip == UltimoIp:
                SeqIp += 1
            else:
                SeqIp = 1

            if SeqIp >= 5:
                Bots += 1
                UltimoBotIp = Ip
                SeqIp = 0

            UltimoIp = Ip

            if Tempo > UltimoTempo:
                Aumento += 1
            else:
                Aumento = 0

            if Aumento == 3:
                Degradacao += 1
                Aumento = 0

            UltimoTempo = Tempo

    MediaTempo = SomaTempo / Total
    Disponibilidade = (Sucessos / Total) * 100
    TaxaErro = (Erros / Total) * 100

    if FalhaCritica > 0 or Disponibilidade < 70:
        Estado = 'CRITICO'
    elif Disponibilidade < 85 or Lentos > Normais:
        Estado = 'INSTAVEL'
    elif Disponibilidade < 95 or Bots > 0:
        Estado = 'ATENCAO'
    else:
        Estado = 'SAUDAVEL'

    print('\nRELATORIO')
    print('Total acessos:', Total)
    print('Sucessos:', Sucessos)
    print('Erros:', Erros)
    print('Erros 500:', Erros500)
    print('Disponibilidade:', Disponibilidade)
    print('Taxa erro:', TaxaErro)
    print('Tempo medio:', MediaTempo)
    print('Maior tempo:', MaiorTempo)
    print('Menor tempo:', MenorTempo)
    print('Rapidos:', Rapidos)
    print('Normais:', Normais)
    print('Lentos:', Lentos)
    print('Status 200:', Status200)
    print('Status 403:', Status403)
    print('Status 404:', Status404)
    print('Status 500:', Status500)
    print('Brute force:', Brute)
    print('Ultimo IP brute:', UltimoBruteIp)
    print('Admin erros:', AdminErro)
    print('Degradacao:', Degradacao)
    print('Falhas criticas:', FalhaCritica)
    print('Bots:', Bots)
    print('Ultimo bot:', UltimoBotIp)
    print('Rotas sensiveis:', Sensiveis)
    print('Erros rotas sensiveis:', SensiveisErro)
    print('Estado final:', Estado)


menu()
