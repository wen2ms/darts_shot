#ifndef DARTSHOT_H
#define DARTSHOT_H

#include <QObject>
#include <QImage>

class DartShot : public QObject {
    Q_OBJECT
  public:
    explicit DartShot(int camera_index, QObject *parent = nullptr);
    
    void working();

  signals:
    void frame_ready(QImage);
    
  private:
    int camera_index_;
    bool is_running_ = true;
};

#endif  // DARTSHOT_H
