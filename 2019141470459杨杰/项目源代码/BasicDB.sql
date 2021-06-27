drop database if exists bank_db;
create database if not exists bank_db;
use bank_db;
drop table if exists web_account;
create table if not exists web_account(
    username varchar(10) primary key comment'web账户',
    web_password varchar(15) not null comment'web密码',
    acc_power boolean not null comment'账户权限',
    id_num char(18) comment'身份证号',
    client_location varchar(50) comment'地址',
    telephone char(11) comment'手机号',
    client_name varchar(10) comment'开户姓名',
    web_status boolean not null comment'web账户状态',
    connect_status boolean not null comment'连接状态'
)charset=utf8 comment='web账户表';

drop table if exists web_associ_bank;
create table if not exists web_associ_bank(
    username varchar(10) primary key comment'web账户',
    bank_card_id char(5) not null comment'关联web账户名',
    associ_date datetime not null comment'关联时间',
    associ_status boolean not null comment'关联状态'
)charset=utf8 comment='web_bank关联表';

drop table if exists bank_account;
create table if not exists bank_account(
    bank_card_id char(5) primary key comment'银行卡卡号',
    card_password varchar(15) not null comment'银行卡密码',
    acc_start_date datetime not null comment'开户时间',
    acc_end_date datetime comment'销户时间',
    left_money decimal(9,2) not null comment'余额',
    bank_status boolean not null comment'账户状态'
)charset=utf8 comment='银行卡表';

drop table if exists web_acc_log;
create table if not exists web_acc_log(
    log_record_id int(20) primary key comment'登录记录唯一编号',
    username varchar(10) not null comment'登录者',
    log_ip varchar(20) not null comment'登录ip地址'
)charset=utf8 comment='登录记录关联表';

drop table if exists acc_log_record;
create table if not exists acc_log_record(
    log_record_id int(20) primary key comment'账户操作记录唯一编号',
    log_oper_time datetime comment'账户操作时间',
    log_kind varchar(15) comment'账户操作类型'
)charset=utf8 comment='账户登录记录表';

drop table if exists acc_oper_record;
create table if not exists acc_oper_record(
    oper_record_id int(20) primary key comment'操作记录唯一编号',
    oper_date datetime comment'操作时间',
    oper_kind varchar(10) not null comment'操作类型',
    do_oper varchar(10) not null comment'操作发出者',
    fin_oper varchar(10) comment'被操作者',
    oper_value decimal(9,2) comment'操作值',
    oper_result boolean not null comment'操作结果',
    remark text comment'备注'
)charset=utf8 comment='对银行卡内容的操作记录表';

drop table if exists bank_acc_oper;
create table if not exists bank_acc_oper(
    oper_record_id int(20) primary key auto_increment comment'操作记录唯一编号',
    bank_card_id char(19) comment'银行卡卡号'
)charset=utf8 comment='银行卡操作记录关联表';

set global log_bin_trust_function_creators=TRUE;
set @x=1;

delimiter $$
drop function if exists getmoney$$
create function getmoney(card_id char(5)) returns decimal(9,2)
begin
    declare return_money decimal(9,2);
    select left_money from bank_account where bank_card_id=card_id into return_money;
    return return_money;
end $$
delimiter ;

delimiter $$
drop procedure if exists create_new_web_acc$$
create procedure create_new_web_acc(in username varchar(10),in web_password varchar(15),in id_num char(18),in client_location varchar(50),in telephone char(11),in client_name varchar(10))
begin
    insert into web_account values(
        username,
        web_password,
        false,
        id_num,
        client_location,
        telephone,
        client_name,
        true,
        false
    );
end $$
delimiter ;

delimiter $$
drop procedure if exists insert_log_record$$
create procedure insert_log_record(in temp_log_id int(8),in log_kind varchar(15),in username varchar(10),in log_ip varchar(20))
begin
    insert into acc_log_record values(temp_log_id,now(),log_kind);
    insert into web_acc_log values(temp_log_id,username,log_ip);
end $$
delimiter ;

delimiter $$
drop procedure if exists insert_oper_record$$
create procedure insert_oper_record(in temp_oper_id int(8),in oper_kind varchar(10),in do_oper varchar(10),in fin_oper varchar(10),in oper_value decimal(9,2),in oper_result boolean,in remark text)
begin
    insert into acc_oper_record values(temp_oper_id,now(),oper_kind,do_oper,fin_oper,oper_value,oper_result,remark);
    insert into bank_acc_oper values(temp_oper_id,bank_card_id);
end $$
delimiter ;

