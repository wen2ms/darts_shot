#ifndef SAVEFRAME_H
#define SAVEFRAME_H

#include <QThread>
#include <QImage>
#include <QVector>

class SaveFrame : public QThread {
    Q_OBJECT
  public:
    explicit SaveFrame(const QVector<QImage>& frames, const QString& file_path, QObject *parent = nullptr);
    
  protected:
    void run() override;

  signals:
    void current_percent(int value);
    
  private:
    QVector<QImage> frames_;
    QString file_path_;
};

#endif  // SAVEFRAME_H
