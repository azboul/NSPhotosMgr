#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class WidgetOverlay(QWidget):
		
	# Signal emiited when the close button is pressed
	widgetRemoved = pyqtSignal()

	def __init__( self, parent = None):
		super(WidgetOverlay, self).__init__(parent)
		self.setupUi()

	def setupUi(self):
		self.setLayout(QVBoxLayout())
		self.setObjectName("widgetOverlay")
		
		self.setProperty("SelectMode", False)
		self.setProperty("Selected", False)
		self.setFocusPolicy(Qt.StrongFocus)

		# Configure the close button
		self.m_CloseButton = QToolButton(self)
		self.m_CloseButton.setIcon(QIcon("./resources/CloseIcon.svg"))
		self.m_CloseButton.setStyleSheet("border: none")
		self.m_CloseButton.setToolTip("Remove the element")
		self.m_CloseButton.setIconSize(QSize(16,16))
		self.m_CloseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.m_CloseButton.setFixedSize(QSize(20,20))
		self.m_CloseButton.hide()
		self.m_CloseButton.clicked.connect(self.RemoveWidget)
		#self.m_CloseButton.installEventFilter(self)

	def SetWidget(self,widget):
		self.m_Widget = widget
		self.layout().addWidget(self.m_Widget)
		self.m_Widget.lower()
		self.setFocusProxy(self.m_Widget)
		self.m_Widget.installEventFilter(self)

	def GetWidget(self):
		return self.m_Widget

	def eventFilter(self, object, event):
		if self.m_Widget == object and self.property("SelectMode") == True:
			if event.type() == QEvent.MouseButtonPress:
				print("QEvent.MouseButtonPress " + str(self.property("Selected")))
				return True
			elif event.type() == QEvent.FocusIn:
				print("QEvent.FocusIn " + str(self.property("Selected")))
				self.ToggleSlectionMode()
				return True
			elif event.type() == QEvent.FocusOut:
				print("QEvent.FocusOut " + str(self.property("Selected")))
				self.ToggleSlectionMode()
			elif event.type() == QEvent.MouseButtonRelease:
				print("QEvent.MouseButtonRelease " + str(self.property("Selected")))
				return True
			elif event.type() == QEvent.MouseButtonDblClick:
				print("QEvent.MouseButtonDblClick " + str(self.property("Selected")))
		return super(WidgetOverlay,self).eventFilter(object, event)

	def resizeEvent(self, event):
		self.MoveCloseButton()

	def enterEvent(self, event):
		self.m_CloseButton.show()

	def mousePressEvent(self, event):
		# print("WidgetOverlay : mousePress")
		super(WidgetOverlay, self).mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		# print("WidgetOverlay : mouseRelease")
		super(WidgetOverlay, self).mouseReleaseEvent(event)

	def mouseDoubleClickEvent(self, event):
		# print("WidgetOverlay : mouseDoubleClick")
		super(WidgetOverlay, self).mouseDoubleClickEvent(event)

	def leaveEvent(self, event):
		self.m_CloseButton.hide()
	
	def MoveCloseButton(self):
		pos = self.m_Widget.rect().topRight()
		self.m_CloseButton.move(pos)

	def RemoveWidget(self):
		self.parentWidget().layout().removeWidget(self)
		self.hide()
		self.deleteLater()
		# emit the signal
		self.widgetRemoved.emit()

	def ToggleSlectionMode(self):
		self.setProperty("Selected", not self.property("Selected"))
		self.UpdateStyle()

	def UpdateStyle(self):
		if self.property("Selected") == True:
			self.setStyleSheet("background-color: rgba(0,150,0,10);")
		else:
			self.setStyleSheet("")

def MakeWidgetOverlay(parent, widget):
	editorWidget = WidgetOverlay()
	editorWidget.SetWidget(widget)
	editorWidget.setMouseTracking(True)
	return editorWidget

