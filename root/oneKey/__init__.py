#!/usr/bin/python
# -*- coding:utf-8 -*-
# Autor: PengCheng 
# E-mail: southAngel@126.com 
# Time: 2018-09-04 23:00 
from maya import mel
from . import listUi

SWIN = listUi.IndexMain()

def bindShortcut():
    script_mel = '''
if (!`runTimeCommand -q -ex OneKeyTool`){
runTimeCommand
	-annotation ""
	-category "Custom Scripts"
	-hotkeyCtx ""
	-commandLanguage "python"
	-command ("import SouAng.root.smenuSet as SouAngm\\nSouAngm.oneKeyShow()")
	OneKeyTool;
nameCommand -ann "OneKeyToolNameCommand" -command ("OneKeyTool") OneKeyToolNameCommand;
hotkey -keyShortcut "f" -ctl -name ("OneKeyToolNameCommand");
}
    '''
    mel.eval(script_mel)

bindShortcut()
