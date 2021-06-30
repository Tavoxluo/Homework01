学长学姐，各位老师您好：
      很高兴在最后能够完成这个项目，虽然中间遇到了很多挫折。由于病人信息的安全性与保密性，各位老师拿到的（附件一：项目代码中并没有真正的database数据集），我将在本地使用真实数据的运行录做视频放置在（附件四：项目汇报视频中）。各位老师与学长学姐可以在视频中对所有的软件构成与操作有一个直观的了解。

由于追求极简风格，在本界面给出常用命令控制说明：
    # show_database                     		显示本地database
    # show_3D                           		显示本地3D文件
    # write_zhou_angle                  		写出支架轴向夹角文件 zhou_angle
    # write_statistics_zhou_angle       		写出支架轴向夹角文件 statistics_zhou_angle
    # write_huan_shape                  		写出支架首尾环文件   huan_shape
*计算机网络命令：
    # -1   - 查看本地ip表 ip-temp表
    # 0    - 发送添加身份请求
    # 1    - LAN发送组网传输回馈 
    # 2.1  - database模块数据传输事务添加请求 使用ip-list
    # 2.2  - database模块数据传输事务添加请求 使用ip-temp-list
    # 3    - 洪泛搜索特定ID患者信息请求       使用inf_flooding_list
*数据库命令
    #append_flooding_list			追加洪泛信息
    #clear_flooding_list			清除本地洪泛信息
    #show_flooding_list			展示洪泛信息
    #use_func_db				使用函数显示病人数据总量
    #select_patient_db			展示数据库
    #select_SQL_db				直接输入模式
    #change_patient_xianzhixing_db		更改数据库中限制性信息
    #change_patient_calculation_db		更改数据库中可运算信息
    #ini_db					初始化本地数据库
    #delete_all_db				清空本地数据库
    #show_permission_db			展示登录账号权限
    #show_self_roles_db			展示登录使用角色


