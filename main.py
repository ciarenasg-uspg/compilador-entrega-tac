"""Compilador incremental final: Lexer > Parser/AST > Semantica > TAC > VM."""
import argparse
from pathlib import Path

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analizador import AnalizadorSemantico
from intermediate.tac import GeneradorTAC
from vm.maquina_virtual import MaquinaVirtual

BASE_DIR = Path(__file__).resolve().parent


def analizar_lexico(codigo):
    print('\n=== FASE 1 - LEXER ===')
    tokens = Lexer(codigo).analizar()
    for token in tokens:
        print(' ', token)
    return tokens


def analizar_sintactico(tokens):
    print('\n=== FASE 2 - PARSER + AST ===')
    arbol = Parser(tokens).parsear()
    print(arbol)
    return arbol


def analizar_semantica(arbol):
    print('\n=== FASE 3 - SEMANTICA ===')
    sem = AnalizadorSemantico()
    sem.analizar(arbol)
    print('Tabla de simbolos:', sem.tabla_simbolos)
    return sem


def generar_tac(arbol):
    print('\n=== FASE 4 - CODIGO INTERMEDIO (TAC) ===')
    tac = GeneradorTAC().generar(arbol)
    for i, (op, arg1, arg2, res) in enumerate(tac):
        print(f'{i:02d} | {op:<10} | {str(arg1):<8} | {str(arg2):<8} | {str(res)}')
    return tac


def ejecutar_vm(tac, limite_pasos):
    print('\n=== FASE 5 - MAQUINA VIRTUAL ===')
    vm = MaquinaVirtual(tac)
    salidas = vm.ejecutar(max_pasos=limite_pasos)
    print('\nMemoria final:', {k: v for k, v in vm.memoria.items() if not k.startswith('@t')})
    print('Salidas:', salidas)
    return vm


def main():
    argumentos = argparse.ArgumentParser(description='Compilador incremental completo')
    argumentos.add_argument('archivo', nargs='?', default='pruebas/01_basico_valido.txt',
                            help='Archivo de programa fuente (por defecto: pruebas/01_basico_valido.txt)')
    fases = argumentos.add_mutually_exclusive_group()
    fases.add_argument('--solo-lexer', action='store_true')
    fases.add_argument('--solo-parser', action='store_true')
    fases.add_argument('--solo-semantica', action='store_true')
    fases.add_argument('--solo-tac', action='store_true')
    argumentos.add_argument('--limite-pasos', type=int, default=10000,
                            help='Maximo de instrucciones VM (por defecto 10000)')
    opciones = argumentos.parse_args()
    ruta = Path(opciones.archivo)
    if not ruta.is_absolute() and not ruta.exists():
        ruta = BASE_DIR / ruta
    try:
        codigo = ruta.read_text(encoding='utf-8')
    except OSError as err:
        print(f'[Error archivo] No se pudo abrir {ruta}: {err}')
        return 1
    print('=== MI COMPILADOR - ENTREGA FINAL ===')
    print('\nCODIGO FUENTE:\n'+codigo)
    try:
        tokens = analizar_lexico(codigo)
        if opciones.solo_lexer: return 0
        arbol = analizar_sintactico(tokens)
        if opciones.solo_parser: return 0
        analizar_semantica(arbol)
        if opciones.solo_semantica: return 0
        tac = generar_tac(arbol)
        if opciones.solo_tac: return 0
        ejecutar_vm(tac, opciones.limite_pasos)
        print('\nCompilacion y ejecucion completadas.')
        return 0
    except NotImplementedError as err:
        print(f'\n[IMPLEMENTACION PENDIENTE] {err}')
        return 2
    except (RuntimeError, SyntaxError, NameError, TypeError, ValueError,
            ZeroDivisionError) as err:
        print(f'\n{err}')
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
