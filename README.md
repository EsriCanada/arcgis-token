# ArcGIS Token Generator

Simple Python desktop application to quickly generate an ArcGIS Online token.  Users will mainly use this utility when developing applications and require an AGOL token for testing purposes.  [About ArcGIS Tokens](http://resources.arcgis.com/en/help/main/10.1/index.html#/About_ArcGIS_tokens/0154000005r6000000/)

## Getting Started

A self-contained, pre-built executable for this application is available on the [Releases](https://github.com/amarinelli/arcgis-token/releases) page.

Interested in building your own executable?  See below.

## Usage

Once an executable is downloaded/built and run, a small dialog will appear containing the extent of the application.

- Supply your username and password for your [ArcGIS Online](http://www.arcgis.com/features/) Organizational Account
- Choose an expiration duration
- Choose whether the token will be automatically copied to your computer's clipboard
- Submit the request using the *Get Token* button
- Messages will appear showing success status and if granted, a timestamp of expiration
- Now that you have a token, you can make a request to secured Esri services
 - Example for testing [here](http://hydro.arcgis.com/arcgis/rest/login?redirect=http%3A//hydro.arcgis.com/arcgis/rest/services)
 
 *Remember that any credits consumed by the requests you make here will be deducted from your ArcGIS Online account. See the [Credit Overview](http://www.esri.com/software/arcgis/arcgisonline/credits) for more information and to use a [Credit Estimator](http://www.esri.com/software/arcgis/arcgisonline/credits/estimator)*

## How it works

The working code of the application is quite simple and uses the ArcGIS REST API [Generate Token](http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Generate_Token/02r3000000m5000000/) operation to request a token

Example:

```JavaScript
https://www.arcgis.com/sharing/rest/generateToken
username=jsmith33
password=myPassword
expiration=60 
referer=http://www.arcgis.com
```

### Third Party Libraries Used

- [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download)
- [pyinstaller](https://github.com/pyinstaller/pyinstaller/wiki)


### Build

Building an executable from this script can be done using [py2exe](http://www.py2exe.org/) or [pyinstaller](https://github.com/pyinstaller/pyinstaller/wiki).  The instructions below use pyinstaller to build an self-contained executable named *ArcGIS-Token.exe*

[Download](https://github.com/amarinelli/arcgis-token/archive/master.zip) the source code and make sure you have the appropriate dependencies (PyQt4 and pyinstaller)

See the [pyinstaller manual](http://pythonhosted.org/PyInstaller/#using-pyinstaller) for documentation and options.

```Shell
pip install pyinstaller
pyinstaller --name=ArcGIS-Token --onefile --windowed --noconsole arcgis_token.py
```

The executable should be created in the /dist folder

### Future Improvements

- Add the ability to generate a token for ArcGIS for Server

### Contributing

Please feel free to fork your own copy and to submit [issues](https://github.com/amarinelli/arcgis-token/issues)


