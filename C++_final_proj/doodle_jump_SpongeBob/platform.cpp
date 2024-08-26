#include "platform.h"
#include <QPixmap>
#include <QDebug>

Platform::Platform(): props(NULL), timer(NULL), VEL(0){}

NormalPlatform::NormalPlatform(QTimer * time)//普通平台的设置，支持角色位置更新向上跳跃
{
    timer = time;
    setPixmap(QPixmap(":/platform/images/Normal_Platform.png", "PNG"));
    setZValue(1);
    sound = new QMediaPlayer();
    sound->setMedia(QUrl("qrc:/sound/resource/jump.mp3"));
}

NormalPlatform::~NormalPlatform()
{
    if(scene()){
        scene()->removeItem(this);
    }
    if(props){
        delete props;
    }
}

void NormalPlatform::collide(Player * player)//普通平台可以实现支持玩家位置改变
{
    if(player->getVel() > 0){
        if(player->pos().y() + player->pixmap().height() >= pos().y() && \
           player->pos().y() + player->pixmap().height() <= pos().y() + pixmap().height())
        {

            if(player->doodlejump->getTurnOnSound()) {
                if(sound->state() == QMediaPlayer::PlayingState){
                    sound->setPosition(0);
                } else if(sound->state() == QMediaPlayer::StoppedState) {
                    sound->play();
                }
            }
            player->setVel();
        }
    }
}

void NormalPlatform::spawnProps()
{
    //NormalPlatform位置随机生成
    int p = rand() % 100;
    if(p >= 10){
        props = new Spring();
    } else if (p >= 0) {
        props = new PropellerHelmet(this, timer);
    }

}

CrackedPlatform::CrackedPlatform(QTimer * t)
{
    //Cracked_Platform动画和对应音效设置
    img[0] = QPixmap(":/platform/images/Cracked_Platform1.png", "PNG");
    img[1] = QPixmap(":/platform/images/Cracked_Platform2.png", "PNG");
    img[2] = QPixmap(":/platform/images/Cracked_Platform3.png", "PNG");
    img[3] = QPixmap(":/platform/images/Cracked_Platform4.png", "PNG");

    setPixmap(img[0]);
    setZValue(1);

    timer = t;
    VEL = 7;
    count = 0;

    sound = new QMediaPlayer();
    sound->setMedia(QUrl("qrc:/sound/resource/cracked_platform.mp3"));
}

CrackedPlatform::~CrackedPlatform()
{
    if(timer!=NULL){
        disconnect(timer, SIGNAL(timeout()), this, SLOT(falling()));
    }
}

void CrackedPlatform::collide(Player * player)
{
    //碰撞过程的设置， CrackedPlatform不能支持玩家位置更新，不能完成下一次在该平台上的跳跃
    if(player->getVel() > 0){
        if(player->pos().y() + player->pixmap().height() >= pos().y() && \
           player->pos().y() + player->pixmap().height() <= pos().y() + pixmap().height()){
            if(player->doodlejump->getTurnOnSound()){
                if(sound->state() == QMediaPlayer::PlayingState){
                    sound->setPosition(0);
                } else if(sound->state() == QMediaPlayer::StoppedState) {
                    sound->play();
                }
            }
            connect(timer, SIGNAL(timeout()), this, SLOT(falling()));
        }
    }

}

void CrackedPlatform::falling()// CrackedPlatform上玩家的下落与之前正常的下落保持一致
{
    if(count < 4){
        setPixmap(img[count]);
        ++count;
    }
    setY(pos().y() + VEL);
}

HorizontalMovePlatform::HorizontalMovePlatform(QTimer * time):NormalPlatform(time)
{
    //HorizontalMovePlatform的素材设置
    setPixmap(QPixmap(":/platform/images/Horiziontal_Move_Platform.png", "PNG"));
    setZValue(1);

    connect(timer, SIGNAL(timeout()), this, SLOT(move()));

    VEL = 3;
}

HorizontalMovePlatform::~HorizontalMovePlatform()
{
    disconnect(timer, SIGNAL(timeout()), this, SLOT(move()));
}

void HorizontalMovePlatform::move()
{
    //HorizontalMovePlatform位置移动设置，在窗口内实现左右移动，到达边界反向运动
    if(pos().x() + pixmap().width() + VEL > 640 || pos().x() + VEL < 0){
        VEL *= -1;
    }
    setX(pos().x() + VEL);
}

OneOffPlatform::OneOffPlatform(QTimer * time):NormalPlatform(time)
{
    //OneOffPlatform的素材设置
    setPixmap(QPixmap(":/platform/images/One-off_Platform1.png", "PNG"));
    setZValue(1);
}

OneOffPlatform::~OneOffPlatform()
{
    if(scene()){
        scene()->removeItem(this);
    }
}

void OneOffPlatform::collide(Player * player)
{
    //OneOffPlatform的碰撞动画设置
    if(player->getVel() > 0){
        if(player->pos().y() + player->pixmap().height() >= pos().y() && \
           player->pos().y() + player->pixmap().height() <= pos().y() + pixmap().height())
        {

            if(player->doodlejump->getTurnOnSound()) {
                if(sound->state() == QMediaPlayer::PlayingState){
                    sound->setPosition(0);
                } else if(sound->state() == QMediaPlayer::StoppedState) {
                    sound->play();
                }
            }
            player->setVel();
            hide();//实现OneOffPlatform在与角色碰撞之后隐藏，不能再次使用
        }
    }
}
