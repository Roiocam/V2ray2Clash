# V2ray2Clash

#### 说明 : 本脚本提供解析v2ray订阅链接为Clash配置文件的自动化,供学习交流使用.
#### 参数 :
     1. url=订阅地址
     2. user_path=用户~的路径[cd ~  -> pwd 查看]
     3. net_config=规则策略.
#### 使用说明:
     1. 安装python : 
          - [Arch]: sudo pacman -S python 
          - [Ubuntu]: sudo apt install python3 
          - [Centos]: sudo yum install python3
     2. 填写订阅地址和用户路径
     3. 执行命令 (python3 ./v2ray.py)
#### Linux自动化更新订阅:
     - 输入crontab -e编辑定时任务
     - 模板: [cron表达式] [python路径] [脚本路径] > [输出日志路径]    
     - 例子: 0 0 18 * * ? /usr/bin/python3.8 ~/v2ray.py > ~/auto.log
     - Arch系也可通过:[cron表达式] systemctl restart clash.service[需自行设置]设置定时任务.在更新订阅后重启Clash-linux 
     
