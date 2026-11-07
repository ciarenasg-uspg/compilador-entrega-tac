# Guía de extensiones personales — entrega final

Las funcionalidades que agregaste al lexer y parser, y luego validaste en semántica, **deben atravesar las fases nuevas cuando afecten la ejecución**. No recibimos tus tokens personalizados en este ZIP, por lo que debes integrar el generador y la VM con tu propia base.

| Extensión previa | ¿Cambiar TAC? | ¿Cambiar VM? | Razón |
|---|---|---|---|
| `%` (módulo) en `OpBinaria` | Sí | Sí | Emitir `%` y ejecutar `a % b` (verificar divisor cero). |
| `^` potencia en `OpBinaria` | Sí | Sí | Emitir `^` y calcular potencia según tipos del lenguaje. |
| Comparadores `<=` `>=` | No, si ya usa `OpBinaria` | Sí, si no estaban | El TAC genérico emite el operador; VM debe ejecutarlo. |
| `&&` `||` | Puede requerir cambios | Sí | Elegir evaluación directa o cortocircuito y documentarlo. |
| Decimal | Puede requerir cambios | Sí | Representar literales, valores, división y tipos numéricos. |
| `sino` | Sí | No necesariamente | Usar `JMP`, `JMP_FALSE` y `LABEL` ya disponibles. |
| `leer()` | Sí | Sí | Emitir instrucción de entrada y ejecutarla (no cubierta por VM base). |
| `//` comentarios eliminados por lexer | No | No | No llegan al AST. |
| `++` | Según el nodo AST | Quizá no | Puede expandirse a suma más asignación. |

**Importante:** la decisión depende del **nodo AST y su semántica**, no solamente del nombre del token. Si tu parser transforma `%` a `OpBinaria`, `evaluar_expr()` ya puede emitir `%` una vez implementado, pero la VM necesita reconocerlo en `OPERADORES` y resolverlo en `instruccion_operacion()`.

## Ejemplo: operador módulo `%`
1. Lexer previo: reconocía `OP_MOD` para `%`.
2. Parser previo: lo incluyó junto a `*` y `/` en `termino()`.
3. AST: puede reutilizar `OpBinaria(Numero(10), '%', Numero(3))`.
4. Semántica: exige enteros y devuelve `entero`.
5. TAC: en `evaluar_expr()` genérico se emite `('%', '10', '3', '@t1')`.
6. VM: agregar `'%'` a `OPERADORES` y `elif op == '%': valor = a % b`, verificando `b != 0`.
7. Prueba con `entero r = 10 % 3; imprimir(r);` → salida `1` y prueba `10 % 0` → error.

## Ejemplo: comentarios
Si los comentarios son ignorados en el lexer, no aparecen como nodos AST y no necesitan soporte nuevo en TAC/VM. Demostrar que un comentario no afecta el resultado de ejecución.

## Evidencias solicitadas
- Un archivo de programa con tu sintaxis personalizada que llegue hasta ejecución final.
- El TAC correspondiente y la salida de la VM (captura o transcripción).
- Un caso de error relevante: sintáctico, semántico o de ejecución; cuando tu extensión no puede generar un error propio, documenta el motivo y prueba un error del lenguaje base.
- Explicar qué archivos cambiaste, el nodo AST involucrado y cómo funciona su ejecución.
