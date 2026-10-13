# Traktor Kontrol X1 - Ableton Live 12 MIDI Remote Script

Este proyecto es un **Script Remoto MIDI (MIDI Remote Script)** personalizado para Ableton Live 12, diseñado para utilizar el controlador **Native Instruments Traktor Kontrol X1** (configurado en modo MIDI) para manejar funciones clave de transporte, navegación del navegador (browser) y de la vista Arrangement.

Está construido utilizando el API interno de Ableton (`_Framework`).

## 🛠️ Instalación

Para que Ableton Live 12 reconozca el script, la carpeta `Traktor_Kontrol_X1` debe estar en el lugar correcto. 

**Ruta Recomendada (Live 11 y 12):**
1. Ve a tu carpeta de usuario de Ableton: `Documentos\Ableton\User Library\Remote Scripts\`
2. (Si la carpeta `Remote Scripts` no existe, créala).
3. Copia allí la carpeta `Traktor_Kontrol_X1`.

**Ruta Alternativa (Instalación del sistema):**
`C:\ProgramData\Ableton\Live 12 Suite\Resources\MIDI Remote Scripts\`

**Activación:**
1. **Reinicia Ableton Live.** (Ableton solo lee estos scripts al arrancar).
2. Abre Ableton, ve a **Preferencias (Preferences) > Link / Tempo / MIDI**.
3. En la sección **Superficie de control (Control Surface)**, busca en el menú desplegable y selecciona `Traktor Kontrol X1`.
4. En las entradas y salidas (Input/Output), selecciona los puertos MIDI virtuales de tu Traktor Kontrol X1.

---

## 🎛️ Configuración del Controller Editor (Native Instruments)

Para que el hardware se comunique correctamente con este script de Python, debes usar la aplicación **Controller Editor** de Native Instruments y asegurarte de lo siguiente:

1. **Modo MIDI:** El controlador debe estar enviando mensajes MIDI estándar (normalmente activando el modo MIDI en el X1).
2. **Canal MIDI:** Todos los botones y perillas deben estar configurados para enviar datos por el **Canal 2** (En el código de Ableton esto se lee como `CHANNEL = 1`).
3. **Tipo de Botones:** Los botones deben estar en modo **Gate** (envían 127 al presionar, 0 al soltar). El código de Ableton se encarga del comportamiento de encendido/apagado.
4. **Encoders (Perillas 16, 17, 26, 27):** Deben estar configurados en modo **Relative** (por ejemplo, *Relative (7-Bit)* o *Two's Complement*). Si están en modo *Absolute*, el zoom y el scroll dejarán de funcionar al llegar al límite (0 o 127).

---

## 🗺️ Mapeos Actuales (Current Mappings)

Template **Basic** del Controller Editor, todo por el **Canal MIDI 2**. Cada deck tiene un tema: el izquierdo **reproduce** y el derecho **graba**.

### 1. Deck izquierdo — Reproducir
| Botón | CC | Función |
|---|---|---|
| PLAY | 40 | Play / Pausa |
| SYNC | 42 | Metrónomo |
| CUE | 36 | Stop (2 veces = volver al inicio) |
| CUP | 38 | Tap Tempo |
| ◀ BEAT / BEAT ▶ | 32 / 34 | Rebobinar / Avanzar (mantener) |
| IN | 28 | Loop on/off |
| OUT | 30 | Follow (la vista sigue la reproducción) |

### 2. Deck derecho — Grabar
| Botón | CC | Función |
|---|---|---|
| PLAY | 41 | Grabar en Arrangement ● |
| SYNC | 43 | Grabar en Session |
| CUE | 37 | Automation Arm |
| CUP | 39 | Re-enable Automation |
| ◀ BEAT / BEAT ▶ | 33 / 35 | Undo / Redo |
| IN | 29 | Capture MIDI |
| OUT | 31 | Arrangement Overdub (MIDI +) |

### 3. Botones FX — Vistas
| Botón | CC | Función |
|---|---|---|
| FX1 izq. | 20 | Mostrar / ocultar Browser |
| FX2 izq. | 22 | Session ⇄ Arrangement |
| FX1 der. | 21 | Mostrar / ocultar vista Clip |
| FX2 der. | 23 | Mostrar / ocultar vista Devices |

### 4. Encoders inferiores — Browser
Cualquier giro o push le da el foco al Browser (ya no hace falta hacer click en él).

| Control | CC | Función |
|---|---|---|
| Giro izq. | 26 | Subir / bajar |
| Push izq. | 24 | Cargar lo seleccionado (si es carpeta, la abre) |
| Giro der. | 27 | Cerrar / abrir carpeta |
| Push der. | 25 | Preescuchar |

### 5. Encoders superiores — Arrangement
| Control | CC | Función |
|---|---|---|
| Giro izq. | 16 | Zoom |
| Giro der. | 17 | Mover izquierda / derecha |

### 6. Sección superior — Device seleccionado
Las perillas controlan el device que tiene la "mano azul" (sigue a la pista y al device seleccionados). En los botones ON y 1, la columna izquierda va **hacia atrás** y la derecha **hacia adelante**. Los botones 2 y 3 navegan: a la izquierda **devices**, a la derecha **pistas** (2 = anterior, 3 = siguiente).

| Control | CC | Función |
|---|---|---|
| 8 perillas | 0–7 | Parámetros 1–8 del device (orden de lectura: izq→der, arriba→abajo) |
| ON izq. / ON der. | 8 / 9 | Encender/apagar device / Armar pista seleccionada |
| 1 izq. / 1 der. | 10 / 11 | Banco de parámetros anterior / siguiente |
| 2 izq. / 3 izq. | 12 / 14 | Device anterior / siguiente |
| 2 der. / 3 der. | 13 / 15 | Pista anterior / siguiente |

**Modo de las perillas** (usa la página *Shift* del template, manteniendo SHIFT):

| Control | CC | Función |
|---|---|---|
| SHIFT + ON izq. | 52 | Perillas = **macros / parámetros** del device (modo por defecto) |
| SHIFT + ON der. | 53 | Perillas = **sends A–H** de la pista seleccionada |

En modo Sends las perillas siguen a la pista seleccionada; si la pista tiene menos returns, las perillas sobrantes no hacen nada.

Para cambiar una asignación, edita las constantes `CC_*` al inicio de `TraktorKontrolX1.py`. Para depurar, pon `DEBUG_MIDI = True` y el script escribirá en `Log.txt` todo el MIDI que recibe.

---

## 💡 ¿Por qué podría no estar funcionando?

Si ya probaste el código y no hace nada, revisa este checklist:
1. **¿Reiniciaste Ableton?** Los scripts no se recargan "en vivo" a menos que tengas un entorno de desarrollo específico activo.
2. **Errores de sintaxis:** Si Ableton encuentra un error en el archivo `.py`, no cargará el script. Ableton genera un archivo `Log.txt` (en `%appdata%\Ableton\Live 12.x\Preferences\Log.txt` en Windows) donde puedes ver por qué falló la carga del script.
3. **Selección en Preferencias:** ¿Aparece tu script en el menú de Control Surfaces? Si no aparece, la carpeta está mal ubicada, faltan archivos base, o hubo un error al compilar el Python al iniciar Live.
4. **Modo del hardware:** El Traktor X1 tiene su modo nativo (que se comunica con Traktor) y su modo MIDI. Verifica que está en modo MIDI (los LEDs suelen cambiar o apagarse esperando comandos MIDI).