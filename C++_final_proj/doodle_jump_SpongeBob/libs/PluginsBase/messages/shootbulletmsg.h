#ifndef SHOOTBULLETMSG_H
#define SHOOTBULLETMSG_H

#include <imessage.h>
#include <pluginsbase_global.h>
#include <QDataStream>
#include <QPointF>

struct PLUGINSBASE_EXPORT ShootBulletMsg : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    double x;
    double y;

private:
     const static uint32_t m_messageType = 11;
};

struct PLUGINSBASE_EXPORT ShootBulletMsgAns : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool success;

private:
     const static uint32_t m_messageType = 12;
};
#endif // SHOOTBULLETMSG_H
