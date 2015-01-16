from distutils.core import setup
import py2exe

setup(windows=['arcgis_token.py'], options={"py2exe": {"includes": ["PyQt4.QtGui", "PyQt4.QtCore"]}})
