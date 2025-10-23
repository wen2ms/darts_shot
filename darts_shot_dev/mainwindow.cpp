#include "mainwindow.h"

#include <QPixmap>
#include <QFileDialog>
#include <QMessageBox>

#include "./ui_mainwindow.h"

#include "saveframe.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow), original_images_(3) {
    ui->setupUi(this);
    
    ui->progressBar->setRange(0, 100);
    ui->progressBar->setValue(0);
    
    camera_labels_.push_back(ui->camera_0);
    camera_labels_.push_back(ui->camera_1);
    
    for (int i = 0; i < camera_labels_.size(); ++i) {
        camera_labels_[i]->setFixedSize(320, 240);
        
        DartShot* dart_shot_thread = new DartShot(i + 1, this);
        
        connect(dart_shot_thread, &DartShot::frame_ready, this, [=](QImage frame) {
            QImage scaled_frame = frame.scaled(320, 240, Qt::KeepAspectRatio);
            
            camera_labels_[i]->setPixmap(QPixmap::fromImage(scaled_frame));
            
            original_images_[i] = frame.copy();
        });
        
        dart_shot_threads_.push_back(dart_shot_thread);
    }
    
    for (auto thread : dart_shot_threads_) {
        thread->start();
    }
}

MainWindow::~MainWindow() {    
    for (auto thread : dart_shot_threads_) {
        thread->stop_shot();
        
        thread->quit();
        thread->wait();
        thread->deleteLater();
    }
    
    delete ui;
}

void MainWindow::on_shot_clicked() {
    QString file_path = ui->file_path->text();
    
    qDebug() << "saving frames...";
    
    ui->progressBar->setValue(0);
        
    SaveFrame* save_frame_thread = new SaveFrame(original_images_, file_path);
    
    connect(save_frame_thread, &SaveFrame::current_percent, ui->progressBar, &QProgressBar::setValue);
    
    connect(save_frame_thread, &QThread::finished, this, [=]() {
        save_frame_thread->quit();
        save_frame_thread->wait();
        save_frame_thread->deleteLater();
    });
    
    save_frame_thread->start();
}

void MainWindow::keyPressEvent(QKeyEvent* event) {
    if (event->key() == Qt::Key_Space) {
        QString file_path = ui->file_path->text();
        
        qDebug() << "saving frames...";
        
        ui->progressBar->setValue(0);
        
        SaveFrame* save_frame_thread = new SaveFrame(original_images_, file_path);
        
        connect(save_frame_thread, &SaveFrame::current_percent, ui->progressBar, &QProgressBar::setValue);
        
        connect(save_frame_thread, &QThread::finished, this, [=]() {
            save_frame_thread->quit();
            save_frame_thread->wait();
            save_frame_thread->deleteLater();
        });
        
        save_frame_thread->start();
    }
}

void MainWindow::on_set_file_clicked() {
    QString file_path = QFileDialog::getExistingDirectory(this, "Select Directory");
    
    if (file_path.isEmpty()) {
        QMessageBox::warning(this, "Open File", "The file path selected cannot be empty");
        
        return;
    }
    
    ui->file_path->setText(file_path);   
}
