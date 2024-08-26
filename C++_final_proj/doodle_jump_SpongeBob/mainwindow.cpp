#include "mainwindow.h"
#include "ui_mainwindow.h"

#include<QScreen>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setCentralWidget(ui->graphicsView);

    doodlejump = new DoodleJump(ui->graphicsView);

    QScreen *screen = QGuiApplication::primaryScreen();
    QRect  screenGeometry = screen->geometry();
    int x = (screenGeometry.width() - width()) / 2;
    int y = (screenGeometry.height() - height()) / 2;
    setGeometry(x, y, 640, 960);
}

MainWindow::~MainWindow()
{
    delete ui;
}
