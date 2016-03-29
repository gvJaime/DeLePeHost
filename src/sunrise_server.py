#!/usr/bin/env python

from rainbow import register, publish, run
from DLP_Printer.DLP_Printer import DLP_Printer
import os.path



@register
def save_file(name='name', content='content'):
    with open(name, 'w') as file_:
        import base64
        file_.write(base64.b64decode(content))
        return "OK"


@register
def moveAxis(amount=0):
    a='G1 Y' + str(amount) + ' F200 \n\r'
    sunrise.mechComm.write('G91\n\r')
    sunrise.mechComm.write(a)
    response='Moving Y axis by ' + str(amount) + ' mm.'
    return response

@register
def unlockMech():
    sunrise.mechComm.write("$x\r\n")
    answer = sunrise.mechComm.getData();
    if "ok" in answer:
        return "Alarm lock successfully released"
    else:
        return "ERROR: Communication could't be established with cnc board"

@register
def sliceFile(name='name', content='content'):
    global loaded
    try:
        os.mkdir('temp')
    except Exception:
        pass
    temp_stl_path=os.path.join(os.getcwd(),'temp','loaded.stl')
    print temp_stl_path
    with open(temp_stl_path, 'w') as file_:
        import base64
        file_.write(base64.b64decode(content))
        sunrise.slicer.file_to_svg(temp_stl_path,50)
        response = name + " successfully sliced"
        loaded=True
        return response

@register
def buildPrint():
    global loaded
    if not loaded:
        return "Print will not happen"
    else:
        sunrise.buildPrint(os.path.join(os.getcwd(),'temp','loaded.svg'),{'exposeTime':20000,'blankTime':500})

if __name__ == '__main__':
    sunrise=DLP_Printer()
    sunrise.projector.blank()
    global loaded
    loaded=False
    try:
        os.rmdir("./temp")
    except:
        pass

    run(host='0.0.0.0', webserver=True)
