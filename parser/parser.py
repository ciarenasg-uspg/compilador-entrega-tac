"""Parser de referencia. ¡Conserva tu parser anterior con sus metodos adicionales!"""
from typing import List
from lexer.token import Token
from arbol_ast.nodos import (
    NodoAST, Programa, Declaracion, Asignacion, Numero, Identificador,
    OpBinaria, Imprimir, Si, Mientras,
)


class Parser:
    def __init__(self, tokens: List[Token]):
        if not tokens or tokens[-1].tipo != 'EOF':
            raise ValueError('El parser necesita una lista de tokens terminada en EOF.')
        self.tokens = tokens
        self.pos = 0
        self.token_actual = tokens[0]

    def avanzar(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.token_actual = self.tokens[self.pos]

    def coincidir(self, valor_esperado: str) -> Token:
        actual = self.token_actual
        if actual.tipo == valor_esperado or actual.valor == valor_esperado:
            self.avanzar()
            return actual
        encontrado = actual.valor if actual.tipo != 'EOF' else 'EOF'
        raise SyntaxError(
            f"[Error Sintactico] Linea {actual.linea}: "
            f"se esperaba '{valor_esperado}', se encontro '{encontrado}' "
            f"(tipo: {actual.tipo})."
        )

    def parsear(self) -> Programa:
        sentencias = []
        while self.token_actual.tipo != 'EOF':
            sentencias.append(self.sentencia())
        return Programa(sentencias)

    def sentencia(self) -> NodoAST:
        tipo = self.token_actual.tipo
        if tipo == 'PR_ENTERO':
            return self.declaracion()
        if tipo == 'ID':
            return self.asignacion()
        if tipo == 'PR_IMPRIMIR':
            return self.sentencia_imprimir()
        if tipo == 'PR_SI':
            return self.sentencia_si()
        if tipo == 'PR_MIENTRAS':
            return self.sentencia_mientras()
        actual = self.token_actual
        raise SyntaxError(
            f"[Error Sintactico] Linea {actual.linea}: "
            f"sentencia no valida al comenzar con '{actual.valor}' ({actual.tipo})."
        )

    def declaracion(self) -> Declaracion:
        palabra = self.coincidir('PR_ENTERO')
        nombre = self.coincidir('ID')
        self.coincidir('ASIGNACION')
        expr = self.expresion()
        self.coincidir(';')
        return Declaracion(palabra.valor, nombre.valor, expr, palabra.linea)

    def asignacion(self) -> Asignacion:
        nombre = self.coincidir('ID')
        self.coincidir('ASIGNACION')
        expr = self.expresion()
        self.coincidir(';')
        return Asignacion(nombre.valor, expr, nombre.linea)

    def expresion(self) -> NodoAST:
        nodo = self.aritmetica()
        while self.token_actual.tipo == 'OP_REL':
            operador = self.token_actual.valor
            self.avanzar()
            nodo = OpBinaria(nodo, operador, self.aritmetica())
        return nodo

    def aritmetica(self) -> NodoAST:
        nodo = self.termino()
        while self.token_actual.valor in ('+', '-'):
            operador = self.token_actual.valor
            self.avanzar()
            nodo = OpBinaria(nodo, operador, self.termino())
        return nodo

    def termino(self) -> NodoAST:
        nodo = self.factor()
        while self.token_actual.valor in ('*', '/'):
            operador = self.token_actual.valor
            self.avanzar()
            nodo = OpBinaria(nodo, operador, self.factor())
        return nodo

    def factor(self) -> NodoAST:
        actual = self.token_actual
        if actual.tipo == 'NUMERO':
            self.avanzar()
            return Numero(int(actual.valor))
        if actual.tipo == 'ID':
            self.avanzar()
            return Identificador(actual.valor, actual.linea)
        if actual.valor == '(':
            self.avanzar()
            nodo = self.expresion()
            self.coincidir(')')
            return nodo
        encontrado = actual.valor if actual.tipo != 'EOF' else 'EOF'
        raise SyntaxError(
            f"[Error Sintactico] Linea {actual.linea}: factor invalido "
            f"'{encontrado}' ({actual.tipo})."
        )

    def sentencia_imprimir(self) -> Imprimir:
        self.coincidir('PR_IMPRIMIR')
        self.coincidir('(')
        expr = self.expresion()
        self.coincidir(')')
        self.coincidir(';')
        return Imprimir(expr)

    def sentencia_si(self) -> Si:
        self.coincidir('PR_SI')
        self.coincidir('(')
        condicion = self.expresion()
        self.coincidir(')')
        return Si(condicion, self.bloque())

    def sentencia_mientras(self) -> Mientras:
        self.coincidir('PR_MIENTRAS')
        self.coincidir('(')
        condicion = self.expresion()
        self.coincidir(')')
        return Mientras(condicion, self.bloque())

    def bloque(self) -> List[NodoAST]:
        self.coincidir('{')
        sentencias = []
        while self.token_actual.valor != '}':
            if self.token_actual.tipo == 'EOF':
                raise SyntaxError(
                    f"[Error Sintactico] Linea {self.token_actual.linea}: "
                    "fin de archivo inesperado: falta '}' para cerrar bloque."
                )
            sentencias.append(self.sentencia())
        self.coincidir('}')
        return sentencias
