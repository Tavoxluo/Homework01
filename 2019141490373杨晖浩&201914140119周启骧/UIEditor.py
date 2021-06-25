# -*- coding: utf-8 -*-

# 文本编辑器模块


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class TextEditor(object):
    # 文本编辑器模块
    def __init__(self):
        # 内容
        self.content = ''
        # 当前字体
        self.cfont = ''
        self.pause = False
        self.bsize = 36

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(950, 600)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        # 剪切
        self.cutbutton = QtWidgets.QPushButton(Form)
        self.cutbutton.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.cutbutton.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.cutbutton.setObjectName("cutbutton")
        self.cutbutton.clicked.connect(self.fileCut)
        self.gridLayout.addWidget(self.cutbutton, 0, 0, 2, 1)
        # 复制
        self.copybutton = QtWidgets.QPushButton(Form)
        self.copybutton.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.copybutton.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.copybutton.setObjectName("copybutton")
        self.copybutton.clicked.connect(self.fileCopy)
        self.gridLayout.addWidget(self.copybutton, 0, 1, 2, 1)
        # 粘贴
        self.pastebutton = QtWidgets.QPushButton(Form)
        self.pastebutton.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.pastebutton.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.pastebutton.setObjectName("pastebutton")
        self.pastebutton.clicked.connect(self.filePaste)
        self.gridLayout.addWidget(self.pastebutton, 0, 2, 2, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setMinimumSize(QtCore.QSize(10, self.bsize))
        self.line.setMaximumSize(QtCore.QSize(10, self.bsize))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 3, 2, 1)
        # 后退
        self.bbackward = QtWidgets.QPushButton(Form)
        self.bbackward.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bbackward.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bbackward.setObjectName("bbackward")
        self.bbackward.clicked.connect(self.fileUndo)
        self.gridLayout.addWidget(self.bbackward, 0, 4, 2, 1)
        # 前进
        self.bforward = QtWidgets.QPushButton(Form)
        self.bforward.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bforward.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bforward.setObjectName("bforward")
        self.bforward.clicked.connect(self.fileRedo)
        self.gridLayout.addWidget(self.bforward, 0, 5, 2, 1)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setMinimumSize(QtCore.QSize(10, self.bsize))
        self.line_2.setMaximumSize(QtCore.QSize(10, self.bsize))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 0, 6, 2, 1)
        # 加粗
        self.bbold = QtWidgets.QPushButton(Form)
        self.bbold.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bbold.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bbold.toggled.connect(self.fileBold)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.bbold.setFont(font)
        self.bbold.setCheckable(True)
        self.bbold.setObjectName("bbold")
        self.gridLayout.addWidget(self.bbold, 0, 7, 2, 1)
        # 斜体
        self.bitalic = QtWidgets.QPushButton(Form)
        self.bitalic.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bitalic.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bitalic.toggled.connect(self.fileItalic)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(self.bsize)
        self.bitalic.setFont(font)
        self.bitalic.setCheckable(True)
        self.bitalic.setObjectName("bitalic")
        self.gridLayout.addWidget(self.bitalic, 0, 8, 2, 1)
        # 下划线
        self.bunderline = QtWidgets.QPushButton(Form)
        self.bunderline.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bunderline.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bunderline.toggled.connect(self.fileUnderline)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setUnderline(True)
        self.bunderline.setFont(font)
        self.bunderline.setObjectName("bunderline")
        self.bunderline.setCheckable(True)
        self.gridLayout.addWidget(self.bunderline, 0, 9, 2, 1)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setMinimumSize(QtCore.QSize(10, self.bsize))
        self.line_3.setMaximumSize(QtCore.QSize(10, self.bsize))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 0, 10, 2, 1)
        # 字体框
        self.bfont = QtWidgets.QPushButton(Form)
        self.bfont.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bfont.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bfont.clicked.connect(self.fileFontBox)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.bfont.setFont(font)
        self.bfont.setObjectName("bfont")
        self.gridLayout.addWidget(self.bfont, 0, 11, 2, 1)
        # 颜色选择框
        self.bcolor = QtWidgets.QPushButton(Form)
        self.bcolor.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bcolor.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bcolor.clicked.connect(self.fileColorBox)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        self.bcolor.setFont(font)
        self.bcolor.setObjectName("bcolor")
        self.gridLayout.addWidget(self.bcolor, 0, 12, 2, 1)
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setMinimumSize(QtCore.QSize(10, self.bsize))
        self.line_4.setMaximumSize(QtCore.QSize(10, self.bsize))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 0, 13, 2, 1)
        # 左对齐
        self.bleft = QtWidgets.QPushButton(Form)
        self.bleft.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bleft.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bleft.clicked.connect(self.fileLeft)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.bleft.setFont(font)
        self.bleft.setObjectName("bleft")
        self.gridLayout.addWidget(self.bleft, 0, 14, 2, 1)
        # 居中对齐
        self.bmiddle = QtWidgets.QPushButton(Form)
        self.bmiddle.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bmiddle.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bmiddle.clicked.connect(self.fileCenter)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.bmiddle.setFont(font)
        self.bmiddle.setObjectName("bmiddle")
        self.gridLayout.addWidget(self.bmiddle, 0, 15, 2, 1)
        # 右对齐
        self.bright = QtWidgets.QPushButton(Form)
        self.bright.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bright.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.bright.clicked.connect(self.fileRight)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.bright.setFont(font)
        self.bright.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.bright, 0, 16, 2, 1)
        # 搜索文本
        self.blook = QtWidgets.QPushButton(Form)
        self.blook.setMinimumSize(QtCore.QSize(self.bsize, self.bsize))
        self.blook.setMaximumSize(QtCore.QSize(self.bsize, self.bsize))
        self.blook.clicked.connect(self.fileSearch)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.blook.setFont(font)
        self.blook.setObjectName("blook")
        self.gridLayout.addWidget(self.blook, 0, 17, 2, 1)
        # 查看HTML
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.toggled.connect(self.checkBoxChecked)
        self.gridLayout.addWidget(self.checkBox, 0, 18, 1, 1)
        # 字体下拉选择框
        self.fontComboBox = QtWidgets.QFontComboBox(Form)
        self.fontComboBox.setMinimumSize(QtCore.QSize(100, 20))
        self.fontComboBox.setMaximumSize(QtCore.QSize(200, 20))
        self.fontComboBox.setObjectName("fontComboBox")
        self.fontComboBox.currentFontChanged.connect(self.fileChangeFont)
        self.gridLayout.addWidget(self.fontComboBox, 1, 18, 1, 1)
        # 文本编辑框
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.cursorPositionChanged.connect(self.textChanged)
        self.cfont = self.textEdit.currentFont()
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 19)
        # 初始化
        self.retranslateUi(Form)
        self.checkBoxChecked()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "TextEditor"))
        self.cutbutton.setIcon(QtGui.QIcon('img/cut.png'))
        self.cutbutton.setToolTip('剪切(Ctrl+x)')
        self.cutbutton.setShortcut('Ctrl+x')
        self.copybutton.setIcon(QtGui.QIcon('img/copy.png'))
        self.copybutton.setToolTip('复制(Ctrl+c)')
        self.copybutton.setShortcut('Ctrl+c')
        self.pastebutton.setIcon(QtGui.QIcon('img/paste.png'))
        self.pastebutton.setToolTip('粘贴(Ctrl+v)')
        self.pastebutton.setShortcut('Ctrl+v')
        self.bbackward.setIcon(QtGui.QIcon('img/backward.png'))
        self.bforward.setIcon(QtGui.QIcon('img/forward.png'))
        self.bbold.setIcon(QtGui.QIcon('img/bold.png'))
        self.bitalic.setIcon(QtGui.QIcon('img/italic.png'))
        self.bunderline.setIcon(QtGui.QIcon('img/underline.png'))
        self.bfont.setIcon(QtGui.QIcon('img/font.png'))
        self.bfont.setToolTip('字体')
        self.bcolor.setIcon(QtGui.QIcon('img/color.png'))
        self.bcolor.setToolTip('颜色')
        self.bleft.setIcon(QtGui.QIcon('img/left.png'))
        self.bmiddle.setIcon(QtGui.QIcon('img/center.png'))
        self.bright.setIcon(QtGui.QIcon('img/right.png'))
        self.blook.setIcon(QtGui.QIcon('img/look.png'))
        self.blook.setToolTip('搜索')
        self.checkBox.setText(_translate("Form", "查看html"))

    # 按钮功能实现
    def fileFontBox(self):
        font, okPressed = QFontDialog.getFont()
        if okPressed:
            self.textEdit.setCurrentFont(font)

    def fileColorBox(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.textEdit.setTextColor(col)

    def fileLeft(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def fileRight(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def fileCenter(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def fileChangeFont(self, font):
        self.textEdit.setCurrentFont(font)

    def fileSearch(self):
        msgBox = QWidget()
        pattern, okPressed = QtWidgets.QInputDialog.getText(msgBox, "查找", "查找字符串:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and pattern != '':
            sub = self.textEdit
            sub.moveCursor(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            if sub.find(pattern):
                palette = sub.palette()
                palette.setColor(QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
                sub.setPalette(palette)

    def fileBold(self):
        sub = self.textEdit
        tmpFormat = sub.currentCharFormat()
        if tmpFormat.fontWeight() == QtGui.QFont.Bold:
            tmpFormat.setFontWeight(QtGui.QFont.Normal)
        else:
            tmpFormat.setFontWeight(QtGui.QFont.Bold)
        sub.mergeCurrentCharFormat(tmpFormat)

    def fileItalic(self):
        tmpTextBox = self.textEdit
        tmpTextBox.setFontItalic(not tmpTextBox.fontItalic())

    def fileUnderline(self):
        tmpTextBox = self.textEdit
        tmpTextBox.setFontUnderline(not tmpTextBox.fontUnderline())

    def fileCopy(self):
        self.textEdit.copy()

    def fileCut(self):
        self.textEdit.cut()

    def filePaste(self):
        self.textEdit.paste()

    def fileRedo(self):
        self.textEdit.redo()

    def fileUndo(self):
        self.textEdit.undo()

    def textChanged(self):
        if self.pause:
            pass
        else:
            self.cfont = self.textEdit.currentFont()
            self.content = self.textEdit.toHtml()

    def getContent(self):
        # 返回内容
        return self.content

    def checkBoxChecked(self):
        if self.checkBox.isChecked():
            self.pause = True
            self.textEdit.clear()
            self.textEdit.setPlainText(self.content)
        else:
            self.textEdit.clear()
            self.textEdit.setHtml(self.content)
            self.textEdit.setCurrentFont(self.cfont)
            self.pause = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()
    mw = TextEditor()
    mw.setupUi(win)
    win.show()
    sys.exit(app.exec_())
