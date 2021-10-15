# -*- coding: utf-8 -*-
# 哔哩哔哩自动完成任务 V1.4 (beta)
# 本程序可以帮你自动完成B站可获取经验值的任务，让你快速涨经验值、升级！
# 作者：两位B站用户：肥宅水水呀（https://space.bilibili.com/324042405）  编写代码主体
#                    wuziqian211（https://space.bilibili.com/425503913）       修改错误、完善代码、增加新功能
# 2020年9月26日   由 肥宅水水呀 编写批处理版本
# 2020年9月28日   由 肥宅水水呀 重写python版本
# 2020年10月6日   由 wuziqian211      修改python版本
# 2020年10月10日  本程序主体功能已完善
# 2020年1月12日   由 肥宅水水呀 优化python版本

import os
import sys
import requests
import time
import colorama
from contextlib import closing

version = "1.4(beta)" # 版本号
appdata = os.getenv ("Appdata") # 获取环境变量Appdata的值
true = True
false = False
null = None
colorama.init (autoreset = True) # 初始化彩色文字，并且设置颜色自动恢复

# 彩色文字用法："\033[{显示方式};{前景色};{背景色}m" + 文字 + "\033[0m"
# 数值表示的参数含义：
# 显示方式  0（默认）   1（高亮）   22（非粗体）  4（下划线）  24（非下划线）  5（闪烁）   25（非闪烁）  7（反显）   27（非反显）
# 前景色    30（黑色）  31（红色）  32（绿色）    33（黄色）   34（蓝色）      35（洋红）  36（青色）    37（白色）
# 背景色    40（黑色）  41（红色）  42（绿色）    43（黄色）   44（蓝色）      45（洋红）  46（青色）    47（白色）

def isConnected (): # 判断网络是否连接正常
    try: # 异常调试
        requests.get ("https://www.bilibili.com/")
    except: # 如果requests请求异常，执行except内的操作
        return False
    return True

def update (): # 检查更新
    try: # 异常调试
        update = requests.get ("https://happycola.gitee.io/bili-auto-task-update/index.json", timeout = 5) # 从更新服务器获取数据，请求超时时间设为5秒
    except: # 如果requests请求异常，执行except内的操作
        print ("\033[1;37mConnect Timeout\033[0m（访问更新服务器请求超时，程序可能无法及时获取更新！）") # 彩色文字：白色，代号37
        check () # 检查配置文件是否存在
        return
    if update.status_code == 200: # 判断服务器响应状态码是否正常
        update_message = eval (update.text) ["message"]
        if update_message == "ok": # 判断该程序还能正常使用（如果变量update_message的值不等于“ok”，则代表该程序因特殊原因被作者停止使用）
            update_version = eval (update.text) ["data"] ["version"]
            if update_version != version: # 版本不相同，说明有新版本
                print ("检测到新版本：\033[1;36mv" + update_version + "\033[0m（当前版本：\033[1;37mv" + version + "\033[0m）")
                update_content = eval (update.text) ["data"] ["content"]
                print (update_content)
                print ()
                print ("是否更新？")
                
                while True: # 一直循环
                    update_choose = input ("输入1立即更新，输入2则跳过更新 [1/2] ")
                    if update_choose == "1" or update_choose == "2": # 用户的选择有效
                        break # 跳出循环
                    print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环
                    
                if update_choose == "1": # 立即更新
                    update_link = eval (update.text) ["data"] ["link"]
                    update_filename = eval (update.text) ["data"] ["filename"]
                    # 下载文件代码（开始）
                    with closing (requests.get (update_link,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}, stream = True)) as update_file:
                        chunk_size = 1024 # 单次请求最大值
                        content_size = int (update_file.headers ["content-length"]) # 下载文件总大小（用int()来格式化为整数）
                        data_count = 0
                        with open (".\\" + update_filename, "wb") as file:
                            for data in update_file.iter_content (chunk_size = chunk_size):
                                file.write (data)
                                data_count = data_count + len (data) # 已下载的数据大小
                                progress = (data_count / content_size) * 100
                                print ("\r正在下载新版文件……%.2f%% (%.2f MB/%.2f MB)" % (progress, data_count / 1024 / 1024, content_size / 1024 / 1024), end = "") # 动态输出下载状态（单位：MB，保留2位小数）
                    # 下载文件代码（结束）
                    print ()
                    print ("更新完成，更新后的程序路径：" + os.getcwd () + "\\" + update_filename)
                    print ("正在载入新版程序...")
                    print ()
                    os.system ('"' + os.getcwd () + "\\" + update_filename + '"') # 打开新版程序
                    sys.exit () # 关闭本程序
                
                else: # 跳过更新
                    print ()
                    check ()
            
            else: # 版本相同
                check ()
        
        else: # 程序不能正常使用
            print (update_message)
            print ()
            print ("按任意键关闭本程序！")
            os.system ("pause >nul")
            sys.exit () # 关闭本程序
    
    else: # 无法连接到服务器
        print ("\033[1;37m访问更新服务器时异常\033[0m，程序可能无法及时获取更新！") # 彩色文字：白色，代号37
        check ()

