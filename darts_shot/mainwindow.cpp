#include "mainwindow.h"

#include <QPixmap>

#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow) {
    ui->setupUi(this);
    
    camera_labels_.push_back(ui->camera_0);
    camera_labels_.push_back(ui->camera_1);
    camera_labels_.push_back(ui->camera_2);
    
    for (int i = 0; i < 3; ++i) {
        camera_labels_[i]->setFixedSize(640, 480);
        
        DartShot* dart_shot_thread = new DartShot(i);
        
        connect(dart_shot_thread, &DartShot::frame_ready, this, [=](const QImage& frame) {
            camera_labels_[i]->setPixmap(QPixmap::fromImage(frame));
        });
        
        dart_shot_threads_.push_back(dart_shot_thread);
    }
    
    for (auto thread : dart_shot_threads_) {
        thread->start();
    }
}

MainWindow::~MainWindow() {
    delete ui;
    
    for (auto thread : dart_shot_threads_) {
        thread->stop_shot();
        
        thread->quit();
        thread->wait();
        thread->deleteLater();
    }
}
