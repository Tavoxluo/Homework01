#include "mainwindow.h"
#include "ui_mainwindow.h"

mainwindow::mainwindow(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::mainwindow)
{
    ui->setupUi(this);
    record = new class records();
    connect(record, SIGNAL(close_record()), this, SLOT(show_mainwindow()));
    connect(this, SIGNAL(updateRecodelist(QStringList)), record, SLOT(updateRecodelist(QStringList)));

}

mainwindow::~mainwindow()
{
    delete ui;
}

void mainwindow::show_mainwindow()
{
    this->show();
}

void mainwindow::getUsers(QStringListModel *userListModel, QStringList userlist){
    qDebug()<<"update userlist: " << userListModel;
    qDebug()<< "update online" << userlist;
    //更新ListView的值
    ui->userList->setModel(userListModel);

    //更新comboBox的值
    ui->userBox->clear();
    ui->userBox->addItems(userlist);
}

void mainwindow::acceptParentmsg(QString msg, QString user_id)
{
    this->user_id = user_id;
    ui->msgBro->insertPlainText(msg);
}

void mainwindow::on_closeBtn_clicked()
{
    this->close();
    emit close_main("exit");
}

//群发消息
void mainwindow::on_group_send_clicked()
{
    QString sendmsg, sendTime;
    //消息格式
    //log_id, user_id, user_chat_id, user_chat_state, create_date, log_text

    sendTime = QDateTime::currentDateTime().toString("yyyy-M-dd hh:mm:ss");
    if(ui->msgLineE->text().isEmpty()) {
        QMessageBox::about(NULL, "Infomation!", "发送信息不能为空...");
        return;
    }

    //组合消息
    sendmsg = "group|" + this->user_id +"|group|" + "01|" + sendTime + "|" + ui->msgLineE->text();
    qDebug() << "sendmsg" << sendmsg;
    emit sendMsg(sendmsg);
    ui->msgLineE->clear();
}

void mainwindow::on_friendBtn_clicked()
{
    emit addFriend(ui->friendLineE->text());
}

void mainwindow::on_recordBtn_clicked()
{
    /* 显示记录 */
    this->hide();
    emit updateRecodelist(this->record->userlist);
    record->show();
}

//私发消息
void mainwindow::on_pri_send_clicked()
{
    QString sendmsg, sendTime;

    sendTime = QDateTime::currentDateTime().toString("yyyy-M-dd hh:mm:ss");
    if(ui->msgLineE->text().isEmpty()) {
        QMessageBox::about(NULL, "Infomation!", "发送信息不能为空...");
        return;
    }

    QString user = ui->userBox->currentText();
    if(ui->userBox->currentText().isEmpty()) {
        QMessageBox::critical(this,"error","请选择要私发的用户");
        return;
    }

    sendmsg = "private|" + this->user_id +"|"+ user +"|" + "01|" + sendTime + "|" + ui->msgLineE->text();
    emit sendMsg(sendmsg);
    ui->msgLineE->clear();
}
