#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from shutil import copy2
from os.path import isfile, join
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import xmlrpc.client

class CustomDelegate(QStyledItemDelegate):
	def __init__(self, parent):
		super(CustomDelegate, self).__init__(parent)
		self.PathList= list()
		
	def paint(self, painter, option, index):
		#super(CustomDelegate, self).paint(painter, option, index)
		painter.save()

		# Background style
		painter.setPen(QPen(Qt.NoPen))
		if option.state & QStyle.State_Selected:
			painter.setBrush(QColor("#3399FF"))
		elif option.state & QStyle.State_Selected:
			painter.setBrush(QColor(Qt.darkBlue))
		else:
			painter.setBrush(QBrush(Qt.white))
		painter.drawRect(option.rect)
		
		# Text style
		text = index.data(Qt.DisplayRole)
		if self.IsInPaths(text):
			painter.setPen(QPen(Qt.lightGray))
			f = painter.font()
			f.setItalic(True)
			painter.setFont(f)
		elif option.state & QStyle.State_Selected or option.state & QStyle.State_MouseOver:
			painter.setPen(QPen(Qt.white))
		else:
			painter.setPen(QPen(Qt.black))
		painter.translate(3, 0)
		painter.drawText(option.rect, Qt.AlignLeft, text)
		
		painter.restore()

	def IsInPaths(self, filename):
		for path in self.PathList:
			if os.path.isfile(join(path, filename)):
				return True
		return False

	def AddPath(self, path):
		self.PathList.append(path)
	

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
		#self.MovePicList = FolderListView()
		self.MovePicList.setObjectName("movePicList")
		self.MovePicList.setSelectionMode(QAbstractItemView.SingleSelection)
		self.delegate = CustomDelegate(self)
		self.MovePicList.setItemDelegateForColumn(0, self.delegate)
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

		self.LoadAllPictures("/home/nico/Images/Photo_Guillaume")
	
	def OnLoadAllPictures(self):
		picturePath = QFileDialog.getExistingDirectory(self.MoveInitButton, "Choisir un dossier")
		if not picturePath:
			return
		LoadAllPictures(picturePath)

	def LoadAllPictures(self, picturePath):
		self.ClearMoveData()
		self.MoveInitDir.setText(picturePath)		
		row=0
		onlyfiles = [f for f in os.listdir(picturePath) if isfile(join(picturePath, f)) and f.endswith(".JPG")]
		
		fileNameList = list()
		for f in onlyfiles:
			fileNameList.append(os.path.basename(f))

		#self.MovePicList.SetList(f)
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
		currentRow = self.MovePicList.currentRow()
		if currentRow == -1:
			return
		currentItem = self.MovePicList.currentItem()		
		fromPath = currentItem.data(Qt.UserRole)
		destPath = button.property("MovePath") + "/"
		
		copy2(fromPath, destPath)
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

		self.delegate.AddPath(subFolder)

	def CheckServerConnection(self):
		self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
		# print(s.pow(2,3))  # Returns 2**3 = 8
		# print(s.add(2,3))  # Returns 5
		# print(s.mul(5,2))  # Returns 5*2 = 10
		if self.server.is_even(14):
			self.ConnectStatus.setText("Connecté au serveur")


if __name__ == '__main__':
	app = QApplication(sys.argv)
	editor = Editor()
	editor.show()
	#editor.showMaximized()
	sys.exit(app.exec_())
