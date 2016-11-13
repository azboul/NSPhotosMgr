#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from os.path import isfile, join
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Editor(QDialog):
	def __init__(self):
		super(Editor, self).__init__()
		self.setupUi()

	def setupUi(self):
		Layout = QVBoxLayout()
		self.setLayout(Layout)
		
		self.tabWidget = QTabWidget(self)
		Layout.addWidget(self.tabWidget)
				
		self.PictMoveTab = QWidget()
		self.PictMoveLayout = QHBoxLayout()
		self.PictMoveTab.setLayout(self.PictMoveLayout)
				
		self.PictMoveParam = QWidget(self.PictMoveTab)
		self.PictMoveLayout.addWidget(self.PictMoveParam, 2)
		gridLayout = QGridLayout()
		self.PictMoveParam.setLayout(gridLayout)
		self.MoveInitDir = QLineEdit(self.PictMoveParam)
		self.MoveInitButton = QPushButton("Choisir dossier")
		self.MoveInitButton.clicked.connect(self.movePict_loadPictures)
		self.MovePicList = QListWidget(self.PictMoveParam)
		gridLayout.addWidget(self.MoveInitDir, 0, 0, 1, 2)
		gridLayout.addWidget(self.MoveInitButton, 0, 2)
		gridLayout.addWidget(self.MovePicList, 1, 0, 1, 3)
		self.PictMoveLabel = QLabel(self.PictMoveTab)
		self.PictMoveLabel.setText("Picture preview")
		self.PictMoveKeys = QTableWidget(self.PictMoveParam)
		self.PictMoveKeys.setColumnCount(2)
		self.PictMoveKeys.setRowCount(10)		
		headerLabels = ["Sous-dossier", "Touche clavier"]
		self.PictMoveKeys.setHorizontalHeaderLabels(headerLabels)
		self.PictMoveKeys.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.PictMoveKeys.setSelectionMode(QAbstractItemView.SingleSelection)
		gridLayout.addWidget(self.PictMoveKeys, 2, 0)
		
		self.PictMoveLabel.installEventFilter(self)		

		self.PictMoveLayout.addWidget(self.PictMoveLabel, 3)
		self.tabWidget.addTab(self.PictMoveTab, "Moving Pictures")
		
	def movePict_loadPictures(self):
		picturePath = QFileDialog.getExistingDirectory(self.MoveInitButton, "Choisir un dossier")
		if not picturePath:
			return
		self.MovePicList.clear()
		self.MoveInitDir.setText(picturePath)
		row=0
		onlyfiles = [f for f in os.listdir(picturePath) if isfile(join(picturePath, f)) and f.endswith(".JPG")]
		for f in onlyfiles:
			item = QListWidgetItem()
			item.setText(os.path.basename(f))
			self.MovePicList.insertItem(row,item)
			row = row+1
			
	def	keyPressEvent (self, keyEvent):
		print("Touche "+ (keyEvent.text()))
		super(Editor, self).keyPressEvent(keyEvent)
		
	def eventFilter(self, obj, event):
	 if obj == self.PictMoveLabel:
	 	if event.type() == QEvent.KeyPress:
	 		print(keyEvent.text())

if __name__ == '__main__':
	app = QApplication(sys.argv)
	editor = Editor()
	editor.showMaximized()
	sys.exit(app.exec_())
