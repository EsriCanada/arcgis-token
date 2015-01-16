from distutils.core import setup
import py2exe

setup(windows=["arcgis_token.py"],
      options=dict(
          py2exe={
              "includes":
                  ["PyQt4.QtGui", "PyQt4.QtCore"],
              "dll_excludes":
                  ["MSVCP90.dll"]
          }))
