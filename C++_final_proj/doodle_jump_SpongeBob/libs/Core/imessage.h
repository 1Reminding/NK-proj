#ifndef IMESSAGE_H
#define IMESSAGE_H

#include <QDataStream>

struct IMessage
{
    IMessage() = default;
    virtual ~IMessage() {}

    virtual uint32_t getType() const = 0;
    virtual void serialize(QDataStream *s) const = 0;
    virtual void deserialize(QDataStream *s) = 0;
};

#endif // IMESSAGE_H
