"""Generador de código intermedio (TAC = Three Address Code).
Integrar sus extensiones personales cuando corresponda.

Formato de instrucción: (operacion, argumento1, argumento2, destino).
Los temporales internos comienzan con @t y las etiquetas con @L para evitar
colisiones con nombres de variables permitidos por el lexer base.
"""
from typing import List, Tuple, Optional
from arbol_ast.nodos import (
    NodoAST, Programa, Declaracion, Asignacion, Numero, Identificador,
    OpBinaria, Imprimir, Si, Mientras,
)

Instruccion = Tuple[str, Optional[str], Optional[str], Optional[str]]


class GeneradorTAC:
    def __init__(self):
        self.instrucciones: List[Instruccion] = []
        self.conteo_temp = 0
        self.conteo_etiquetas = 0

    def nuevo_temp(self) -> str:
        self.conteo_temp += 1
        return f'@t{self.conteo_temp}'

    def nueva_etiqueta(self) -> str:
        self.conteo_etiquetas += 1
        return f'@L{self.conteo_etiquetas}'

    def emitir(self, op: str, arg1: Optional[str] = None,
               arg2: Optional[str] = None, res: Optional[str] = None) -> None:
        self.instrucciones.append((op, arg1, arg2, res))

    def generar(self, nodo: NodoAST) -> List[Instruccion]:
        """Visita un nodo y acumula instrucciones; devolver no implica reiniciar."""
        metodo = f'generar_{type(nodo).__name__}'
        visitante = getattr(self, metodo, self.error_generico)
        visitante(nodo)
        return self.instrucciones

    def error_generico(self, nodo: NodoAST):
        raise NotImplementedError(
            f'No existe generacion TAC para {type(nodo).__name__}. '
            'Adapta tu extension personal.'
        )

    def generar_Programa(self, nodo: Programa) -> None:
        for sentencia in nodo.sentencias:
            self.generar(sentencia)

    # EJEMPLO RESUELTO DEL DOCENTE: declaracion con expresion de inicializacion.
    def generar_Declaracion(self, nodo: Declaracion) -> None:
        fuente = self.evaluar_expr(nodo.expr)
        self.emitir('ASSIGN', fuente, None, nodo.id)


    def generar_Asignacion(self, nodo: Asignacion) -> None:
        # TODO TAC 1: obtener la fuente de nodo.expr y emitir ASSIGN.
        raise NotImplementedError('TODO TAC 1: generar_Asignacion')

    def generar_Imprimir(self, nodo: Imprimir) -> None:
        # TODO TAC 2: evaluar expresion y emitir PRINT.
        raise NotImplementedError('TODO TAC 2: generar_Imprimir')

    def generar_Si(self, nodo: Si) -> None:
        # TODO TAC 3: evaluar condicion; JMP_FALSE a etiqueta_fin; bloque; LABEL.
        raise NotImplementedError('TODO TAC 3: generar_Si')

    def generar_Mientras(self, nodo: Mientras) -> None:
        # TODO TAC 4: LABEL inicio, condicion, JMP_FALSE fin, bloque, JMP inicio, LABEL fin.
        # La condicion debe calcularse DENTRO del ciclo para reevaluarse.
        raise NotImplementedError('TODO TAC 4: generar_Mientras')

    def evaluar_expr(self, nodo: NodoAST) -> str:
        # TODO TAC 5: Numero -> literal; Identificador -> nombre;
        # OpBinaria -> emitir subexpresiones recursivamente y crear temporal.
        raise NotImplementedError('TODO TAC 5: evaluar_expr')
