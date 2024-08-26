#ifndef REMOVEITEMMESSAGE_H
#define REMOVEITEMMESSAGE_H

#include <imessage.h>
#include <vector>
#include <pluginsbase_global.h>
#include <QDataStream>

struct PLUGINSBASE_EXPORT RemoveItemMessage : IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    std::vector<uint32_t> ids;

private:
     const static uint32_t m_messageType = 3;
};

struct PLUGINSBASE_EXPORT RemoveItemMessageAns : IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool success;

private:
     const static uint32_t m_messageType = 4;
};

#endif // REMOVEITEMMESSAGE_H
