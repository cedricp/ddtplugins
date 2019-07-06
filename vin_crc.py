# -*- coding: utf-8 -*-

# Plugin to compute CRC from VIN
# (c) 2017

import crcmod
from binascii import unhexlify
import platform

try:
    import PyQt5.QtGui as gui
    import PyQt5.QtCore as core
    import PyQt5.QtWidgets as widgets
    if platform.system() == 'Darwin':
        import PyQt5.QtWebEngine as webkit
        import PyQt5.QtWebEngineWidgets as webkitwidgets
    else:
        import PyQt5.QtWebKit as webkit
        import PyQt5.QtWebKitWidgets as webkitwidgets
    def utf8(string):
        return string
    qt5 = True
except:
    import PyQt4.QtGui as gui
    import PyQt4.QtGui as widgets
    import PyQt4.QtCore as core
    import PyQt4.QtWebKit as webkit
    import PyQt4.QtWebKit as webkitwidgets
    def utf8(string):
        return unicode(string.toUtf8(), encoding="UTF-8")
    qt5 = False

import options

_ = options.translator('ddt4all')

plugin_name = _("CRC calculator")
category = _("VIN")
# We need an ELM to work
need_hw = False

def calc_crc(vin=None):
    VIN=vin.encode("hex")
    VININT=unhexlify(VIN)

    crc16 = crcmod.predefined.Crc('x-25')
    crc16.update(VININT)
    crcle = crc16.hexdigest()
    # Seems that computed CRC is returned in little endian way
    # Convert it to big endian
    return crcle[2:4] + crcle[0:2]


class CrcWidget(widgets.QDialog):
    def __init__(self):
        super(CrcWidget, self).__init__(None)
        layout = widgets.QVBoxLayout()
        self.input = widgets.QLineEdit()
        self.output = widgets.QLineEdit()
        self.output.setStyleSheet("QLineEdit { color: rgb(255, 0, 0); }")
        info = widgets.QLabel(_("CRC CALCULATOR"))
        info.setAlignment(core.Qt.AlignHCenter)
        self.output.setAlignment(core.Qt.AlignHCenter)
        layout.addWidget(info)
        layout.addWidget(self.input)
        layout.addWidget(self.output)
        self.input.textChanged.connect(self.recalc)
        self.setLayout(layout)
        self.output.setReadOnly(True)

    def recalc(self):
        if qt5:
            vin = str(self.input.text().encode("ascii", errors='"ignore')).upper()
        else:
            vin = str(self.input.text().toAscii()).upper()
        crc = calc_crc(vin)
        self.output.setText('%s' % crc)


def plugin_entry():
    a = CrcWidget()
    a.exec_()