def fix (): # 异常修复
    print ()
    print ("\033[1;37m程序的配置损坏\033[0m，这通常是因为程序意外关闭导致的！") # 彩色文字：白色，代号37
    print ("请重新填写数据（填写好的数据将会被记录，以方便下次使用）")
    print ()
    if os.path.exists (appdata + "\\biliautotaskdata.txt"): # 如果配置存在
        os.remove (appdata + "\\biliautotaskdata.txt") # 删除配置文件
    
    settings () # 跳转到设置
        
def check (): # 检查配置文件是否存在
    if (os.path.exists (appdata + "\\biliautotaskdata.txt")): # 配置文件存在
        print ("是否使用上次的配置？")
        
        while True: # 一直循环
            c = input ("输入1立即使用上次的配置，输入2则重新配置 [1/2] ")
            if c == "1" or c == "2": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环
        
        if c == "1": # 使用上次的配置
            main () # 跳转到主程序
            
        else: # 重新配置
            if os.path.exists (appdata + "\\biliautotaskdata.txt"): # 如果配置存在
                os.remove (appdata + "\\biliautotaskdata.txt") # 删除配置文件
            
            print () # 输出空行
            print ("请填写数据（填写好的数据将会被记录，以方便下次使用）")
            settings () # 跳转到设置
        
    else: # 配置文件不存在
        print ("检测到第一次使用该程序，请先填写数据（填写好的数据将会被记录，以方便下次使用）")
        settings ()
        
def settings (): # 设置
    coin = ""
    
    print ("请选择要自动执行的操作：1、登录+观看视频（5+5=10经验）  2、投币（每投一枚硬币增加10经验，最多50经验）  3、分享（5经验）")
    choose = input ("直接输入序号，如123，请填写：")
    
    if "2" in choose: # 用户选择了投币
        while True: # 一直循环
            print ()
            coin = input ("每天投几个币？（填大于等于1，小于等于5的整数）")
            if coin == "1" or coin == "2" or coin == "3" or coin == "4" or coin == "5": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入大于等于1，小于等于5的整数！") # 提示用户的选择无效，并再次循环
    
    with open (appdata + "\\biliautotaskdata.txt", "wt") as file:
        file.write (coin + "\n" + choose + "\n")
    Cookie () # 输入Cookie

def Cookie (): # 输入Cookie
    print ()
    SESSDATA = input ("请输入SESSDATA的值：")
    bili_jct = input ("请输入bili_jct的值：")
    with open (appdata + "\\biliautotaskdata.txt", "at") as file:
        file.write (SESSDATA + "\n" + bili_jct)
    main () # 跳转到主程序

