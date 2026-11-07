# Compilador — Entrega FINAL (TAC + Máquina Virtual)

## Objetivo
Unificar las dos últimas fases del compilador incremental: **generar instrucciones TAC desde el AST validado** y **ejecutarlas con la máquina virtual**. Se conserva lo desarrollado en las entregas de Lexer, Parser y Semántica.

## Qué entrega el catedrático
- `main.py`: pipeline integrado y comandos para detenerse después de una fase.
- `lexer/`, `parser/`, `arbol_ast/`, `semantic/`: **versiones de referencia completas para el lenguaje base**. No sustituir las versiones personalizadas de entregas anteriores.
- `intermediate/tac.py`: clase `GeneradorTAC` con contador de temporales, etiquetas, `emitir()`, despacho de visitantes y un ejemplo resuelto de declaración. **Cinco TODO**.
- `vm/maquina_virtual.py`: infraestructura VM, memoria, puntero de ejecución `ip`, etiquetas, límite de pasos, lectura de operandos, `ASSIGN` resuelto. **Cuatro TODO**.
- `pruebas/`: casos válidos, errores y pruebas unitarias que reflejan el contrato de cada fase.
- `GUIA_EXTENSIONES_FINAL.md`: cómo adaptar TAC y VM a tus funcionalidades personales.

## Qué implementa el estudiante (9 TODO)
**TAC**: `generar_Asignacion()`, `generar_Imprimir()`, `generar_Si()`, `generar_Mientras()`, `evaluar_expr()`.

**VM**: `instruccion_operacion()`, `instruccion_imprimir()`, `instruccion_salto()`, `instruccion_salto_condicional()`.

No basta con quitar `raise NotImplementedError`: el método debe generar instrucciones o ejecutar las operaciones correctas.

## ¡IMPORTANTE! Integración con tus entregas previas
Continúa **en tu repositorio y con tus archivos anteriores**. Este ZIP trae un lenguaje base completo para guiarte, pero **no incorpora automáticamente tus tokens, AST y reglas individuales**. Conserva tus personalizaciones y adapta `intermediate/`, `vm/` y `main.py` al proyecto que ya realizaste.

## Formato de TAC
Cada instrucción es una tupla de cuatro valores `(op, arg1, arg2, res)`.

```text
entero x = 5 + 3;
imprimir(x);

('+', '5', '3', '@t1')
('ASSIGN', '@t1', None, 'x')
('PRINT', 'x', None, None)
```

- Los temporales son `@t1`, `@t2`, etc. y las etiquetas son `@L1`, `@L2`, etc. Son nombres internos, distintos a los identificadores del lenguaje.
- `LABEL` marca un destino; `JMP` y `JMP_FALSE` cambian el `ip` de la VM.
- En `mientras`, la condición TAC debe estar **después de la etiqueta de inicio** para recalcularse en cada iteración.
- Comparaciones se ejecutan como `1` (verdadero) y `0` (falso). La semántica las tipa como `booleano`.
- La división entre enteros usa `//` y un divisor cero provoca error de ejecución.
- El límite de pasos de la VM evita que un programa con un `mientras` infinito quede ejecutándose sin fin.

## Ejecución
Desde la raíz del proyecto:

```bash
python main.py
python main.py pruebas/16_salidas_y_expresiones.txt
python main.py pruebas/18_ciclo_while.txt
python main.py pruebas/03_control.txt --solo-tac
python main.py --solo-lexer
python main.py --solo-parser
python main.py --solo-semantica
python main.py pruebas/20_ciclo_infinito_limite.txt --limite-pasos 50
python -m unittest discover -s pruebas -p "test_*.py" -v
```

En esta plantilla, la ejecución completa **se detendrá en el primer TODO** hasta implementarlo. Para comprobar las fases previas, usa `--solo-semantica`.

## Pruebas y entrega
Ejecuta los casos de las cinco fases, incorpora pruebas de tus extensiones anteriores y documenta: código de entrada, TAC generado, salida de la VM y errores detectados. Incluye al menos un caso válido y uno de error relevante a tu funcionalidad personal, cuando corresponda. No modifiques los tests entregados para ocultar fallos.

**Entregable:** enlace al repositorio **GitHub** con código integrado, README, ejemplos de ejecución y evidencias de pruebas; sin frontend obligatorio.
