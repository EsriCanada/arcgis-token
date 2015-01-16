from distutils.core import setup
import py2exe

setup(windows=["arcgis_token.py"],
      options=dict(
          py2exe={
              "includes":
                  ["PyQt4.QtGui", "PyQt4.QtCore", "sip"],
              "dll_excludes":
                  ["MSVCP90.dll"]
          }))

# C:\Python27\Python279\python.exe setup.py py2exe