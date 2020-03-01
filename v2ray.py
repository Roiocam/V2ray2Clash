
# 说明 : 本脚本提供解析v2ray订阅链接为Clash配置文件的自动化,供学习交流使用.
# 参数 :
#     1. url=订阅地址
#     2. user_path=用户~的路径[cd ~  -> pwd 查看]
#     3. net_config=规则策略.
# Linux自动化更新订阅:
#     - 输入crontab -e编辑定时任务
#     - 模板: [cron表达式] [python路径] [脚本路径] > [输出日志路径]
#     - 例子: 0 0 18 * * ? /usr/bin/python3.8 ~/v2ray.py > ~/auto.log
#     - Arch系也可通过:[cron表达式] systemctl restart clash.service[需自行设置]设置定时任务.在更新订阅后重启Clash-linux 

#属性
url = '订阅地址'
user_path = '用户~目录'
net_config = 'https://raw.githubusercontent.com/Roiocam/V2ray2Clash/master/config.yaml'
#原配置文件地址 = 'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/Pro.yaml'

#V2ray to Clash
import urllib.request
import base64
import json
import datetime
import yaml
import sys
clash_path = '/.config/clash/config.yaml'
def log(msg):
    time = datetime.datetime.now()
    print('['+time.strftime('%Y.%m.%d-%H:%M:%S')+']:'+msg)
#保存到文件
def save_to_file(file_name, contents):
    fh = open(file_name, 'w',encoding="utf-8")
    fh.write(contents.decode('utf-8'))
    fh.close()
#获取订阅地址数据:
def get_proxies(url):
    proxies=[]
    #请求订阅地址
    urllib.request.getproxies()
    urllib.request.ProxyHandler(proxies=None)
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    vmess_raw = base64.b64decode(raw)
    vmess_list = vmess_raw.splitlines()
    log('已获取'+str(len(vmess_list))+'个节点')
    #解析vmess链接为json
    for item in vmess_list:
        b64_proxy = item.decode('utf-8')[8:]
        proxy_str = base64.b64decode(b64_proxy).decode('utf-8')
        proxy = json.loads(proxy_str)
        proxies.append(proxy)
    return proxies
#转换成Clash对象
def translate_proxy(arr):
    log('代理节点转换中...')
    proxies={
        'proxy_list':[],
        'proxy_names':[]
    }
    for item in arr:
        obj = {
            'alterId':item['aid'],
            'cipher':item['type'],
            'name':item['ps'],
            'network':item['net'] if item['net'] and item['net']!= 'tcp' else None,
            'port':item['port'],
            'server':item['add'],
            'tls':True if item['tls']=='tls' else None,
            'type':'vmess',
            'uuid':item['id'],
            'ws-path':item['path'] if item['path'] else None
        }
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        proxies['proxy_list'].append(obj)
        proxies['proxy_names'].append(obj['name'])
    return proxies
def load_local_config(user_path):
    try:
        path = user_path + clash_path
        f = open(path, 'r',encoding="utf-8")
        config = yaml.load(f.read(),Loader=yaml.FullLoader)
        f.close()
        return config
    except FileNotFoundError:
        log('配置文件加载失败')
        sys.exit()
#获取规则策略的配置文件
def get_github_config(user_path):
    try:
        urllib.request.getproxies()
        urllib.request.ProxyHandler(proxies=None)
        raw = urllib.request.urlopen(net_config).read().decode('utf-8')
        config = yaml.load(raw,Loader=yaml.FullLoader)
    except BaseException:
        log('网络获取规则配置失败,加载本地配置文件')
        return load_local_config(user_path)
    log('已获取规则配置文件')
    return config
#将代理添加到配置文件
def add_proxies_to_config(data,config):
    config['Proxy']=data['proxy_list']
    #规则策略的占位符
    placeholder = ['1','2','3','4']
    for group in config['Proxy Group']:
        if group['proxies'] is None:
            group['proxies'] = data['proxy_names']
        replace  = [False for proxy in group['proxies'] if proxy in placeholder]
        if replace:
            group['proxies'] = [proxy for proxy in group['proxies'] if proxy not in placeholder]
            group['proxies'].extend(data['proxy_names'])
    return config
#保存配置文件
def save_config(user_path,config_data):
    path = user_path + clash_path
    lenth = len(config_data['Proxy'])
    config = yaml.dump(config_data,sort_keys=False,default_flow_style=False,encoding='utf-8',allow_unicode=True)
    save_to_file(path,config)
    log('成功更新:'+str(lenth)+'个节点')

#程序入口
config_raw = get_github_config(user_path)
proxy_raw = get_proxies(url)
proxy = translate_proxy(proxy_raw)
config = add_proxies_to_config(proxy,config_raw)
save_config(user_path,config)
