"""Maquina virtual educativa que interpreta instrucciones TAC.
Integrar sus extensiones personales cuando corresponda.
4 TODOs ya entregados por el catedrático

Soporta valores enteros y comparaciones que producen 1 (verdadero) / 0 (falso).
Division: // (división entera de Python). Sin entrada interactiva ni frontend.
Limite de pasos por seguridad ante ciclos infinitos.
"""
from typing import List, Dict, Optional
from intermediate.tac import Instruccion

OPERADORES = {'+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>='}


class MaquinaVirtual:
    def __init__(self, tac: List[Instruccion]):
        self.tac = list(tac)
        self.memoria: Dict[str, int] = {}
        self.ip = 0
        self.salidas: List[int] = []
        self.etiquetas: Dict[str, int] = {}
        for i, (op, _a1, _a2, res) in enumerate(self.tac):
            if op == 'LABEL':
                if not res or res in self.etiquetas:
                    raise ValueError(f'[Error VM] Etiqueta repetida o vacia: {res!r}')
                self.etiquetas[res] = i

    def obtener_val(self, arg: Optional[str]) -> int:
        """Lee una constante o una variable/temporal que ya tenga valor."""
        if arg is None:
            raise ValueError('[Error VM] Falta operando obligatorio.')
        if arg.lstrip('-').isdigit():
            return int(arg)
        if arg not in self.memoria:
            raise NameError(f"[Error VM] Variable/temporal '{arg}' sin valor.")
        return self.memoria[arg]

    # EJEMPLO RESUELTO: instruccion de asignacion.
    def instruccion_asignar(self, fuente: Optional[str], destino: Optional[str]):
        if not destino:
            raise ValueError('[Error VM] ASSIGN sin destino.')
        self.memoria[destino] = self.obtener_val(fuente)

    def ejecutar(self, max_pasos: int = 10000) -> List[int]:
        if max_pasos < 1:
            raise ValueError('max_pasos debe ser al menos 1.')
        pasos = 0
        while 0 <= self.ip < len(self.tac):
            if pasos >= max_pasos:
                raise RuntimeError(
                    f'[Limite de ejecucion] Se superaron {max_pasos} pasos. '
                    'Revisa la condicion de while o incrementa el limite.'
                )
            op, arg1, arg2, res = self.tac[self.ip]
            pasos += 1
            if op == 'ASSIGN':
                self.instruccion_asignar(arg1, res)
            elif op in OPERADORES:
                self.instruccion_operacion(op, arg1, arg2, res)
            elif op == 'PRINT':
                self.instruccion_imprimir(arg1)
            elif op == 'JMP':
                self.instruccion_salto(res)
            elif op == 'JMP_FALSE':
                self.instruccion_salto_condicional(arg1, res)
            elif op == 'LABEL':
                pass  # Las etiquetas marcan posiciones, no realizan operaciones.
            else:
                raise NotImplementedError(
                    f"[Error VM] Instruccion '{op}' no soportada. "
                    'Agrega tu extension a OPERADORES o a ejecutar().'
                )
            # Los saltos ubican ip en la etiqueta y este incremento entra en
            # la instruccion inmediatamente posterior a LABEL.
            self.ip += 1
        return self.salidas

    def _ubicacion_etiqueta(self, etiqueta: Optional[str]) -> int:
        if etiqueta not in self.etiquetas:
            raise ValueError(f"[Error VM] Etiqueta de salto desconocida: {etiqueta!r}")
        return self.etiquetas[etiqueta]


    def instruccion_operacion(self, op: str, arg1: Optional[str],
                             arg2: Optional[str], res: Optional[str]) -> None:
        if not res:
            raise ValueError('[Error VM] Operacion sin destino.')
        a = self.obtener_val(arg1)
        b = self.obtener_val(arg2)
        if op == '+': valor = a + b
        elif op == '-': valor = a - b
        elif op == '*': valor = a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError('[Error VM] Division entre cero.')
            valor = a // b
        elif op == '==': valor = int(a == b)
        elif op == '!=': valor = int(a != b)
        elif op == '<': valor = int(a < b)
        elif op == '>': valor = int(a > b)
        elif op == '<=': valor = int(a <= b)
        elif op == '>=': valor = int(a >= b)
        else: raise NotImplementedError(f'[Error VM] Operador {op} sin ejecucion.')
        self.memoria[res] = valor

    def instruccion_imprimir(self, fuente: Optional[str]) -> None:
        valor = self.obtener_val(fuente)
        self.salidas.append(valor)
        print(f'>> SALIDA: {valor}')

    def instruccion_salto(self, etiqueta: Optional[str]) -> None:
        self.ip = self._ubicacion_etiqueta(etiqueta)

    def instruccion_salto_condicional(self, condicion: Optional[str],
                                     etiqueta: Optional[str]) -> None:
        if self.obtener_val(condicion) == 0:
            self.ip = self._ubicacion_etiqueta(etiqueta)
