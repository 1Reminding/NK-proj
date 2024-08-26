#include "hazard.h"

Monster::Monster(QTimer * t)
{
    timer = t;
    setPixmap(QPixmap(":/hazard/images/monster1.png"));
    setZValue(2);

    beHitSound = new QMediaPlayer();
    beHitSound->setMedia(QUrl("qrc:/sound/resource/monsterhit.mp3"));
}

Monster::~Monster()
{
    if(scene()){
        scene()->removeItem(this);
    }
}

void Monster::collide(Player * player)
{
    if (player->getVel() > 0) {
        if(player->pos().y() < this->pos().y()){
            if(player->doodlejump->getTurnOnSound()) {
                if(beHitSound->state() == QMediaPlayer::PlayingState){
                    beHitSound->setPosition(0);
                } else if(beHitSound->state() == QMediaPlayer::StoppedState) {
                    beHitSound->play();
                }
            }
            connect(timer, SIGNAL(timeout()), this, SLOT(move()));
        }
        player->setVel();
    } else {
        player->setVel(0);
        player->hitByMonster();
    }
}

void Monster::hit()
{
    if(scene()) {
        scene()->removeItem(this);
    }
}

void Hazard::move()
{
    setY(pos().y() + 33);
}

Hole::Hole(QTimer * t)
{
    timer = t;
    setPixmap(QPixmap(":/hazard/images/hole.png"));//添加黑洞图片
    setZValue(2);

    sound = new QMediaPlayer();
    sound->setMedia(QUrl("qrc:/sound/resource/Hole.mp3"));//添加角色被吸入音效
}

Hole::~Hole()
{
    if(scene()){
        scene()->removeItem(this);
    }
}

void Hole::collide(Player * player)
{//当角色触碰边缘，开始对应的动画效果和位置改变
    if(player->doodlejump->getTurnOnSound()) {
        if(sound->state() == QMediaPlayer::PlayingState){
            sound->setPosition(0);
        } else if(sound->state() == QMediaPlayer::StoppedState) {
            sound->play();
        }
    }

    player->stop();//运动停止，大小改变
    player->setPos(pos().x() + 50, pos().y() + 50);
    player->hitByHole();
    connect(timer, SIGNAL(timeout()), player, SLOT(hitByHole()));//游戏结束
}
