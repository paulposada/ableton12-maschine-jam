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

## 🗺️ Mapeos Actuales (Diagrama Visual)

> 💡 **¿Prefieres una referencia gráfica completa?**  
> Consulta la **[Guía Visual del Mapeo (GUIA_VISUAL.md)](GUIA_VISUAL.md)** o abre la imagen vectorial **[traktor_x1_layout.svg](traktor_x1_layout.svg)**.

Template **Basic** del Controller Editor, todo por el **Canal MIDI 2**.

![Diagrama Visual Traktor Kontrol X1](traktor_x1_layout.svg)

### 📐 Esquema Rápido del Controlador

```text
  [ CC 8 ] (Device On/Off)      (( CC 0 )) (( CC 1 ))      [ CC 9 ] (Armar Pista)
  [ CC 10 ] (◀ Banco Prev)      (( CC 2 )) (( CC 3 ))      [ CC 11 ] (Banco Next ▶)
  [ CC 12 ] (◀ Device Prev)     (( CC 4 )) (( CC 5 ))      [ CC 13 ] (◀ Pista Prev)
  [ CC 14 ] (Device Next ▶)     (( CC 6 )) (( CC 7 ))      [ CC 15 ] (Pista Next ▶)
 -----------------------------------------------------------------------------------
  (( CC 16 )) Zoom Arr.              [ SHIFT ]             (( CC 17 )) Scroll Arr.
 -----------------------------------------------------------------------------------
  [ CC 20 ] Toggle Browser    [ CC 22 ] Sess ⇄ Arr   |   [ CC 21 ] Clip   [ CC 23 ] Devices
 -----------------------------------------------------------------------------------
  (( CC 26 )) Browser Scroll (Push 24: Cargar)   |   (( CC 27 )) Carpeta (Push 25: Preescucha)
 ===================================================================================
        DECK IZQUIERDO (REPRODUCCIÓN)        |       DECK DERECHO (GRABACIÓN)
 --------------------------------------------+--------------------------------------
  [ CC 28 ] Loop       [ CC 30 ] Follow      |   [ CC 29 ] Capture    [ CC 31 ] Overdub
  [ CC 32 ] ◀ Rebobinar [ CC 34 ] Avanzar ▶  |   [ CC 33 ] ↩ Undo     [ CC 35 ] Redo ↪
  [ CC 36 ] ⏹ Stop     [ CC 38 ] Tap Tempo   |   [ CC 37 ] Auto Arm   [ CC 39 ] Re-enable Auto
  [ CC 40 ] ▶ Play     [ CC 42 ] Metrónomo   |   [ CC 41 ] ● Rec Arr. [ CC 43 ] ● Rec Sess.
```

---

### 1. Deck izquierdo — Reproducción (Transporte)
| Botón Hardware | CC | Función en Ableton Live | Comportamiento LED |
|---|---|---|---|
| **PLAY** | 40 | Play / Pausa | Encendido cuando la canción está reproduciéndose |
| **SYNC** | 42 | Metrónomo On / Off | Refleja el estado del metrónomo en Live |
| **CUE \| REL** | 36 | Stop (**2 pulsaciones** = volver al compás 1.1.1) | Feedback momentáneo al pulsar |
| **CUP \| ABS** | 38 | Tap Tempo | Parpadea con las pulsaciones de tap |
| **◀ BEAT** | 32 | Rebobinar en Arrangement | Encendido mientras se mantiene pulsado |
| **BEAT ▶** | 34 | Avanzar en Arrangement | Encendido mientras se mantiene pulsado |
| **IN** | 28 | Loop Activo / Inactivo | Encendido si el loop de Arrangement está activado |
| **OUT \| 4** | 30 | Follow (la vista sigue al cabezal) | Encendido si Follow está activado en Live |

---

### 2. Deck derecho — Grabación y Edición
| Botón Hardware | CC | Función en Ableton Live | Comportamiento LED |
|---|---|---|---|
| **PLAY** | 41 | Grabar en Arrangement (●) | Encendido cuando la grabación global está activa |
| **SYNC** | 43 | Grabar en Session | Encendido cuando Session Record está activo |
| **CUE \| REL** | 37 | Automation Arm | Refleja si la automatización está armada |
| **CUP \| ABS** | 39 | Re-enable Automation | Encendido si hay automatizaciones sobreescritas pendientes |
| **◀ BEAT** | 33 | Deshacer (**Undo**) | Momentáneo al pulsar |
| **BEAT ▶** | 35 | Rehacer (**Redo**) | Momentáneo al pulsar |
| **IN** | 29 | **Capture MIDI** (recupera notas improvisadas) | Encendido si hay material disponible para capturar |
| **OUT \| 4** | 31 | Arrangement Overdub (MIDI +) | Refleja estado de MIDI Overdub |

---

### 3. Botones FX — Conmutación de Vistas
| Botón Hardware | CC | Función en Ableton Live | Comportamiento LED |
|---|---|---|---|
| **FX 1 (izq)** | 20 | Mostrar / ocultar Browser | Encendido si el navegador está visible |
| **FX 2 (izq)** | 22 | Alternar vista Session ⇄ Arrangement | Encendido en Arrangement, apagado en Session |
| **FX 1 (der)** | 21 | Mostrar / ocultar vista Clip / Detalle | Encendido si la vista Clip está abierta |
| **FX 2 (der)** | 23 | Mostrar / ocultar vista Devices | Encendido si la cadena de Devices está visible |

---

### 4. Encoders inferiores — Navegación del Browser (Autofocus)
*Cualquier acción sobre estos encoders da el foco automáticamente al Browser sin usar el ratón.*

