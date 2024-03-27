from random import randint
import argparse
import matplotlib as plt
parser = argparse.ArgumentParser(description='Calculadora, suma/resta/multiplica a y b')
parser.add_argument('-c', '--corridas', type=int, help='Corridas')
parser.add_argument('-n', '--numero_tiradas', type=int, help='numero de tiradas')
parser.add_argument('-e', '--numero_eleguido', type=int, help='numero de eleguido')

args = parser.parse_args()




if args.corridas and args.numero_tiradas and args.numero_eleguido:
    data = []
    frecuencia_absoluta = 0
    for corrida in range(args.corridas):
        data.append({})
        for tirada in range(args.numero_tiradas):
            key = randint(0, 36)
            if key == args.numero_eleguido:
                frecuencia_absoluta += 1
            if key in data[corrida].keys():
                data[corrida][key] += 1
            else:
                data[corrida][key] = 1
    print('frecuencia Absoluta:', frecuencia_absoluta)
    print('freciencia relativa: ', frecuencia_absoluta/(args.numero_tiradas*args.corridas))
else:
    print(' Los valores -c -n -e son obligatorios')
    exit()