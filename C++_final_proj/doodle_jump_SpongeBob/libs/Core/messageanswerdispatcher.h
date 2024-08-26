#ifndef MESSAGEANSWERDISPATCHER_H
#define MESSAGEANSWERDISPATCHER_H

#include "messageheader.h"
#include <exception>
#include <iostream>
#include <QDebug>

class MessageAnswerDispatcher;

class MsgAnswerHandler
{
public:
    MsgAnswerHandler(MessageAnswerDispatcher * disp, int m_uid) : m_answerDispatcher(disp), m_uid(m_uid) {}

    template<class TAns>
    void onCompleted(std::function<void (TAns)> callback);

private:
    MessageAnswerDispatcher* m_answerDispatcher;
    int m_uid;
};


class MessageAnswerDispatcher
{
    friend class MsgAnswerHandler;
public:
    MessageAnswerDispatcher();
    void proceedMsgAnswer(const MessageHeader & h, QDataStream &s);

private:
    std::map<int, std::function<void(const MessageHeader & h, QDataStream &s)>> m_answerHandlers;

};

template<class TAns>
void MsgAnswerHandler::onCompleted(std::function<void (TAns)> callback)
{
    auto lambda = [callback](const MessageHeader& h, QDataStream &s){
        TAns answ;
        try {
            answ.deserialize(&s);
            if (h.type != answ.getType()) {
                throw std::exception();
            }
            callback(answ);
        } catch (const std::exception & e) {
            std::cerr << "types are not the same! " << h.type << " " << answ.getType() << std::endl;
        }
    };

    m_answerDispatcher->m_answerHandlers.insert({m_uid, lambda});
}
#endif // MESSAGEANSWERDISPATCHER_H