def main (): # 主程序
    with open (appdata + "\\biliautotaskdata.txt", "rt") as x:
        line = x.read ().splitlines () # 读取内容，并分割每行
        
    try: # 异常调试
        coin = line [0] # 读取第1行内容：投币数
        choose = line [1] # 读取第2行内容：选择
        SESSDATA = line [2] # 读取第3行内容：Cookie（SESSDATA）
        bili_jct = line [3] # 读取第4行内容：Cookie（bili_jct）
        
    except: # 如果读取配置文件异常，执行except内的操作
        fix ()
        return
    
    headers = {"Cookie": "SESSDATA=" + SESSDATA + "; bili_jct=" + bili_jct, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}
    
    # 获取API返回值（验证Cookie是否失效）  
    result = requests.get ("https://api.bilibili.com/x/web-interface/nav", headers = headers).text # 获取当前用户登录信息
    code = eval (result) ["code"] # 获取命令行返回值，并改变编码为“utf-8”，转换类型为“词典”，并获取API的返回值
    
    if code != 0: # 账号未登录（-101），请求错误（-400），或者是其他原因导致的失败
        print ("\033[1;37m请正确填写有效的Cookie！\033[0m") # 彩色文字：白色，代号37
        with open (appdata + "\\biliautotaskdata.txt", "wt") as file: # 重新创建配置文件
            file.write (coin + "\n" + choose + "\n") # 写入数据：用户已提交的投币数和选择
            
        Cookie () # 重新输入Cookie
        return
        
    start = time.time () # 开始计时
    print ()
    
    # 判断程序后续将投币或转发等操作执行到哪些视频（如果历史记录存在视频，使用历史记录中的视频，并使用视频排行榜中的视频）
    vid = []
    result = requests.get ("https://api.bilibili.com/x/web-interface/history/cursor", headers = headers).text # 获取视频历史记录
    for history in eval (result) ["data"] ["list"]: # 根据历史记录中的视频来循环
        if history ["history"] ["business"] == "archive": # 如果这一条记录是视频（不是视频将无法投币）
            vid.append (str (history ["history"] ["oid"])) # 获取这个视频的av号，并添加进数组
    
    result = requests.get ("https://api.bilibili.com/x/web-interface/ranking").text # 获取视频排行榜中的视频
    for hot in eval (result) ["data"] ["list"]: # 根据视频排行榜中的视频来循环
        vid.append (str (hot ["aid"])) # 获取这些视频的av号，并添加进数组
    
    video = []
    for avnumber in vid: # 对所有视频进行去重并判断视频的有效性
        if avnumber not in video: # 如果新列表中没有这个视频，就要添加视频
            result = requests.get ("https://api.bilibili.com/x/web-interface/archive/stat?aid=" + avnumber, headers = headers).text # 获取视频的状态数
            if eval (result) ["code"] == 0: # 获取成功
                video.append (avnumber) # 添加有效视频
    
    if video == []: # 没有有效的视频可用
        print ("\033[1;37m没有找到有效的视频，无法完成任务！请开启历史记录并多看几个视频！\033[0m") # 彩色文字：白色，代号37
        os.system ("pause >nul") # 防止程序运行结束后窗口自动关闭
        sys.exit ()
    
    if "1" in choose: # 用户的选择中是否有“1”（登录+观看视频）
        print ("正在完成任务：登录+观看视频（5+5=10经验）……")
        result = requests.post ("https://api.bilibili.com/x/click-interface/web/heartbeat", headers = headers, data = {"aid": video [0]}).text # 告诉B站：用户“点击”了一个视频
    
    if "2" in choose: # 用户的选择中是否有“2”（投币）
        print ("正在完成任务：投币（每投一枚硬币增加10经验，最多50经验）……")
        need_coin = int (coin) # 需要投的硬币数
        for coin_video in video: # 根据可以投币的视频的数量来循环
            result = requests.get ("https://api.bilibili.com/x/web-interface/view?aid=" + coin_video, headers = headers).text # 获取视频的信息
            if eval (result) ["data"] ["copyright"] == 1: # 视频为自制（1）
                can_coin = 2 # 这个视频可以投2个币
            else: # 视频为转载（2）或者其他类型
                can_coin = 1 # 这个视频可以投1个币
            
            result = requests.get ("https://api.bilibili.com/x/web-interface/archive/coins?aid=" + coin_video, headers = headers).text # 获取当前用户为这个视频投的硬币数
            already_coin = eval (result)  ["data"]  ["multiply"] # 用户已经为这个视频投币的数量
            if already_coin < can_coin: # 用户为这个视频投的硬币数小于这个视频可以投的硬币数，就可以继续操作；否则，会提示投的硬币数超过上限
                can_coin -= already_coin # 这个视频可以投的硬币数减去用户已经为这个视频的投币数
                coin_count = 0
                
                if can_coin <= 0: # 这个视频不能投币
                    continue # 到循环尾
                if need_coin >= 2: # 需要投的硬币数大于等于2
                    coin_count = can_coin # 给这个视频的投币数就是这个视频可以投币的数量
                elif need_coin == 1: # 需要投的硬币数等于1
                    coin_count = 1 # 给这个视频的投币数为1
                
                none = requests.post ("https://api.bilibili.com/x/web-interface/coin/add", headers = headers, data = {"aid": coin_video, "multiply": str (coin_count), "csrf": bili_jct}).text # 给视频投币，设置变量"none"防止打印返回数据
                need_coin -= coin_count # 需要投币的数量减去已经给这个视频投币的数量
                if need_coin <= 0: # 如果需要投币的数量已经小于等于0
                    break # 跳出循环
    
    if "3" in choose: # 用户的选择中是否有“3”（分享）
        print ("正在完成任务：分享（5经验）……")
        none = requests.post ("https://api.bilibili.com/x/web-interface/share/add", headers = headers, data = {"aid": video [0], "csrf": bili_jct}).text # “分享”视频，实际上没有分享，只是告诉B站用户已经分享了视频  # 设置变量"none"来防止打印返回数据
    
    end = time.time () # 结束计时
    
    # 查询任务完成状态
    while True: # 一直循环
        result = requests.get ("https://api.bilibili.com/x/member/web/exp/reward", headers = headers).text # 获取用户的任务完成状态
        data = eval (result) ["data"]
        result_coin = requests.get ("https://api.bilibili.com/x/web-interface/coin/today/exp", headers = headers).text # 获取用户给视频投了多少枚硬币
        
        if data ["login"]: # 是否已登录
            login = "\033[1;36m已完成\033[0m（\033[1;36m5\033[0m经验）" # 彩色文字：青蓝色，代号36
        else:
            login = "\033[1;37m未完成\033[0m（\033[1;37m0\033[0m经验）" # 彩色文字：白色，代号37
        
        if data ["watch"]: # 是否已观看视频
            watch = "\033[1;36m已完成\033[0m（\033[1;36m5\033[0m经验）" # 彩色文字：青蓝色，代号36
        else:
            watch = "\033[1;37m未完成\033[0m（\033[1;37m0\033[0m经验）" # 彩色文字：白色，代号37
        
        if data ["share"]: # 是否已分享视频
            share = "\033[1;36m已完成\033[0m（\033[1;36m5\033[0m经验）" # 彩色文字：青蓝色，代号36
        else:
            share = "\033[1;37m未完成\033[0m（\033[1;37m0\033[0m经验）" # 彩色文字：白色，代号37
        
        if ("1" in choose and "已完成" in (login and watch)) or (not "1" in choose): # (1)变量choose包含“1”并且变量login和变量watch都包含“已完成”  (2)变量choose不包含“1”【当满足(1)或(2)时执行if内的操作】
            if ("2" in choose and int (eval (result_coin) ["data"]) / 10 >= int (coin)) or (not "2" in choose): # (1)变量choose包含“2”并且当前已投币数大于等于用户设定投币数    (2)变量choose不包含“2”【当满足(1)或(2)时执行if内的操作】
                if ("3" in choose and "已完成" in share) or (not "3" in choose): # (1)变量choose包含“3”并且变量share包含“已完成”    (2)变量choose不包含“3”【当满足(1)或(2)时执行if内的操作】
                    break # 跳出循环
        
        print ("\r登录：" + login + "，观看视频：" + watch + "，分享：" + share + "，投币：\033[1;36m" + str (int (int (eval (result_coin) ["data"]) / 10)) + "\033[0m个（\033[1;36m" + str (eval (result_coin) ["data"]) + "\033[0m经验）", end = "") # 将光标移到本行首位，覆盖原有输出（同行内动态输出任务完成状态）
        time.sleep (0.5) # 等待0.5秒
    
    print ("\r登录：" + login + "，观看视频：" + watch + "，分享：" + share + "，投币：\033[1;36m" + str (int (int (eval (result_coin) ["data"]) / 10)) + "\033[0m个（\033[1;36m" + str (eval (result_coin) ["data"]) + "\033[0m经验）", end = "") # 将光标移到本行首位，覆盖原有输出（同行内动态输出任务完成状态）
    print ("\n\n完成任务共用时：\033[1;33m" + str (round (end - start, 2)) + "秒\033[0m") # 彩色文字：黄色，代号33
    os.system ("pause >nul") # 防止程序运行结束后窗口自动关闭
    sys.exit () # 关闭本程序

# 程序开始运行时，运行以下代码
while True: # 一直循环
    if isConnected () == true: # 网络是否连接正常
        update ()
    else:
        print ("\033[1;37m无法连接到互联网，这会使任务无法完成！请检查网络是否正常！\033[0m（按Enter键重试）") # 彩色文字：白色，代号37
        os.system ("pause >nul")
