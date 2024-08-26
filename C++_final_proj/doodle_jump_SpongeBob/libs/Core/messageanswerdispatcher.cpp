#include "messageanswerdispatcher.h"

#include <QDataStream>

MessageAnswerDispatcher::MessageAnswerDispatcher()
{

}

void MessageAnswerDispatcher::proceedMsgAnswer(const MessageHeader &h, QDataStream &s){
    auto search = m_answerHandlers.find(h.uid);
    if (search != m_answerHandlers.end()) {
        search->second(h, s);
        m_answerHandlers.erase(search->first);
    }
}

