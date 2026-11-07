"""Analisis semantico de referencia. ¡Conserva tu Analisis semantico anterior con sus metodos adicionales!"""

from typing import Dict, Optional
from arbol_ast.nodos import (
    NodoAST, Programa, Declaracion, Asignacion, Numero, Identificador,
    OpBinaria, Imprimir, Si, Mientras,
)

class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos: Dict[str, str] = {}

    def analizar(self, nodo: NodoAST) -> Optional[str]:
        metodo = f'visitar_{type(nodo).__name__}'
        visitante = getattr(self, metodo, self.error_generico)
        return visitante(nodo)

    def error_generico(self, nodo: NodoAST):
        raise NotImplementedError(
            f'Falta soporte semantico para el nodo {type(nodo).__name__}. '
            'Revisa las extensiones personales de lexer, parser y AST.'
        )

    def visitar_Programa(self, nodo: Programa) -> None:
        for sentencia in nodo.sentencias:
            self.analizar(sentencia)

    def visitar_Numero(self, nodo: Numero) -> str:
        return 'entero'

    def visitar_Imprimir(self, nodo: Imprimir) -> None:
        self.analizar(nodo.expr)

    def visitar_Declaracion(self, nodo: Declaracion) -> None:
        if nodo.id in self.tabla_simbolos:
            raise NameError(
                f"[Error Semantico] Linea {nodo.linea}: "
                f"variable '{nodo.id}' ya declarada."
            )
        tipo_expr = self.analizar(nodo.expr)
        if tipo_expr != nodo.tipo:
            raise TypeError(
                f"[Error Semantico] Linea {nodo.linea}: "
                f"no se puede inicializar '{nodo.id}' de tipo '{nodo.tipo}' "
                f"con expresion de tipo '{tipo_expr}'."
            )
        self.tabla_simbolos[nodo.id] = nodo.tipo

    def visitar_Asignacion(self, nodo: Asignacion) -> None:
        if nodo.id not in self.tabla_simbolos:
            raise NameError(
                f"[Error Semantico] Linea {nodo.linea}: "
                f"variable '{nodo.id}' no declarada."
            )
        tipo_expr = self.analizar(nodo.expr)
        tipo_var = self.tabla_simbolos[nodo.id]
        if tipo_expr != tipo_var:
            raise TypeError(
                f"[Error Semantico] Linea {nodo.linea}: "
                f"asignacion incompatible: '{nodo.id}' es '{tipo_var}' "
                f"pero la expresion es '{tipo_expr}'."
            )

    def visitar_Identificador(self, nodo: Identificador) -> str:
        if nodo.nombre not in self.tabla_simbolos:
            raise NameError(
                f"[Error Semantico] Linea {nodo.linea}: "
                f"variable '{nodo.nombre}' no declarada."
            )
        return self.tabla_simbolos[nodo.nombre]

    def visitar_OpBinaria(self, nodo: OpBinaria) -> str:
        tipo_izq = self.analizar(nodo.izq)
        tipo_der = self.analizar(nodo.der)
        aritmeticos = {'+', '-', '*', '/'}
        relacionales = {'==', '!=', '<', '>', '<=', '>='}
        if nodo.op in aritmeticos or nodo.op in relacionales:
            if tipo_izq != 'entero' or tipo_der != 'entero':
                raise TypeError(
                    f"[Error Semantico] Operador '{nodo.op}' exige "
                    f"dos enteros, se recibieron '{tipo_izq}' y '{tipo_der}'."
                )
            return 'entero' if nodo.op in aritmeticos else 'booleano'
        raise TypeError(
            f"[Error Semantico] Operador '{nodo.op}' sin regla semantica. "
            'Si es una extension personal, define su validacion y tipo de resultado.'
        )

    def visitar_Si(self, nodo: Si) -> None:
        tipo_cond = self.analizar(nodo.condicion)
        if tipo_cond != 'booleano':
            raise TypeError(
                '[Error Semantico] La condicion de si debe ser booleano; '
                f'se recibio {tipo_cond}.'
            )
        for sentencia in nodo.bloque_v:
            self.analizar(sentencia)

    def visitar_Mientras(self, nodo: Mientras) -> None:
        tipo_cond = self.analizar(nodo.condicion)
        if tipo_cond != 'booleano':
            raise TypeError(
                '[Error Semantico] La condicion de mientras debe ser booleano; '
                f'se recibio {tipo_cond}.'
            )
        for sentencia in nodo.bloque:
            self.analizar(sentencia)
