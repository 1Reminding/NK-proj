#include "player.h"
#include "platform.h"
#include "bullet.h"
#include "hazard.h"
#include <QPixmap>
#include <QDebug>

Player::Player(int x, int y, QTimer * t, DoodleJump * dj)
{
    vel = -30;
    doodlejump = dj;
    status = 1;
    count = 0;
    shield = false;
    isHit = false;
    props = NULL;
    timer = t;
    left = false;
    right = false;
    space = false;

    mouth = new QGraphicsPixmapItem(QPixmap(":/player/images/player_Mouth.png"));
    mouth->setZValue(5);

    star_imgs[0].load(":/player/images/star1.png");//角色击落素材添加
    star_imgs[1].load(":/player/images/star2.png");
    star_imgs[2].load(":/player/images/star3.png");

    star = new QGraphicsPixmapItem(star_imgs[0]);
    star->setZValue(5);

    //角色不同运动状态的动作素材设置
    imgs[0][0].load(":/player/images/player_L.png");
    imgs[0][1].load(":/player/images/player_Left_Jump.png");
    imgs[1][0].load(":/player/images/player_Right.png");
    imgs[1][1].load(":/player/images/player_Right_Jump.png");
    imgs[2][0].load(":/player/images/player_Shoot.png");
    imgs[2][1].load(":/player/images/player_Shoot_Jump.png");
    setPixmap(imgs[0][0]); // need to change
    setPos(x, y);
    setZValue(4);

    connect(timer, SIGNAL(timeout()), this, SLOT(move()));
    connect(timer, SIGNAL(timeout()), this, SLOT(moveEvent()));

    // 使角色可聚焦并且设置为当前的焦点
    setFlag(QGraphicsItem::ItemIsFocusable);

    bulletsound = new QMediaPlayer();
    bulletsound->setMedia(QUrl("qrc:/sound/resource/bullet.mp3"));//子弹声
    hitsound = new QMediaPlayer();
    hitsound->setMedia(QUrl("qrc:/sound/resource/Monstercollide.mp3"));//击中怪兽的声音
}

void Player::keyPressEvent(QKeyEvent *event)
{
    switch (event->key()) {
    case Qt::Key_A:
    case Qt::Key_Left://A键实现角色向左移动
        left = true;
        break;
    case Qt::Key_D://D键实现角色向右移动
    case Qt::Key_Right:
        right = true;
        break;
    case Qt::Key_Space:
        space = true;
        break;
    default:
        break;
    }

    return;
}

void Player::keyReleaseEvent(QKeyEvent * event)
{
    switch (event->key()) {
    case Qt::Key_A:
    case Qt::Key_Left:
        left = false;
        break;
    case Qt::Key_D:
    case Qt::Key_Right:
        right = false;
        break;
    case Qt::Key_Space:
        space = false;
        break;
    default:
        break;
    }

}

void Player::moveEvent()
{
    static const int offset = pixmap().width() / 2; // 填充图片空白
    static const int DISPL = 15; //移位替代

    if(left){//角色向左运动，如果有支持物（平台或者弹簧），进行下一次位移操作
        setX(pos().x() - DISPL < -pixmap().width() + offset? 600 - offset : pos().x() - DISPL);
        if(status != 0){
            if(status == 2){
                scene()->removeItem(mouth);
                count = 0;
            }
            status = 0;
            setPixmap(imgs[status][0]);
        }
        if(props){
            props->setPos(pos().x() + 35, pos().y());
        }
    }

    if(right){//角色向右运动，如果有支持物（平台或者弹簧），进行下一次位移操作
        setX(pos().x() + DISPL > 600 - offset? -pixmap().width() + offset : pos().x() + DISPL);
        if(status != 1){
            if(status == 2){
                scene()->removeItem(mouth);
                count = 0;
            }
            status = 1;
            setPixmap(imgs[status][0]);
        }
        if(props){
            props->setPos(pos().x() + 2, pos().y());
        }
    }
//角色换边
    if(space){
        if(status != 2 || count > 2){
            shoot();
        }
    }

    if(props){
        if(status == 0){
            props->setPos(pos().x() + 35, pos().y());
        } else if (status == 1) {
            props->setPos(pos().x() + 2, pos().y());
        }
    }
}

