' Uso: wscript.exe //nologo //B send_keys.vbs <PID de Live> <teclas>
' Activa la ventana de Ableton Live por su PID y le envia las teclas.
' Si no logra activar Live, no envia nada (para no escribir en otra aplicacion).
Option Explicit
Dim shell
If WScript.Arguments.Count < 2 Then WScript.Quit 1
Set shell = CreateObject("WScript.Shell")
If shell.AppActivate(CLng(WScript.Arguments(0))) Then
    WScript.Sleep 30
    shell.SendKeys WScript.Arguments(1)
End If
