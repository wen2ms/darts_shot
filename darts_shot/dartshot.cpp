#include "dartshot.h"

#include <opencv2/opencv.hpp>
#include <QThread>
#include <QDebug>

DartShot::DartShot(int camera_index, QObject *parent) : QObject{parent}, camera_index_(camera_index) {}

void DartShot::working() {
    qDebug() << "The dart shoting thread:" << QThread::currentThread();
    
    cv::VideoCapture capture(camera_index_);
    
    if (!capture.isOpened()) {
        return;
    }
    
    while (is_running_) {
        cv::Mat frame;
        
        capture >> frame;
        
        if (!frame.empty()) {
            cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
            
            emit frame_ready(QImage(frame.data, frame.cols, frame.rows, frame.step, QImage::Format_RGB888));
            
            QThread::msleep(30);
        }
        
        capture.release();
    }
}
