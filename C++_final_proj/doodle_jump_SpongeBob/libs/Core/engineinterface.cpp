#include "messageheader.h"
#include "engineinterface.h"
#include "messagenegotiator.h"

//store over than 500 object creation msgs
EngineInterface::EngineInterface(): fromEngineBase(46000), toEngineBase(46000)
{
    m_answerDispatcher = new MessageAnswerDispatcher;
}

EngineInterface::~EngineInterface()
{
    delete m_answerDispatcher;
}

void EngineInterface::proceed()
{
    try
    {
        while (true)
        {
            auto bA = fromEngineBase.pop();
            if (bA.size() < 4) break; //no message to proceed
            QDataStream s(bA);
            MessageHeader h;
            s >> h;
            //proceed answer
            int pos = s.device()->pos();
            if (h.isAnswer)
            {
                m_answerDispatcher->proceedMsgAnswer(h, s);
            }
            else
            {
                auto search = m_msgFromEngineBaseHandlers.find(h.type);
                if(search != m_msgFromEngineBaseHandlers.end())
                {
                    search->second(s, h.itemId);
                }
            }
            s.device()->seek(pos);
            runConnections(h.type, s);
        }
    }
    catch(const std::exception& ex)
    {
        qCritical() << "EngineInterface::proceed failed. Error:" << ex.what();
    }
}

void EngineInterface::_pushAnswerEngineSide(const QByteArray & msg, MessageHeader * header)
{
    QByteArray data;
    QDataStream s(&data, QIODevice::ReadWrite);
    s << *header;
    data.append(msg);
    fromEngineBase.push(data);
}
