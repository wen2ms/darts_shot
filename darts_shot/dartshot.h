#ifndef DARTSHOT_H
#define DARTSHOT_H

#include <QThread>
#include <QImage>

class DartShot : public QObject {
    Q_OBJECT
  public:
    explicit DartShot(int camera_index, QObject *parent = nullptr);
    
    inline void stop_shot() {is_running_ = false;};
    
    void run();

  signals:
    void frame_ready(const QImage&);
    
  private:
    int camera_index_;
    bool is_running_ = true;
};

#endif  // DARTSHOT_H
