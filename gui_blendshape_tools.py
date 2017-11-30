# rigmarole-tools/gui_blendshape_tools.py

""" WIP development of PySide GUI for blendshape_tools """
try:
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtWidgets
except ImportError:
    print("failed to import PySide2, {}".format(__file__))
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtWidgets as QtWidgets

try:
    # future proofing for Maya 2017.
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance


class BlendshapeToolsWindow(QtWidgets.QMainWindow):
    chooseNeutralClicked = QtCore.Signal(str)
    chooseGeoToSplitClicked = QtCore.Signal(str)
    smashGeoButtonClicked = QtCore.Signal(str)
    splitBlendshapesClicked = QtCore.Signal(str)
    splitBlendshapesSoftClicked = QtCore.Signal(str)
    chooseSmashGeoClicked = QtCore.Signal(str)


def create_window():
    window = BlendshapeToolsWindow()
    window.setWindowTitle('Rigmarole Blendshape Tools')

    container = QtWidgets.QWidget(window)
    horizontal = QtCore.Qt.Horizontal
    
    volumeLabel = QtWidgets.QLabel('Intensity')
    volumeSlider = QtWidgets.QSlider(orientation=horizontal)
    volumeIndicator = QtWidgets.QLineEdit(maximumWidth=80)

    falloffLabel = QtWidgets.QLabel('Falloff Easing')
    falloffDropdown = QtWidgets.QComboBox()
    falloffDropdown.addItem('Linear 1')
    falloffDropdown.addItem('Cubic 3')
    falloffDropdown.addItem('Quadratic 4')
    falloffDropdown.setCurrentIndex(2)

    button = QtWidgets.QPushButton('Choose Neutral Geo:', container)
    splitGeoButton = QtWidgets.QPushButton('Choose Geo to Split:', container)
    textbox = QtWidgets.QLineEdit(container)
    splitGeoField = QtWidgets.QLineEdit(container)

    chooseSmashGeoButton = QtWidgets.QPushButton('Choose Geo to Change:', container)
    smashGeoField = QtWidgets.QLineEdit()
    smashGeoButton = QtWidgets.QPushButton('Vertex Smash', container)

    splitBlendshapesButton = QtWidgets.QPushButton('Split Blendshapes using Helpers', container)
    splitBlendshapesSoftButton = QtWidgets.QPushButton('Split Blendshapes by Soft Selection', container)

    def onclick():
        window.chooseNeutralClicked.emit(textbox.text())
    button.clicked.connect(onclick)

    def onclick():
        window.chooseGeoToSplitClicked.emit(splitGeoField.text())
    splitGeoButton.clicked.connect(onclick)

    def onclick():
        window.smashGeoButtonClicked.emit(smashGeoField.text())
    smashGeoButton.clicked.connect(onclick)

    def onclick():
        window.chooseSmashGeoClicked.emit(smashGeoField.text())
    chooseSmashGeoButton.clicked.connect(onclick)

    def onclick():
        window.splitBlendshapesClicked.emit(splitGeoField.text())
    splitBlendshapesButton.clicked.connect(onclick)

    def onclick():
        window.splitBlendshapesSoftClicked.emit(splitGeoField.text())
    splitBlendshapesSoftButton.clicked.connect(onclick)

    mainLayout = QtWidgets.QVBoxLayout(container)

    # LAYOUT: volume intensity slider
    layout0 = QtWidgets.QHBoxLayout()
    layout0.addWidget(volumeLabel)
    layout0.addWidget(volumeSlider)
    layout0.addWidget(volumeIndicator)

    # LAYOUT: Falloff Easing dropdown box
    layout1 = QtWidgets.QHBoxLayout()
    layout1.addWidget(falloffLabel)
    layout1.addWidget(falloffDropdown)

    # LAYOUT: Random buttons for testing
    layout2 = QtWidgets.QHBoxLayout()
    layout2.addWidget(button)
    layout2.addWidget(textbox)

    # LAYOUT: Split geometry chooser
    layout3 = QtWidgets.QHBoxLayout()
    layout3.addWidget(splitGeoButton)
    layout3.addWidget(splitGeoField)

    # LAYOUT: Split blendshapes operation buttons
    layout5 = QtWidgets.QVBoxLayout()
    layout5.addWidget(splitBlendshapesButton)
    layout5.addWidget(splitBlendshapesSoftButton)

    # LAYOUT: Choose smash geo and smash button
    layout4 = QtWidgets.QHBoxLayout()
    layout4.addWidget(chooseSmashGeoButton)
    layout4.addWidget(smashGeoField)
    layout4.addWidget(smashGeoButton)

    group0 = QtWidgets.QGroupBox('Options')
    optionsLayout = QtWidgets.QVBoxLayout()
    optionsLayout.addLayout(layout0)
    group0.setLayout(optionsLayout)

    group1 = QtWidgets.QGroupBox('Split Blendshapes')
    splitBlendshapeLayout = QtWidgets.QVBoxLayout()
    splitBlendshapeLayout.addLayout(layout1)
    splitBlendshapeLayout.addLayout(layout2)
    splitBlendshapeLayout.addLayout(layout3)
    splitBlendshapeLayout.addLayout(layout5)
    group1.setLayout(splitBlendshapeLayout)
    
    group2 = QtWidgets.QGroupBox('Vertex Smash')
    vertexSmashLayout = QtWidgets.QVBoxLayout()
    vertexSmashLayout.addLayout(layout4)
    group2.setLayout(vertexSmashLayout)

    mainLayout.addWidget(group0)
    mainLayout.addWidget(group1)
    mainLayout.addWidget(group2)

    window.setCentralWidget(container)

    return window

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = create_window()

    def onChooseNeutralClicked(prefix):
        print('Choose neutral geo clicked. Message:', prefix)
    win.chooseNeutralClicked.connect(onChooseNeutralClicked)

    def onChooseSplitClicked(prefix):
        print('Choose split geo clicked. Message:', prefix)
    win.chooseGeoToSplitClicked.connect(onChooseSplitClicked)
    
    def onSmashVertexClicked(prefix):
        print('Smash Vertex clicked. Message:', prefix)
    win.smashGeoButtonClicked.connect(onSmashVertexClicked)
    
    def onSplitBlendshapesClicked(prefix):
        print('Split Blendshapes by Helper clicked. Message:', prefix)
    win.splitBlendshapesClicked.connect(onSplitBlendshapesClicked)
    
    def onSplitBlendshapesSoftClicked(prefix):
        print('Split Blendshapes by Soft Selection clicked. Message:', prefix)
    win.splitBlendshapesSoftClicked.connect(onSplitBlendshapesSoftClicked)
    
    def onChooseSmashGeoClicked(prefix):
        print('Choose Smash Geo clicked. Message:', prefix)
    win.chooseSmashGeoClicked.connect(onChooseSmashGeoClicked)
    
    win.show()
    app.exec_()