| Control Hardware | CC | Acción | Función en Ableton Live |
|---|---|---|---|
| **Giro Izquierdo** | 26 | Giro relativo | Mover selección hacia arriba o hacia abajo en la lista |
| **Push Izquierdo** | 24 | Presionar | **Cargar elemento seleccionado** (si es carpeta, la abre) |
| **Giro Derecho** | 27 | Giro relativo | **Cerrar (izq) o Abrir (der)** carpetas en el árbol |
| **Push Derecho** | 25 | Presionar | **Preescuchar** sample seleccionado (Prehear / Preview) |

---

### 5. Encoders superiores — Vista Arrangement
| Control Hardware | CC | Acción | Función en Ableton Live |
|---|---|---|---|
| **Giro Izquierdo** | 16 | Giro relativo | **Zoom Horizontal** (acercar / alejar la línea de tiempo) |
| **Giro Derecho** | 17 | Giro relativo | **Scroll Horizontal** (desplazarse a izquierda / derecha) |

---

### 6. Sección Superior — Dispositivo (Device) y Pistas (Track)
Las 8 perillas controlan automáticamente el dispositivo que tiene la **"mano azul"** en Live.

| Control Hardware | CC | Función en Ableton Live |
|---|---|---|
| **8 Perillas (CC 0–7)** | 0–7 | Parámetros 1 a 8 del Device (orden: fila 1 [0,1], fila 2 [2,3], fila 3 [4,5], fila 4 [6,7]) |
| **ON (izq)** | 8 | Encender / apagar dispositivo seleccionado |
| **ON (der)** | 9 | Armar para grabación la pista seleccionada |
| **1 (izq) / 1 (der)** | 10 / 11 | Banco de parámetros anterior (◀) / siguiente (▶) |
| **2 (izq) / 3 (izq)** | 12 / 14 | Dispositivo anterior (◀) / siguiente (▶) en la cadena |
| **2 (der) / 3 (der)** | 13 / 15 | Pista anterior (◀) / siguiente (▶) en el set |

#### 🔄 Modos Alternativos de las Perillas (Página Shift)
Manteniendo presionado el botón **SHIFT** del hardware:

| Combinación | CC | Función |
|---|---|---|
| **SHIFT + ON (izq)** | 52 | Las 8 perillas controlan **Macros / Parámetros** del Device (modo por defecto) |
| **SHIFT + ON (der)** | 53 | Las 8 perillas controlan los **Sends A–H** de la pista seleccionada |

> En modo Sends, las perillas mapean dinámicamente a los canales de Retorno activos en Live.

---

### 7. LEDs y Diagnóstico
Al cargar el script, **todos los LEDs se encienden medio segundo** (prueba de que el X1 recibe el feedback) y luego muestran el estado real:

* **Estado de Live:** Play, Metrónomo, Loop, Rec, Session Rec, Overdub, Automation Arm/Re-enable, Device on/off, Follow, Arm de la pista, Capture MIDI (encendido si hay algo que capturar), vistas visibles (Browser, Arrangement, Clip, Devices) y modo de perillas (SHIFT + ON).
* **Botones de acción** (Undo/Redo, navegación de devices/pistas, bancos, Tap): se encienden mientras los mantienes presionados.

Requisitos en el Controller Editor: cada botón con **LED On: For MIDI In**, y en Ableton el **Output** del Control Surface en `Traktor Kontrol X1 - 2`.

---

## 🧩 Estructura del código

| Archivo | Responsabilidad |
|---|---|
| `__init__.py` | Punto de entrada de Live (`create_instance`) |
| `TraktorKontrolX1.py` | Ensambla todas las piezas, una sección del controlador por método `_setup_*` |
| `config.py` | Canal, modos MIDI y **mapa de CC** agrupado por sección (aquí se reasignan los controles) |
| `elements.py` | Fábrica de botones, encoders y perillas |
| `actions.py` | Botón → acción (patrón Command) con su LED |
| `feedback.py` | LEDs que reflejan estados de Live |
| `listeners.py` | Registro de listeners para desconectarlos limpiamente |
| `song_actions.py` | Undo/Redo, Capture MIDI, Follow, Arm |
| `selection.py` | Pista / device anterior y siguiente |
| `knob_modes.py` | Modos de las perillas: Macros ⇄ Sends (patrón State) |
| `browser.py` / `arrangement.py` | Componentes de los encoders |
| `views.py` / `navigation.py` | Utilidades de vistas y de navegación |
| `live_keys.py` + `send_keys.vbs` | Envío de Enter/→ a Live para cargar y preescuchar (solo Windows) |
| `midi_debug.py` | Depuración de MIDI (`DEBUG_MIDI` en `config.py`) |

Al instalar, copia **toda la carpeta** (todos los `.py` y `send_keys.vbs`).

---

## 💡 ¿Por qué podría no estar funcionando?

Si ya probaste el código y no hace nada, revisa este checklist:
1. **¿Reiniciaste Ableton?** Los scripts no se recargan "en vivo" a menos que tengas un entorno de desarrollo específico activo.
2. **Errores de sintaxis:** Si Ableton encuentra un error en el archivo `.py`, no cargará el script. Ableton genera un archivo `Log.txt` (en `%appdata%\Ableton\Live 12.x\Preferences\Log.txt` en Windows) donde puedes ver por qué falló la carga del script.
3. **Selección en Preferencias:** ¿Aparece tu script en el menú de Control Surfaces? Si no aparece, la carpeta está mal ubicada, faltan archivos base, o hubo un error al compilar el Python al iniciar Live.
4. **Modo del hardware:** El Traktor X1 tiene su modo nativo (que se comunica con Traktor) y su modo MIDI. Verifica que está en modo MIDI (los LEDs suelen cambiar o apagarse esperando comandos MIDI).