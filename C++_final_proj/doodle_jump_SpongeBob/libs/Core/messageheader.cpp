#include "messageheader.h"

QDataStream &operator<<(QDataStream &out, const MessageHeader& obj) {
   out << obj.isAnswer << obj.type << obj.uid << obj.itemId;
   return out;
}

QDataStream &operator>>(QDataStream &in, MessageHeader &obj) {
   in >> obj.isAnswer >> obj.type >> obj.uid >> obj.itemId;
   return in;
}
