#ifndef STARTENGINEMSG_H
#define STARTENGINEMSG_H

#include <imessage.h>
#include <pluginsbase_global.h>
#include <QDataStream>

enum EngineMode {
    START, PAUSE, STOP
};

struct PLUGINSBASE_EXPORT SetModeEngineMsg : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    EngineMode mode;

private:
     const static uint32_t m_messageType = 7;
};

struct PLUGINSBASE_EXPORT SetModeEngineMsgAns : public IMessage
{
    uint32_t getType() const override { return m_messageType; }
    static bool checkType(uint32_t type) { return type == m_messageType; }
    static bool checkType(IMessage *msg) { return msg->getType() == m_messageType; }
    void serialize(QDataStream *) const override;
    void deserialize(QDataStream *) override;

public:
    bool modeChangedSuccess;
    EngineMode mode;

private:
     const static uint32_t m_messageType = 8;
};

#endif // STARTENGINEMSG_H
