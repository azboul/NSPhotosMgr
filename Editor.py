#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from os.path import isfile, join
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import xmlrpc.client

class Editor(QDialog):
	def __init__(self):
		super(Editor, self).__init__()
		self.setupUi()

	def setupUi(self):
		Layout = QVBoxLayout()
		self.setLayout(Layout)
		
		self.tabWidget = QTabWidget(self)
		Layout.addWidget(self.tabWidget)

		#		
		# Move pictures section
		# 
		self.PictMoveTab = QWidget()
		self.PictMoveLayout = QHBoxLayout()
		self.PictMoveTab.setLayout(self.PictMoveLayout)
				
		self.PictMoveParam = QWidget(self.PictMoveTab)
		self.PictMoveLayout.addWidget(self.PictMoveParam, 2)
		gridLayout = QGridLayout()
		self.PictMoveParam.setLayout(gridLayout)
		self.MoveInitDir = QLineEdit(self.PictMoveParam)
		self.MoveInitButton = QPushButton("Choisir dossier")
		self.MoveInitButton.clicked.connect(self.OnLoadAllPictures)
		self.MovePicList = QListWidget(self.PictMoveParam)
		self.MovePicList.setObjectName("movePicList")
		self.MovePicList.setSelectionMode(QAbstractItemView.SingleSelection)
		self.MovePicList.currentItemChanged.connect(self.onCurrentPictChanged)
		gridLayout.addWidget(self.MoveInitDir, 0, 0, 1, 2)
		gridLayout.addWidget(self.MoveInitButton, 0, 2)
		gridLayout.addWidget(self.MovePicList, 1, 0, 1, 3)

		self.PictMoveLabel = QLabel(self.PictMoveTab)
		self.PictMoveLabel.setText("Picture preview")
		
		self.groupBox = QGroupBox(self.PictMoveTab)
		self.groupBox.setTitle("Copier les photos")
		self.groupBox.setLayout(QVBoxLayout())
		gridLayout.addWidget(self.groupBox, 2, 0)
		
		self.moveButtonGroup = QButtonGroup()
		self.moveButtonGroup.buttonClicked.connect(self.onMoveFolderClicked)
		
		self.addButton = QPushButton()
		self.addButton.setText("+")
		self.addButton.clicked.connect(self.AddMoveButton)
		gridLayout.addWidget(self.addButton, 3, 0)
		
		self.PictMoveLayout.addWidget(self.PictMoveLabel, 3)
		self.tabWidget.addTab(self.PictMoveTab, "Moving Pictures")

		#
		# Batch processing
		#

		self.PicProcessTab = QWidget()
		self.PicProcessLayout = QVBoxLayout()
		self.PicProcessTab.setLayout(self.PicProcessLayout)

		self.ServerLayout = QHBoxLayout() 
		self.PicProcessLayout.addLayout(self.ServerLayout)

		self.ConnectButton = QPushButton()
		self.ConnectButton.setText("Connection")
		self.ConnectButton.clicked.connect(self.CheckServerConnection)
		self.ServerLayout.addWidget(self.ConnectButton)

		self.ConnectStatus = QLabel()
		self.ConnectStatus.setText("Pas de connection au server")
		self.ServerLayout.addWidget(self.ConnectStatus)

		self.tabWidget.addTab(self.PicProcessTab, "Pictures Processing")
	
	def OnLoadAllPictures(self):
		picturePath = QFileDialog.getExistingDirectory(self.MoveInitButton, "Choisir un dossier")
		if not picturePath:
			return
		self.ClearMoveData()
		self.MoveInitDir.setText(picturePath)		
		row=0
		onlyfiles = [f for f in os.listdir(picturePath) if isfile(join(picturePath, f)) and f.endswith(".JPG")]
		for f in onlyfiles:
			item = QListWidgetItem()
			item.setText(os.path.basename(f))
			item.setData(Qt.UserRole, join(picturePath, f))
			self.MovePicList.insertItem(row,item)
			row = row+1

	def ClearMoveData(self):
		self.MovePicList.clear()
		self.MoveInitDir.setText("")
			
	def onCurrentPictChanged(self, itemCurrent, itemPrevious):
		if itemCurrent:
			self.LoadPicture(itemCurrent.data(Qt.UserRole))
			
	def LoadPicture(self, path):
		pix = QPixmap(path)
		self.PictMoveLabel.setPixmap(pix.scaled(self.PictMoveLabel.size(), Qt.KeepAspectRatio))
		
	def onMoveFolderClicked(self, button):
		print(button.property("MovePath"))
		
		currentRow = self.MovePicList.currentRow()
		if currentRow == -1:
			return
		
		#currentItem = self.MovePicList.currentItem()
		#path = currentItem.data(Qt.UserRole)
		#imgName = currentItem.text()
		#print(path)
		#print(imgName)
		
		self.MovePicList.setCurrentRow(currentRow+1)
		
	def resizeEvent(self, sizeEvent):
		super(Editor, self).resizeEvent(sizeEvent)
		
	def AddMoveButton(self):
		if not self.MoveInitDir.text():
			return
		
		subFolder = QFileDialog.getExistingDirectory(self.MoveInitButton, "Choisir un dossier pour les photos seront copiées.")
		if not subFolder:
			return

		newMoveButton = QPushButton()
		newMoveButton.setText(subFolder.split('/')[-1])
		newMoveButton.setToolTip(subFolder)
		newMoveButton.setProperty("MovePath", subFolder)
		self.groupBox.layout().addWidget(newMoveButton)
		
		self.moveButtonGroup.addButton(newMoveButton)

	def CheckServerConnection(self):
		self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
		# print(s.pow(2,3))  # Returns 2**3 = 8
		# print(s.add(2,3))  # Returns 5
		# print(s.mul(5,2))  # Returns 5*2 = 10
		if self.server.IsConnect():
			self.ConnectStatus.setText("Connecté au serveur")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	editor = Editor()
	editor.show()
	#editor.showMaximized()
	sys.exit(app.exec_())
