#ifndef CHANGEVIEWRECT_H
#define CHANGEVIEWRECT_H

#include <imessage.h>
#include <pluginsbase_global.h>
#include <QString>
#include <QRectF>

struct PLUGINSBASE_EXPORT ChangeViewRectMsg : IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    QRectF viewRect;

private:
    const static uint32_t m_messageType = 13;
};

struct PLUGINSBASE_EXPORT ChangeViewRectMsgAns : IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool success;

private:
    const static uint32_t m_messageType = 14;
};

#endif // CHANGEVIEWRECT_H
