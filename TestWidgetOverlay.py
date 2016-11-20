#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from WidgetOverlay import WidgetOverlay

def MakeWidgetOverlay(parent, widget):
	editorWidget = WidgetOverlay()
	editorWidget.SetWidget(widget)
	editorWidget.setMouseTracking(True)
	return editorWidget

if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = QDialog()
	dialog.setLayout(QVBoxLayout())
	dialog.layout().setContentsMargins(0,0,0,0)
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QPushButton()))
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QPushButton()))
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QLineEdit()))    
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QPushButton()))        
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QLineEdit()))
	dialog.layout().addWidget(MakeWidgetOverlay(dialog, QTableWidget()))	
	dialog.layout().addStretch()

	dialog.show()
	sys.exit(app.exec_())