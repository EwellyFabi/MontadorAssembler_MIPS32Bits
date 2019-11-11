#################### MONTADOR MIPS 32 BITS ####################
# Autor: Ewelly Sousa

#################### DECLARAÇÃO DE FUNÇÕES ####################


def instruction_R(linha):
    # Trata operações de shift de bits
    if linha[0] == 'sll' or linha[0] == 'srl' or linha[0] == 'sra':
        binario = opR[linha[0]] + '00000' + reg[linha[2]] + reg[linha[1]] + bin(linha[3])[2:].zfill(5) + funct(linha[0])
    elif linha[0] == 'jr':
        binario = opR[linha[0]] + reg[linha[1]] + '000000000000000' + funct[linha[0]]
    else:
        binario = opR[linha[0]] + reg[linha[2]] + reg[linha[3]] + reg[linha[1]] + '00000' + funct[linha[0]]
    saida.write(binario)
    saida.write('\n')

def instruction_I(linha):   
    x = int(linha[2])
    binario = opI[linha[0]] + reg[linha[1]] + reg[linha[3]] + bin(x)[2:].zfill(16)
    saida.write(binario)
    saida.write('\n')

# Trata operações aritméticas imediatas
def instruction_AritI(linha):
    if linha[0] == 'beq' or linha[0] == 'bne':
        binario = opArithmeticImmediate[linha[0]] + reg[linha[1]] + reg[linha[2]] + (address[linha[3]]).zfill(16)
    else:
        x = int(linha[3])
        binario = opArithmeticImmediate[linha[0]] + reg[linha[1]] + reg[linha[2]] + bin(int(x))[2:].zfill(16)

    saida.write(binario)
    saida.write('\n')

def instruction_J(linha):
    binario = opJ[linha[0]] + (address[linha[1]]).zfill(26)
    saida.write(binario)
    saida.write('\n')

#################### FIM DAS DECLARAÇÕES DE FUNÇÕES ####################

#################### DICIONARIOS ####################
# Dicionarios com os opcodes do tipo R, I e J, os registradores,
# o campo funct da instrução do tipo R 

opR = {}
opI = {}
opJ = {}
reg = {}
funct = {}
address = {}
opArithmeticImmediate = {}
codeTemp = []

with open("dicionarioR.txt") as r:
    for line in r:
        (key, val) = line.split()
        opR[key] = val

with open("dicionarioI.txt") as i:
    for line in i:
        (key, val) = line.split()
        opI[key] = val

with open("dicionarioJ.txt") as j:
    for line in j:
        (key, val) = line.split()
        opJ[key] = val

with open("dicionarioReg.txt") as r:
    for line in r:
        (key, val) = line.split()
        reg[str(key)] = val

with open("dicionarioFunct.txt") as f:
    for line in f:
        (key, val) = line.split()
        funct[str(key)] = val

with open("dicionarioArit_Imed.txt") as a:
    for line in a:
        (key, val) = line.split()
        opArithmeticImmediate[str(key)] = val


# Lê o código MIPS e faz a tradução para o código binário
with open("codigo_mips.txt","r") as c:
    
    numLinha = 1
    ##################### TRATANDO O CODIGO #####################
    for line in c:
        # Verifica se a linha é um comentário, caso seja, ignora
        if line[0][0] == '#':
            continue
        # Verifica se é uma linha vazia, caso seja, ignora
        if len(line) == 1:
            continue

        # Troca as virgulas e parenteses por um espaço para e 
        # faz um split para obter uma lista
        line = line.replace(',',' ').replace('(',' ').replace(')',' ').split()

        cont = 0
        for word in line:
            # Remove os comentarios do código
            if(word[0] == '#'):
                while len(line) != cont:
                    del line[cont] 
            cont += 1
            # Procura o endereço das labels
            if(word[-1] == ':'):
                word = word.replace(':', '')
                address[word] = bin(numLinha)[2:]
                del(line[0])
                #print(printBit(numLinha))
        numLinha += 1

        # Verifica se é uma linha vazia, caso seja, ignora
        if len(line) == 1:
            continue
        print(line)
        codeTemp.append(line)
    ##################### FIM TRATAMENTO DO CODIGO #####################

    ##################### TRADUÇÃO DAS INSTRUÇÕES #####################
    # Cria arquivo que vai receber o código binário
    saida = open("codigo_bin.txt", "w+")
    for linha in codeTemp:
        # Instrução do tipo R
        if linha[0] in opR: 
            instruction_R(linha)
        # Instrução do tipo I
        elif linha[0] in opI: 
            instruction_I(linha)
        # Instrução do tipo J
        elif linha[0] in opJ: 
            instruction_J(linha)
        # Instrução do tipo Aritmética com imediato
        elif linha[0] in opArithmeticImmediate: 
            instruction_AritI(linha)
        
       