void Player::setVel(float v)
{
    if(!isHit){
        setPixmap(imgs[status][1]);
        vel = v;
    }
}

void Player::start()
{
    setFocus();
    connect(timer, SIGNAL(timeout()), this, SLOT(move()));
    connect(timer, SIGNAL(timeout()), this, SLOT(moveEvent()));
}

void Player::stop()
{
    clearFocus();
    disconnect(timer, SIGNAL(timeout()), this, SLOT(move()));
    disconnect(timer, SIGNAL(timeout()), this, SLOT(moveEvent()));
}

int Player::getVel()
{
    return vel;
}

void Player::shoot()
{//发射子弹
    if(bulletsound->state() == QMediaPlayer::PlayingState){
        bulletsound->setPosition(0);
    } else if(bulletsound->state() == QMediaPlayer::StoppedState) {
        bulletsound->play();
    }
//图像拼接，将角色的嘴巴拼接在上扬的头顶
    mouth->setPos(x() + 35, y());
    if(status != 2){
        scene()->addItem(mouth);
    }
    setPixmap(imgs[2][0]);
    Bullet * bullet = new Bullet(timer, y() - 1000);
    bullet->setPos(x() + 35, y() - 5);
    scene()->addItem(bullet);
    status = 2;
}

void Player::hitByMonster()
{
    if(doodlejump->getTurnOnSound()){
        if(hitsound->state() == QMediaPlayer::PlayingState){
            hitsound->setPosition(0);
        } else if(bulletsound->state() == QMediaPlayer::StoppedState) {
            hitsound->play();
        }
    }
    isHit = true;//位置更新，下落
    star->setPos(pos().x() + 10, pos().y());
    scene()->addItem(star);//撞击后的动画效果设置
}

void Player::hitByHole()
{//被黑洞窗子吸进去，游戏结束，角色下落结束画面，更新图像和位置
    if(pixmap().width() < 20){
        setPos(-100, -1000);
        start();
        doodlejump->isEnd = true;
        disconnect(doodlejump->timer, SIGNAL(timeout()), this, SLOT(hitByHole()));
        return;
    }
    setPixmap(QPixmap(imgs[status][0]).scaled(pixmap().width()-10, pixmap().height()-10,Qt::KeepAspectRatio));
    return;
}

void Player::reset()
{
    if(star->scene()){
        star->scene()->removeItem(star);
    }
    isHit = false;
    setPixmap(imgs[1][0]);
    left = false;
    right = false;
    space = false;
}

int Player::getStatus()
{
    return status;
}

void Player::move()
{
    static int t = 0;
    setPixmap(imgs[status][0]);

    // 设置玩家的掉落情况
    vel += 15;//探索出来的合适数值，数字越大每次跳起高度越低，数值越小高度越高【（15,0.5）作为实验值】
    if(!doodlejump->isEnd){
        if(vel >30){
           vel = 30;//用来控制角色的下落速度，大于vel时全部更新为vel为了保证下落时的匀速状态，数值越小下落速度越慢【5作为测试数据】
        }
    }
    if (isHit){
        setY(pos().y() + vel);
        star->setPixmap(star_imgs[t/2]);
        star->setPos(pos().x() + 10, pos().y());
        ++t;
        if(t > 5){
            t = 0;
        }
        return;
    }
    setY(pos().y() + vel);

    if(status == 2){
        mouth->setPos(x() + 35, y());
        if(count++ > 3){
            if(mouth->scene()) {
                scene()->removeItem(mouth);
            }
            count = 0;
            status = 1;
        }
    }

    // 检查碰撞情况
    QList<QGraphicsItem*> colliding_items = collidingItems();
    for(int i = 0, n = colliding_items.size();i<n; ++i){
        Platform * platform = dynamic_cast<Platform *>(colliding_items[i]);
        if(platform){
            platform->collide(this);
        }
        Props * props = dynamic_cast<Props *>(colliding_items[i]);
        if(props){
            props->collide(this);
        }
        Hazard * hazard = dynamic_cast<Hazard *>(colliding_items[i]);
        if(hazard){
            hazard->collide(this);
        }
    }

    return;
}
