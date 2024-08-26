#ifndef MESSAGEHEADER_H
#define MESSAGEHEADER_H

#include <QDataStream>
#include "core_global.h"

struct CORE_EXPORT MessageHeader {
    MessageHeader(int type_ = -1):type(type_){}
    bool isAnswer;
    int type;
    int uid; // if answer - put there request msg id, otherwise put msg id
    int itemId;
};

QDataStream CORE_EXPORT &operator<<(QDataStream &out, const MessageHeader& obj);

QDataStream CORE_EXPORT &operator>>(QDataStream &in, MessageHeader &obj);

#endif // MESSAGEHEADER_H