delimiter $$
drop procedure if exists delete_web_acc$$
create procedure delete_web_acc(in id int(8),in delusername varchar(10),in ip int(10))
begin
    call deconnect_web_bank(delusername);
    call insert_log_record(id,'deleteaccount',delusername,ip);
    update web_account set web_status=false where username=delusername;
end $$
delimiter ;

delimiter $$
drop procedure if exists logout_acc$$
create procedure logout_acc(in id int(8),in username varchar(10),in ip int(10))
begin
    call insert_log_record(id,'logout',username,ip);
end $$
delimiter ;

delimiter $$
drop procedure if exists check_power$$
create procedure check_power(in username varchar(10),in temp_password varchar(15))
begin
    declare acc_num int;
    declare get_power boolean;
    select count(*) from web_account where username=username and web_password=temp_password into acc_num;
    if acc_num=1 then
    select acc_power from web_account where username=username into get_power;
    else
    set get_power=null;
    end if;
    select get_power;
end $$
delimiter ;

delimiter $$
drop procedure if exists check_bank_acc$$
create procedure check_bank_acc(in card_id char(5),in card_pass varchar(15),out temp_status boolean)
begin
    declare acc_count int;
    select count(*) from bank_account where bank_card_id=card_id and card_password=card_pass into acc_count;
    if acc_count=1 then
    select bank_status from bank_account where bank_card_id=card_id into temp_status;
    else
    set temp_status=null;
    end if;
end $$
delimiter ;

delimiter $$
drop procedure if exists connect_web_bank$$
create procedure connect_web_bank(in username varchar(10),in card_id char(5),in card_pass varchar(15),out con_status boolean)
begin
    declare bk_status boolean default false;
    call check_bank_acc(card_id,card_pass,bk_status);
    case bk_status
    when false then
    update web_account set connect_status=true where username=username;
    update bank_account set bank_status=true where bank_card_id=card_id;
    insert into web_associ_bank values(username,card_id,now(),true);
    set con_status=true;
    else
    set con_status=false;
    end case;
end $$
delimiter ;

delimiter $$
drop procedure if exists deconnect_web_bank$$
create procedure deconnect_web_bank(in id int(8),in delusername varchar(10),out decon_status boolean)
begin
    declare card_id char(5);
    select bank_card_id from web_associ_bank where username=delusername and associ_status=true into card_id;
    call insert_oper_record(id,'deconnect',card_id,card_id,0.00,true,null);
    update bank_account set bank_status=false where bank_card_id=card_id;
    update web_account set connect_status=false where username=delusername;
    delete from web_associ_bank where username=delusername;
    set decon_status=true;
end $$
delimiter ;

delimiter $$
drop procedure if exists select_log_record$$
create procedure select_log_record(in username varchar(10))
begin
    select log_oper_time,log_kind,log_ip from web_acc_log natural join acc_log_record where username=username;
end $$
delimiter ;

delimiter $$
drop procedure if exists select_oper_record$$
create procedure select_oper_record(in id int(8),in card_id char(5))
begin
    call insert_oper_record(id,'check',card_id,card_id,0.00,true,null);
    select oper_date,oper_kind,do_oper,fin_oper,oper_value,oper_result,remark from acc_oper_record natural join bank_acc_oper  where bank_card_id=card_id;
end $$
delimiter ;

delimiter $$
drop procedure if exists deposit$$
create procedure deposit(in id int(8),in card_id char(5),in add_value decimal(9,2))
begin
    declare fin_st boolean;
    call insert_oper_record(id,'deposit',card_id,card_id,add_value,true,null);
    update bank_account set left_money=left_money+add_value where bank_card_id=card_id;
    set fin_st=true;
    select fin_st;
end $$
delimiter ;

delimiter $$
drop procedure if exists withdrawal$$
create procedure withdrawal(in id int(8),in card_id char(5),in dec_value decimal(9,2))
begin
    declare left_mon decimal(9,2);
    declare fin_st boolean;
    set left_mon=getmoney(card_id);
    set left_mon=left_mon-dec_value;
    if left_mon>0 then
    call insert_oper_record(id,'withdrawal',card_id,card_id,dec_value,true,null);
    update bank_account set left_money=left_money-dec_value where bank_card_id=card_id;
    set fin_st=true;
    else
    call insert_oper_record(id,'withdrawal',card_id,card_id,dec_value,flase,null);
    set fin_st=false;
    end if;
    select fin_st;
end $$
delimiter ;

