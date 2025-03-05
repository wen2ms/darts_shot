#include "saveframe.h"

#include <QDebug>
#include <QDateTime>

SaveFrame::SaveFrame(const QVector<QImage> &frames, const QString &file_path, QObject *parent)
    : QThread{parent}, frames_(frames), file_path_(file_path) {}

void SaveFrame::run() {
    int all_frames_count = frames_.size();
    
    for (int i = 0; i < all_frames_count; ++i) {
        QString time_stamp = QDateTime::currentDateTime().toString("hh_mm_ss");
        QString file_name = file_path_ + "/" + QString("frame_%1.png").arg(time_stamp);
        
        if (frames_[i].save(file_name)) {
            qDebug() << "saved:" << file_name;
        }
        
        emit current_percent((i + 1) / all_frames_count * 33);
        
        msleep(500);
    }   
}
