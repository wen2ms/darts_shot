#include "saveframe.h"

#include <QDebug>
#include <QDateTime>

SaveFrame::SaveFrame(const QVector<QImage>& frames, const QString &file_path, QObject *parent)
    : QThread{parent}, frames_(frames), file_path_(file_path) {}

void SaveFrame::run() {
    QString time_stamp = QDateTime::currentDateTime().toString("yyyyMMdd_HHmmss_zzz");
    for (int i = 0; i < frames_.size(); ++i) {
        QString file_name = file_path_ + "/" + QString("frame_%1_cam%2.png").arg(time_stamp).arg(i);
                        
        if (frames_[i].save(file_name)) {
            qDebug() << "saved:" << file_name;
            
            emit current_percent((i + 1) * 100 / frames_.size());
        }
        
        msleep(500);
    }   
}