delimiter $$
drop procedure if exists transfer_money$$
create procedure transfer_money(in id int(8),in do_card_id char(5),in to_card_id char(5),in trans_value decimal(9,2))
begin
    declare left_mon decimal(9,2);
    declare fin_st boolean;
    set left_mon=getmoney(do_card_id);
    set left_mon=left_mon-trans_value;
    if left_mon>0 then
    call insert_oper_record(id,'transfer',do_card_id,to_card_id,trans_value,true,null);
    update bank_account set left_money=left_money-trans_value where bank_card_id=do_card_id;
    update bank_account set left_money=left_money+trans_value where bank_card_id=to_card_id;
    set fin_st=true;
    else
    call insert_oper_record(id,'transfer',do_card_id,to_card_id,trans_value,flase,null);
    set fin_st=false;
    end if;
    select fin_st;
end $$
delimiter ;

insert into web_account
values('abcd','16415636867',false,'130421198011154478','Beijing','13642345112','Zhangsan',true,false),
      ('efg','45984848449',false,'350402199401267511','Shandong','13318877954','Lisi',true,false),
      ('hyjk','14587716458',true,'211381198301121510','Hebei','13642345112','Wangwu',true,false);
insert into bank_account values('16516','16415636867',now(),null,500.00,false),
    ('91565','45984848449',now(),null,900.00,false);

insert into acc_oper_record
values(101472,now(),'deposit',91565,91565,5959.00,1,''),
(109472,now(),'deposit',91565,91565,2000.00,1,''),
(117270,now(),'deposit',91565,91565,800.00,1,''),
(125083,now(),'deposit',91565,91565,9000.00,1,''),
(252920,now(),'deposit',91565,91565,6000.00,1,''),
(252925,now(),'deposit',91565,91565,400.00,1,''),
(292920,now(),'deposit',91565,91565,900.00,1,'');

insert into acc_oper_record
values(101372,now(),'deposit',16516,16516,5959.00,1,''),
(101672,now(),'deposit',16516,16516,2000.00,1,''),
(117870,now(),'deposit',16516,16516,800.00,1,''),
(122083,now(),'deposit',16516,16516,9000.00,1,''),
(252420,now(),'deposit',16516,16516,6000.00,1,''),
(252965,now(),'deposit',16516,16516,400.00,1,''),
(292950,now(),'deposit',16516,16516,900.00,1,'');

drop user if exists 'client'@'localhost';
drop user if exists 'administor'@'localhost';
create user if not exists 'client'@'localhost' identified by '123456789';
create user if not exists'administor'@'localhost' identified by '20001227';

grant execute on function getmoney to 'client'@'localhost';
grant execute on procedure create_new_web_acc to 'client'@'localhost';
grant execute on procedure insert_log_record to 'client'@'localhost';
grant execute on procedure insert_oper_record to 'client'@'localhost';
grant execute on procedure delete_web_acc to 'client'@'localhost';
grant execute on procedure logout_acc to 'client'@'localhost';
grant execute on procedure check_power to 'client'@'localhost';
grant execute on procedure check_bank_acc to 'client'@'localhost';
grant execute on procedure connect_web_bank to 'client'@'localhost';
grant execute on procedure deconnect_web_bank to 'client'@'localhost';
grant execute on procedure select_log_record to 'client'@'localhost';
grant execute on procedure select_oper_record to 'client'@'localhost';
grant execute on procedure deposit to 'client'@'localhost';
grant execute on procedure withdrawal to 'client'@'localhost';
grant execute on procedure transfer_money to 'client'@'localhost';


grant execute on function getmoney to 'administor'@'localhost';
grant execute on procedure create_new_web_acc to 'administor'@'localhost';
grant execute on procedure insert_log_record to 'administor'@'localhost';
grant execute on procedure insert_oper_record to 'administor'@'localhost';
grant execute on procedure delete_web_acc to 'administor'@'localhost';
grant execute on procedure logout_acc to 'administor'@'localhost';
grant execute on procedure check_power to 'administor'@'localhost';
grant execute on procedure check_bank_acc to 'administor'@'localhost';
grant execute on procedure connect_web_bank to 'administor'@'localhost';
grant execute on procedure deconnect_web_bank to 'administor'@'localhost';
grant execute on procedure select_log_record to 'administor'@'localhost';
grant execute on procedure select_oper_record to 'administor'@'localhost';
grant execute on procedure deposit to 'administor'@'localhost';
grant execute on procedure withdrawal to 'administor'@'localhost';
grant execute on procedure transfer_money to 'administor'@'localhost';
grant select on bank_db.* to 'administor'@'localhost';


