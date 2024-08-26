#ifndef CHANGECOORDSMSG_H
#define CHANGECOORDSMSG_H

#include <imessage.h>
#include <pluginsbase_global.h>

struct PLUGINSBASE_EXPORT ChangeCoordsMsg : IMessage
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
    const static uint32_t m_messageType = 5;
};

struct PLUGINSBASE_EXPORT ChangeCoordsMsgAns : IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool success;

private:
    const static uint32_t m_messageType = 6;
};

#endif // CHANGECOORDSMSG_H
