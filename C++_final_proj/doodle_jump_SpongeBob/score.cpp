#include "score.h"

#include <QFile>
#include <QPixmap>
#include <QGraphicsTextItem>
#include <QGraphicsPixmapItem>
#include <QFont>
#include <QFontDatabase>
#include <QDebug>
#include <algorithm>

NameScore::NameScore(QString s)
{
    int id = QFontDatabase::addApplicationFont(":/font/resource/DoodleJump.ttf");
    QString family = QFontDatabase::applicationFontFamilies(id).at(0);
    QFont font(family);
    font.setPixelSize(48);

    QStringList list = s.split('#');
    name = list.at(0);
    score = list.at(1).toInt();
    nameGraphics = new QGraphicsTextItem;
    nameGraphics->setFont(font);
    nameGraphics->setPlainText(list.at(0));
    nameGraphics->setZValue(1);
    scoreGraphics = new QGraphicsTextItem;
    scoreGraphics->setFont(font);
    scoreGraphics->setPlainText(list.at(1));
    rank = new QGraphicsTextItem;
    nameGraphics->setZValue(1);
    rank->setFont(font);
    rank->setPlainText("0. ");
    rank->setZValue(1);
}

Score::Score()
{
    rank = new Rank();
    rank->setFlag(QGraphicsItem::ItemIsFocusable);
}

void Score::read()
{
    QFile file("/score");
    if(!file.open(QIODevice::ReadOnly | QIODevice::Text)){
        qDebug() << "Fail to read file: score";
        return;
    }
    QTextStream in(&file);
    QString input = in.readAll();
    if(input != NULL){
        QStringList list = input.split('\n');
        for(auto str: list){
            NameScore ns(str);
            data.push_back(ns);
        }
    }
    file.close();
}

void Score::save()
{
    QFile file("/score");
    if(!file.open(QIODevice::WriteOnly | QIODevice::Text)){
        qDebug() << "Fail to save file: score";
        return;
    }
    QTextStream out(&file);
    for(auto ns: data){
        out << ns.name << '#' << ns.score << '\n';
    }
    file.close();
}

void Score::add(QString name, int score)
{
    NameScore ns(name + '#' + QString::number(score));
    data.push_back(ns);
}

int Score::findHighScore(QString name)
{
    int score = 0;
    for(auto ns: data){
        if(ns.name == name){
            if(ns.score > score){
                score = ns.score;
            }
        }
    }
    return score;
}

void Score::addToScene(QGraphicsScene * scene)
{
    int id = QFontDatabase::addApplicationFont(":/font/resource/DoodleJump.ttf");
    QString family = QFontDatabase::applicationFontFamilies(id).at(0);
    QFont font(family);
    font.setBold(true);
    font.setPixelSize(20);

    QGraphicsTextItem * text = NULL;
    QGraphicsPixmapItem * line = NULL;
    for(auto ns: data){
        text = new QGraphicsTextItem;
        line = new QGraphicsPixmapItem(QPixmap(":/background/images/line.png"));

        text->setFont(font);
        text->setPlainText(ns.name);
        text->setPos(640-text->boundingRect().width(), -ns.score + 490);
        text->setZValue(4);
        line->setPos(640 - line->pixmap().width(), -ns.score + 520);
        line->setZValue(4);

        graphics.push_back(text);
        graphics.push_back(line);

        scene->addItem(text);
        scene->addItem(line);
    }
}

void Score::clean(QGraphicsScene * scene)
{
    for(auto graphic: graphics){
        if(graphic->scene()){
            scene->removeItem(graphic);
        }
        delete  graphic;
    }
    graphics.clear();
}

bool cmp(NameScore& a, NameScore& b){
    return a.score > b.score;
}

void Score::addRankToScene(QGraphicsScene * scene)
{
    QGraphicsPixmapItem * bar = NULL;
    int x = 110, y = 200, i = 0;
    std::sort(data.begin(), data.end(), cmp);
    for(auto record: data){
        record.rank->setPlainText(QString::number(++i)+". ");
        record.rank->setPos(x, y);
        record.nameGraphics->setPos(x + 50, y);
        record.scoreGraphics->setPos(640 - record.scoreGraphics->boundingRect().width(), y);
        if(i%2==1){
            bar = new QGraphicsPixmapItem;
            bar->setPixmap(QPixmap(":/background/images/bar.png"));
            bar->setPos(x - 10, y - 20);
            rank->addToGroup(bar);
        }
        rank->addToGroup(record.rank);
        rank->addToGroup(record.nameGraphics);
        rank->addToGroup(record.scoreGraphics);
        y += 81;
    }

    scene->addItem(rank);
    rank->setFocus();
}

void Rank::keyPressEvent(QKeyEvent * event)
{
    if(boundingRect().height() > 567){
        switch (event->key()) {
        case Qt::Key_Up:
            setY(pos().y() + ((pos().y() >= 0)? 0 : 20));
            break;
        case Qt::Key_Down:
            setY(pos().y() + ((pos().y() <= -(boundingRect().height() - 587))? 0 : -20));
            break;
        default:
            break;
        }
    }
}
