#include "removeitemmessage.h"

void RemoveItemMessage::serialize(QDataStream *s) const
{
    *s << static_cast<int>(ids.size());
    for(int id : ids) {
        *s << id;
    }
}

void RemoveItemMessage::deserialize(QDataStream *s)
{
    int size;
    *s >> size;
    //ids.reserve(size);
    int index = 0;
    for(int i = 0; i < size; i++) {
        *s >> index;
        ids.push_back(index);
    }
}

void RemoveItemMessageAns::serialize(QDataStream *s) const
{
    *s << success;
}

void RemoveItemMessageAns::deserialize(QDataStream *s)
{
    *s >> success;
}
