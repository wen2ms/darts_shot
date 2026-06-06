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
    void save_current_frames();
    
    Ui::MainWindow *ui;
    
    QList<DartShot*> dart_shots_;
    QList<QWidget*> camera_widgets_;
    QList<QLabel*> camera_labels_;
    QList<QThread*> dart_shot_threads_;
    QVector<QImage> original_images_;
};
#endif  // MAINWINDOW_H
