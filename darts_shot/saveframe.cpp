#include "saveframe.h"

SaveFrame::SaveFrame(const QVector<QImage> &frames, const QString &file_path, QObject *parent)
    : QThread{parent}, frames_(frames), file_path_(file_path) {}

void SaveFrame::run() {
    
}
