#ifndef SETVELOCITYMSG_H
#define SETVELOCITYMSG_H

#include <imessage.h>
#include <pluginsbase_global.h>
#include <QDataStream>

struct PLUGINSBASE_EXPORT SetVelocityMsg : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    // if velocity < 0 -> move left
    // else if velocity > 0 -> move right
    double velocity = 0;

private:
     const static uint32_t m_messageType = 9;
};

struct PLUGINSBASE_EXPORT SetVelocityMsgAns : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool success;

private:
     const static uint32_t m_messageType = 10;
};

#endif // SETVELOCITYMSG_H
