#include "dartshot.h"

#include <opencv2/opencv.hpp>
#include <QDebug>

DartShot::DartShot(int camera_index, QObject *parent) : QObject{parent}, camera_index_(camera_index) {}

void DartShot::run() {
    qDebug() << "The dart shoting thread:" << QThread::currentThread();

#ifdef _WIN32
    cv::VideoCapture capture(camera_index_, cv::CAP_DSHOW);
#else
    cv::VideoCapture capture(camera_index_);
#endif
    
    if (!capture.isOpened()) {
        return;
    }
    capture.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
    capture.set(cv::CAP_PROP_FRAME_HEIGHT, 720);
    
    while (is_running_) {
        cv::Mat frame;
        
        capture >> frame;
        
        if (!frame.empty()) {
            cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
            
            QImage frame_image(frame.data, frame.cols, frame.rows, frame.step, QImage::Format_RGB888);
            
            emit frame_ready(frame_image.copy());
            
            QThread::msleep(30);
        }
    }
    
    capture.release();
}
