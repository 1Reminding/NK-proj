#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "doodlejump.h"
#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class DoodleJump;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    DoodleJump * doodlejump;
};

#endif // MAINWINDOW_H
