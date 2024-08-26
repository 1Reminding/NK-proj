#ifndef ENGINEINTERFACE_H
#define ENGINEINTERFACE_H

#include "core_global.h"
#include <circlebuffer.h>
#include <enginebase.h>
#include <messageanswerdispatcher.h>
#include <QDataStream>
#include <map>


struct IMessage;
class MessageNegotiator;
class EngineBase;
class SampleDataGetter;

class CORE_EXPORT MessageConnector {
    std::function<void(QDataStream &)> callbackOnMsg;
    int messageType;
public:

    int getMessageType() {return messageType;}

    template <typename Msg, typename Callable>
    void connectToMsg(Callable m)
    {
        messageType = Msg().getType();
        callbackOnMsg = [m](QDataStream & s)
        {
            Msg msg;
            msg.deserialize(&s);
            m(msg);
        };
    }

    void operator()(QDataStream &s)
    {
        callbackOnMsg(s);
    }
};


class CORE_EXPORT EngineInterface
{
    friend class EngineBase;
    friend MsgAnswerHandler;
    friend class SampleDataGetter;
public:
    EngineInterface();
    ~EngineInterface();

    void proceed();

    template<class Msg>
    MsgAnswerHandler sendToEngine(Msg msg, uint32_t itemId = -1);

    template<class Msg>
    void installStreamMsg(std::function<void(Msg, uint32_t)>);

    template<class Msg, class ... Msgs>
    void sendFromEngine(Msg msg, Msgs ... msgs, uint32_t itemId = -1);

    void _pushAnswerEngineSide(const QByteArray &msg, MessageHeader *header);

    template<typename Msg, typename Callable>
    void addConnection(Callable f)
    {
        int type = Msg().getType();

        MessageConnector mConn;
        mConn.connectToMsg<Msg>(f);

        m_msgConnections[type].push_back(mConn);

    }

    void runConnections(int type, QDataStream &s)
    {
        if(m_msgConnections.find(type) != m_msgConnections.end())
        {
            int pos = s.device()->pos();
            for(auto mConn : m_msgConnections[type])
            {
                mConn(s);
                s.device()->seek(pos);
            }
        }
    }

private:
    CircleBuffer<QByteArray> fromEngineBase;
    CircleBuffer<QByteArray> toEngineBase;

    int nextMsgId = 0;
    int nextMsgIdEngineBaseSide = 0;


    MessageAnswerDispatcher* m_answerDispatcher;
    EngineBase* m_engine;

    std::map<int, std::function<int(QDataStream &s, int)>> m_msgFromEngineBaseHandlers;
    std::map<int, std::vector<MessageConnector>> m_msgConnections;
};

template<class Msg, class ... Msgs>
void EngineInterface::sendFromEngine(Msg msg, Msgs ... msgs, uint32_t itemId)
{
    try{
        QByteArray data;
        QDataStream s(&data, QIODevice::WriteOnly);
        //write header
        MessageHeader header;
        header.uid = this->nextMsgIdEngineBaseSide++;
        header.type = Msg().getType();
        header.itemId = itemId;
        header.isAnswer = false;
        s << header;
        //write msg
        msg.serialize(&s);
        fromEngineBase.push(data);
        if constexpr (sizeof...(msgs) > 0) {
            sendFromEngineBase(msgs..., itemId);
        }
    }
    catch(const std::exception &ex)
    {
        qDebug() << "sendFromEngine : Exception" << ex.what();
    }
}

template <class Msg>
MsgAnswerHandler EngineInterface::sendToEngine(Msg msg, uint32_t itemId)
{
    QByteArray data;
    QDataStream s(&data, QIODevice::WriteOnly);
    //write header
    MessageHeader header;
    header.uid = this->nextMsgId++;
    header.type = msg.getType();
    header.itemId = itemId;
    header.isAnswer = false;
    s << header;
    //write msg
    msg.serialize(&s);
    toEngineBase.push(data);
    MsgAnswerHandler handler(m_answerDispatcher, header.uid);
    return handler;
}

template<class Msg>
void EngineInterface::installStreamMsg(std::function<void(Msg, uint32_t)> lambda){

    auto type = Msg().getType();

    auto funcTobeCalled = [lambda](QDataStream &s, int itemId) {
        //call handler
        Msg msg;
        msg.deserialize(&s);
        lambda(msg, itemId);
        return msg.getType();
    };
    m_msgFromEngineBaseHandlers.emplace(type, funcTobeCalled);
}

#endif // ENGINEINTERFACE_H
