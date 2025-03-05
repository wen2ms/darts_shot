#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QKeyEvent>
#include <QVector>

#include "dartshot.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
    Q_OBJECT

  public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    
  protected:
    void keyPressEvent(QKeyEvent* event) override;
    
  private slots:
    void on_shot_clicked();
    
    void on_set_file_clicked();
    
  private:
    Ui::MainWindow *ui;
    
    QList<QLabel*> camera_labels_;
    QList<DartShot*> dart_shot_threads_;
    QVector<QImage> original_images_;
};
#endif  // MAINWINDOW_H
