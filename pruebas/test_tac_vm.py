"""Pruebas de la entrega final. Algunos casos FALLARAN hasta completar los TODO.
Ejecutar: python -m unittest discover -s pruebas -p "test_*.py" -v
"""
import unittest
from contextlib import redirect_stdout
from io import StringIO

from lexer.lexer import Lexer
from parser.parser import Parser
from semantic.analizador import AnalizadorSemantico
from intermediate.tac import GeneradorTAC
from vm.maquina_virtual import MaquinaVirtual


def compilar(codigo):
    arbol = Parser(Lexer(codigo).analizar()).parsear()
    AnalizadorSemantico().analizar(arbol)
    return GeneradorTAC().generar(arbol)


def correr(codigo, max_pasos=10000):
    tac = compilar(codigo)
    vm = MaquinaVirtual(tac)
    with redirect_stdout(StringIO()):
        resultados = vm.ejecutar(max_pasos=max_pasos)
    return tac, vm, resultados


class TestEstructuraEntregada(unittest.TestCase):
    def test_generador_sin_instrucciones(self):
        self.assertEqual(GeneradorTAC().instrucciones, [])

    def test_formato_y_etiquetas(self):
        g = GeneradorTAC()
        self.assertEqual(g.nuevo_temp(), '@t1')
        self.assertEqual(g.nueva_etiqueta(), '@L1')
        g.emitir('ASSIGN', '5', None, 'x')
        self.assertEqual(g.instrucciones, [('ASSIGN', '5', None, 'x')])

    def test_asignacion_vm_ya_implementada(self):
        vm = MaquinaVirtual([('ASSIGN', '20', None, 'x')])
        with redirect_stdout(StringIO()):
            vm.ejecutar()
        self.assertEqual(vm.memoria['x'], 20)


class TestTAC(unittest.TestCase):
    def test_declaracion_simple(self):
        self.assertEqual(compilar('entero x = 7;'), [('ASSIGN', '7', None, 'x')])

    def test_asignacion(self):
        tac = compilar('entero x = 1; x = 9;')
        self.assertEqual(tac[-1], ('ASSIGN', '9', None, 'x'))

    def test_expresiones_precedencia(self):
        tac = compilar('entero x = 5 + 3 * 2;')
        self.assertEqual([i[0] for i in tac], ['*', '+', 'ASSIGN'])
        self.assertEqual(tac[0][1:3], ('3', '2'))

    def test_imprimir(self):
        tac = compilar('imprimir(15);')
        self.assertEqual(tac, [('PRINT', '15', None, None)])

    def test_si(self):
        tac = compilar('si (1 < 2) { imprimir(3); }')
        self.assertEqual([i[0] for i in tac], ['<', 'JMP_FALSE', 'PRINT', 'LABEL'])

    def test_mientras(self):
        tac = compilar('entero x = 0; mientras (x < 3) { x = x + 1; }')
        ops = [i[0] for i in tac]
        self.assertEqual(ops, ['ASSIGN', 'LABEL', '<', 'JMP_FALSE', '+', 'ASSIGN', 'JMP', 'LABEL'])


class TestVM(unittest.TestCase):
    def test_ejecutar_declaracion(self):
        _tac, vm, _salidas = correr('entero x = 10;')
        self.assertEqual(vm.memoria['x'], 10)

    def test_ejecutar_operaciones_y_salida(self):
        _tac, vm, salidas = correr('entero x = 5 + 3 * 2; imprimir(x);')
        self.assertEqual(vm.memoria['x'], 11)
        self.assertEqual(salidas, [11])

    def test_asignacion_y_cambio(self):
        _tac, vm, salidas = correr('entero x = 1; x = x + 2; imprimir(x);')
        self.assertEqual((vm.memoria['x'], salidas), (3, [3]))

    def test_si_verdadero_y_falso(self):
        _tac, _vm, salidas = correr('si (2 > 1) { imprimir(7); } si (1 > 2) { imprimir(9); }')
        self.assertEqual(salidas, [7])

    def test_while(self):
        _tac, vm, salidas = correr('entero x = 0; mientras (x < 3) { imprimir(x); x = x + 1; }')
        self.assertEqual(salidas, [0, 1, 2])
        self.assertEqual(vm.memoria['x'], 3)

    def test_division_entera(self):
        _tac, _vm, salidas = correr('imprimir(10 / 3);')
        self.assertEqual(salidas, [3])

    def test_comparacion_imprimible(self):
        _tac, _vm, salidas = correr('imprimir(5 >= 3); imprimir(2 == 3);')
        self.assertEqual(salidas, [1, 0])

    def test_division_por_cero(self):
        with self.assertRaises(ZeroDivisionError):
            correr('imprimir(1 / 0);')

    def test_limite_de_pasos(self):
        with self.assertRaises(RuntimeError):
            correr('entero x = 1; mientras (x == 1) { imprimir(x); }', max_pasos=40)

    def test_temporal_no_colisiona_identificador_t1(self):
        _tac, vm, salidas = correr('entero t1 = 9; entero x = 1 + 2; imprimir(t1); imprimir(x);')
        self.assertEqual(salidas, [9, 3])


class TestRegresion(unittest.TestCase):
    def test_error_semantico_bloquea_tac(self):
        with self.assertRaises(NameError):
            compilar('imprimir(x);')

    def test_error_sintactico_bloquea_tac(self):
        with self.assertRaises(SyntaxError):
            compilar('entero x = ;')

    def test_error_lexico_bloquea_tac(self):
        with self.assertRaises(RuntimeError):
            compilar('entero x = @;')


if __name__ == '__main__':
    unittest.main()
