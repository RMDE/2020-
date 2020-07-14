'''
author : RMDE
function : os function
'''

import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
import os


# 错误信息
def Error(win,text):
    QMessageBox.critical(win,"错误",text)
    return True;

# 选择信息
def Question(win,text):
    reply = QMessageBox.question(win,"选择",text,QMessageBox.Ok|QMessageBox.Cancel)
    if reply==QMessageBox.Ok:
        return True
    else:
        return False

# 提示信息
def Info(win,text):
    QMessageBox.information(win,"提示",text)
    return True;

# 警告信息
def Warn(win,text):
    QMessageBox.information(win,"警告",text,QMessageBox.Ok|QMessageBox.Cancel)
    if reply==QMessageBox.Ok:
        return True
    else:
        return False
if __name__=='__main__':
    Load("Icon.jpg")
