from distutils.core import setup
import py2exe

setup(
    options =dict(
        py2exe={
              "includes":
                  ["PyQt4.QtGui", "PyQt4.QtCore", "sip"],
              "dll_excludes":
                  ["MSVCP90.dll"]
          }),
    zipfile = None,
    windows = [dict(script="arcgis_token.py",
                    icon_resources=[(1, "icon.ico")],
                    dest_base="arcgis_token"
    )],
)

# http://stackoverflow.com/questions/9649727/changing-the-icon-of-the-produced-exe-py2exe