#def EventName(event):
#    return {
#        0: "QEvent::None",
#        130: "QEvent::AccessibilityDescription",
#        119: "QEvent::AccessibilityHelp",
#        86: "QEvent::AccessibilityPrepare",
#        114: "QEvent::ActionAdded",
#        113: "QEvent::ActionChanged",
#        115: "QEvent::ActionRemoved",
#        99: "QEvent::ActivationChange",
#        121: "QEvent::ApplicationActivate",
#        122: "QEvent::ApplicationDeactivate",
#        36: "QEvent::ApplicationFontChange",
#        37: "QEvent::ApplicationLayoutDirectionChange",
#        38: "QEvent::ApplicationPaletteChange",
#        35: "QEvent::ApplicationWindowIconChange",
#        68: "QEvent::ChildAdded",
#        70: "QEvent::ChildInserted",
#        69: "QEvent::ChildPolished",
#        71: "QEvent::ChildRemoved",
#        40: "QEvent::Clipboard",
#        19: "QEvent::Close",
#        200: "QEvent::CloseSoftwareInputPanel",
#        178: "QEvent::ContentsRectChange",
#        82: "QEvent::ContextMenu",
#        183: "QEvent::CursorChange",
#        52: "QEvent::DeferredDelete",
#        60: "QEvent::DragEnter",
#        62: "QEvent::DragLeave",
#        61: "QEvent::DragMove",
#        63: "QEvent::Drop",
#        98: "QEvent::EnabledChange",
#        10: "QEvent::Enter",
#        150: "QEvent::EnterEditFocus",
#        124: "QEvent::EnterWhatsThisMode",
#        116: "QEvent::FileOpen",
#        8: "QEvent::FocusIn",
#        9: "QEvent::FocusOut",
#        97: "QEvent::FontChange",
#        188: "QEvent::GrabKeyboard",
#        186: "QEvent::GrabMouse",
#        159: "QEvent::GraphicsSceneContextMenu",
#        164: "QEvent::GraphicsSceneDragEnter",
#        166: "QEvent::GraphicsSceneDragLeave",
#        165: "QEvent::GraphicsSceneDragMove",
#        167: "QEvent::GraphicsSceneDrop",
#        163: "QEvent::GraphicsSceneHelp",
#        160: "QEvent::GraphicsSceneHoverEnter",
#        162: "QEvent::GraphicsSceneHoverLeave",
#        161: "QEvent::GraphicsSceneHoverMove",
#        158: "QEvent::GraphicsSceneMouseDoubleClick",
#        155: "QEvent::GraphicsSceneMouseMove",
#        156: "QEvent::GraphicsSceneMousePress",
#        157: "QEvent::GraphicsSceneMouseRelease",
#        182: "QEvent::GraphicsSceneMove",
#        181: "QEvent::GraphicsSceneResize",
#        168: "QEvent::GraphicsSceneWheel",
#        18: "QEvent::Hide",
#        27: "QEvent::HideToParent",
#        127: "QEvent::HoverEnter",
#        128: "QEvent::HoverLeave",
#        129: "QEvent::HoverMove",
#        96: "QEvent::IconDrag",
#        101: "QEvent::IconTextChange",
#        83: "QEvent::InputMethod",
#        6: "QEvent::KeyPress",
#        7: "QEvent::KeyRelease",
#        89: "QEvent::LanguageChange",
#        90: "QEvent::LayoutDirectionChange",
#        76: "QEvent::LayoutRequest",
#        11: "QEvent::Leave",
#        151: "QEvent::LeaveEditFocus",
#        125: "QEvent::LeaveWhatsThisMode",
#        88: "QEvent::LocaleChange",
#        176: "QEvent::NonClientAreaMouseButtonDblClick",
#        174: "QEvent::NonClientAreaMouseButtonPress",
#        175: "QEvent::NonClientAreaMouseButtonRelease",
#        173: "QEvent::NonClientAreaMouseMove",
#        177: "QEvent::MacSizeChange",
#        153: "QEvent::MenubarUpdated",
#        43: "QEvent::MetaCall",
#        102: "QEvent::ModifiedChange",
#        4: "QEvent::MouseButtonDblClick",
#        2: "QEvent::MouseButtonPress",
#        3: "QEvent::MouseButtonRelease",
#        5: "QEvent::MouseMove",
#        109: "QEvent::MouseTrackingChange",
#        13: "QEvent::Move",
#        12: "QEvent::Paint",
#        39: "QEvent::PaletteChange",
#        131: "QEvent::ParentAboutToChange",
#        21: "QEvent::ParentChange",
#        212: "QEvent::PlatformPanel",
#        75: "QEvent::Polish",
#        74: "QEvent::PolishRequest",
#        123: "QEvent::QueryWhatsThis",
#        199: "QEvent::RequestSoftwareInputPanel",
#        14: "QEvent::Resize",
#        117: "QEvent::Shortcut",
#        51: "QEvent::ShortcutOverride",
#        17: "QEvent::Show",
#        26: "QEvent::ShowToParent",
#        50: "QEvent::SockAct",
#        192: "QEvent::StateMachineSignal",
#        193: "QEvent::StateMachineWrapped",
#        112: "QEvent::StatusTip",
#        100: "QEvent::StyleChange",
#        87: "QEvent::TabletMove",
#        92: "QEvent::TabletPress",
#        93: "QEvent::TabletRelease",
#        94: "QEvent::OkRequest",
#        171: "QEvent::TabletEnterProximity",
#        172: "QEvent::TabletLeaveProximity",
#        1: "QEvent::Timer",
#        120: "QEvent::ToolBarChange",
#        110: "QEvent::ToolTip",
#        184: "QEvent::ToolTipChange",
#        189: "QEvent::UngrabKeyboard",
#        187: "QEvent::UngrabMouse",
#        78: "QEvent::UpdateLater",
#        77: "QEvent::UpdateRequest",
#        111: "QEvent::WhatsThis",
#        118: "QEvent::WhatsThisClicked",
#        31: "QEvent::Wheel",
#        132: "QEvent::WinEventAct",
#        24: "QEvent::WindowActivate",
#        103: "QEvent::WindowBlocked",
#        25: "QEvent::WindowDeactivate",
#        34: "QEvent::WindowIconChange",
#        105: "QEvent::WindowStateChange",
#        33: "QEvent::WindowTitleChange",
#        104: "QEvent::WindowUnblocked",
#        126: "QEvent::ZOrderChange",
#        169: "QEvent::KeyboardLayoutChange",
#        170: "QEvent::DynamicPropertyChange",
#        194: "QEvent::TouchBegin",
#        195: "QEvent::TouchUpdate",
#        196: "QEvent::TouchEnd",
#        203: "QEvent::WinIdChange",
#        198: "QEvent::Gesture",
#        202: "QEvent::GestureOverride"
#    }.get(event.type(), "UnknownEvent")
	