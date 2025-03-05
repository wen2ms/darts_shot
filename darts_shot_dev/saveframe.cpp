#include "saveframe.h"

#include <QDebug>
#include <QDateTime>

SaveFrame::SaveFrame(const QVector<QImage>& frames, const QString &file_path, QObject *parent)
    : QThread{parent}, frames_(frames), file_path_(file_path) {}

void SaveFrame::run() {    
    for (int i = 0; i < frames_.size(); ++i) {
        QString time_stamp = QDateTime::currentDateTime().toString("hh_mm_ss");
        QString file_name = file_path_ + "/" + QString("frame_%1_%2.png").arg(time_stamp).arg(i);
                        
        if (frames_[i].save(file_name)) {
            qDebug() << "saved:" << file_name;
            
            emit current_percent((i + 1) * 50);
        }
        
        msleep(500);
    }   
}
