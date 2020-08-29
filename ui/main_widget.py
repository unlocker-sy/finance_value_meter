from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QPainter
from PyQt5 import QtChart
from PyQt5.QtWidgets import *
import sys
from ui.table_model import CustomTableModel

'''
https://stackoverflow.com/questions/58274166/cannot-import-pyqtchart-in-python-3-7
pyqt5에서 QtChart를 사용하기 위해서는 아래 패키지를 설치해주어야한다.
python -m pip install PyQt5==5.13 PyQtChart==5.13
그리고 import할 때에는 아래 처럼 해주어야 한다.
from PyQt5 import QtChart
'''

class Widget(QWidget):
    # def __init__(self, data):
    def __init__(self):
        QWidget.__init__(self)

        self.grpBox = QGroupBox("재무 정보")
        # Create Widgets
        self.btnStart = QPushButton("시작")
        self.statusLabel = QLabel("진행 상태:")
        self.statusLabel.setAlignment(Qt.AlignLeft)
        self.editCode = QLineEdit("종목 코드 입력")
        self.btnFinanceSheet = QPushButton("재무 정보 수집")
        self.btnStart.clicked.connect(self.start_scrap)
        self.btnFinanceSheet.clicked.connect(self.getCode)

        # Getting the Model
        # self.model = CustomTableModel(data)
        self.model = CustomTableModel()
        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        self.leftInnerLayout = QVBoxLayout()
        self.leftInnerLayout.addWidget(self.btnStart)
        self.leftInnerLayout.addWidget(self.statusLabel)
        self.leftInnerLayout.addWidget(self.editCode)
        self.leftInnerLayout.addWidget(self.btnFinanceSheet)
        self.leftInnerLayout.setAlignment(Qt.AlignTop)
        self.grpBox.setLayout(self.leftInnerLayout)

        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.grpBox)

        # Right Layout - # Creating QChartView
        self.chart = QtChart.QChart()
        self.chart.setAnimationOptions(QtChart.QChart.AllAnimations)
        self.add_series("Magnitude (Column 1)", [0, 1])
        self.chart_view = QtChart.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right Layout
        self.rightLayout = QVBoxLayout()
        # size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # size.setHorizontalStretch(4)
        # self.chart_view.setSizePolicy(size)
        self.rightLayout.addWidget(self.chart_view)

        # QWidget Layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.leftLayout)
        self.main_layout.addLayout(self.rightLayout)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)
        
    # Greets the user
    def getCode(self):
        print("종목 정보 %s" % self.editCode.text())
    
    def start_scrap(self):
        print("start scrap")

    def add_series(self, name, columns):
        # Create QLineSeries
        self.series = QtChart.QLineSeries()
        self.series.setName(name)

        # Filling QLineSeries
        for i in range(self.model.rowCount()):
            # Getting the data
            t = self.model.index(i, 0).data()
            date_fmt = "yyyy-MM-dd HH:mm:ss.zzz"

            x = QDateTime().fromString(t, date_fmt).toSecsSinceEpoch()
            y = float(self.model.index(i, 1).data())

            if x > 0 and y >0:
                self.series.append(x, y)
            
        self.chart.addSeries(self.series)

        # Setting X-axis
        self.axis_x = QtChart.QDateTimeAxis()
        self.axis_x.setTickCount(10)
        self.axis_x.setFormat("dd.MM (h:mm)")
        self.axis_x.setTitleText("Date")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        # Setting Y-axis
        self.axis_y = QtChart.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.2f")
        self.axis_y.setTitleText("Magnitude")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)

        # Getting the color from QChart to use it on the QTableView
        self.model.color = "{}".format(self.series.pen().color().name())