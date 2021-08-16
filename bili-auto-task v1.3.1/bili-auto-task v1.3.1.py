# 哔哩哔哩自动完成任务 V1.3.1
# 本程序可以帮你自动完成B站可获取经验值的任务，让你快速涨经验值、升级！
# 作者：B站用户“开心的肥宅快乐水”（https://space.bilibili.com/324042405）（编写代码主体）、B站用户“wuziqian211”（https://space.bilibili.com/425503913）（修改错误、完善代码、增加新功能）
# 2020年9月26日 由“开心的肥宅快乐水”编写批处理版本
# 2020年9月28日 由“开心的肥宅快乐水”重写python版本
# 2020年10月6日 由“wuziqian211”修改python版本
# 2020年10月10日 本程序主体功能已完善
# 2020年1月12日 由“开心的肥宅快乐水”优化python版本

import os
import requests
import time
from contextlib import closing

version = "1.3.1" # 版本号
appdata = os.getenv ("APPDATA") # 获取环境变量APPDATA的值
true = True
false = False
null = None

def check (): # 检查配置文件是否存在
    if (os.path.exists (appdata + "\\biliautotaskdata.txt")): # 配置存在
        print ("是否使用上次的配置？")
        
        while True: # 一直循环
            c = input ("输入1立即使用上次的配置，输入2则重新配置 [1/2] ")
            if c == "1" or c == "2": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入数字：1或2！") # 提示用户的选择无效，并再次循环
        
        if c == "1": # 使用上次的配置
            main () # 跳转到主程序
            
        elif c == "2": # 重新配置
            if os.path.exists (appdata + "\\biliautotaskdata.txt"): # 如果配置存在
                os.remove (appdata + "\\biliautotaskdata.txt") # 删除配置
            else: # 如果配置不存在
                print ("位于“" + appdata + "\\biliautotaskdata.txt”的配置文件已被用户删除")
            
            print () # 输出空行
            print ("请填写数据（填写好的数据将会被记录，以方便下次使用）")
            settings () # 跳转到设置
        
    else: # 配置不存在
        print ("检测到第一次使用该程序，请先填写数据（填写好的数据将会被记录，以方便下次使用）")
        settings ()
        
def settings (): # 设置
    coin = ""
    
    print ("请选择要自动执行的操作：1、登录+观看视频（5+5=10经验）  2、投币（每投一枚硬币增加10经验，最多50经验）  3、分享（5经验）")
    choose = input ("直接输入序号，如123，请填写：")
    
    if "2" in choose: # 用户是否选择了投币
        while True: # 一直循环
            print ()
            coin = input ("每天投几个币？（填大于等于1，小于等于5的整数）")
            if coin == "1" or coin == "2" or coin == "3" or coin == "4" or coin == "5": # 用户的选择有效
                break # 跳出循环
            
            print ("请输入大于等于1，小于等于5的整数！") # 提示用户的选择无效，并再次循环
    
    with open (appdata + "\\biliautotaskdata.txt", "at") as file:
        file.write (coin + "\n" + choose + "\n")
    Cookie ()

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
        
        coin = line [0] # 读取第1行内容：投币数
        choose = line [1] # 读取第2行内容：选择
        SESSDATA = line [2] # 读取第3行内容：Cookie（SESSDATA）
        bili_jct = line [3] # 读取第4行内容：Cookie（bili_jct）
        
    headers = {'Cookie':'SESSDATA=' + SESSDATA + '; bili_jct=' + bili_jct + '','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
    
    # 获取API返回值（验证Cookie是否失效）  
    result = requests.get ('https://api.bilibili.com/x/web-interface/nav',headers=headers).text # 获取当前用户登录信息
    code = eval (result).get ("code") # 获取命令行返回值，并改变编码为“utf-8”，转换类型为“词典”，并获取API的返回值
    
    if code != 0: # 账号未登录（-101），请求错误（-400），或者是其他原因导致的失败
        print ("请正确填写有效的Cookie！")
        if os.path.exists (appdata + "\\biliautotaskdata.txt"): # 如果配置存在
            os.remove (appdata + "\\biliautotaskdata.txt") # 删除配置
            with open (appdata + "\\biliautotaskdata.txt", "at") as file: # 重新创建配置文件
                file.write (coin + "\n" + choose + "\n") # 写入数据：用户已提交的投币数和选择
        else: # 如果配置不存在
            with open (appdata + "\\biliautotaskdata.txt", "at") as file: # 重新创建配置文件
                file.write (coin + "\n" + choose + "\n") # 写入数据：用户已提交的投币数和选择
            
        Cookie () # 重新输入Cookie
        return
        
    start = time.time() # 开始计时
    print()
    
    # 判断程序后续将投币或转发等操作执行到哪些视频（如果历史记录存在视频，使用历史记录中的视频，并使用视频排行榜中的视频）
    video = []
    result = requests.get ('https://api.bilibili.com/x/web-interface/history/cursor',headers=headers).text # 获取视频历史记录
    for history in eval (result).get ("data").get ("list"): # 根据历史记录中的视频来循环
        if history.get ("history").get ("business") == "archive": # 如果这一条记录是视频（不是视频将无法投币）
            video.append (str (history.get ("history").get ("oid"))) # 获取这个视频的av号，并添加进数组
    
    result = requests.get ('https://api.bilibili.com/x/web-interface/ranking').text # 获取视频排行榜中的视频
    for hot in eval (result).get ("data").get ("list"): # 根据视频排行榜中的视频来循环
        video.append (str (hot.get ("aid"))) # 获取这些视频的av号，并添加进数组

    if video == []: # 没有有效的视频可用
        print ("无法找到有效的视频，无法完成任务！")
        return
    
    if "1" in choose: # 用户的选择中是否有“1”（登录+观看视频）
        print ("正在完成任务：登录+观看视频（5+5=10经验）……")
        result = requests.post ('https://api.bilibili.com/x/click-interface/web/heartbeat',headers=headers,data={'aid':'' + video [0] + ''}).text # 告诉B站：用户“点击”了一个视频
    
    if "2" in choose: # 用户的选择中是否有“2”（投币）
        print ("正在完成任务：投币（每投一枚硬币增加10经验，最多50经验）……")
        need_coin = int (coin) # 需要投的硬币数
        for coin_video in video: # 根据可以投币的视频的数量来循环
            result = requests.get ('https://api.bilibili.com/x/web-interface/view?aid=' + coin_video + '').text # 获取视频的信息
            if eval (result).get ("data").get ("copyright") == 1: # 视频为自制（1）
                can_coin = 2 # 这个视频可以投2个币
            else: # 视频为转载（2）或者其他类型
                can_coin = 1 # 这个视频可以投1个币
            
            result = requests.get ('https://api.bilibili.com/x/web-interface/archive/coins?aid=' + coin_video + '',headers=headers).text # 获取当前用户为这个视频投的硬币数
            already_coin = eval (result).get ("data").get ("multiply") # 用户已经为这个视频投币的数量
            if already_coin < can_coin: # 用户为这个视频投的硬币数小于这个视频可以投的硬币数，就可以继续操作；否则，会提示投的硬币数超过上限
                can_coin -= already_coin # 这个视频可以投的硬币数减去用户已经为这个视频的投币数
                coin_count = 0
                
                if can_coin <= 0: # 这个视频不能投币
                    continue # 到循环尾
                if need_coin >= 2: # 需要投的硬币数大于等于2
                    coin_count = can_coin # 给这个视频的投币数就是这个视频可以投币的数量
                elif need_coin == 1: # 需要投的硬币数等于1
                    coin_count = 1 # 给这个视频的投币数为1
                
                none = requests.post ('https://api.bilibili.com/x/web-interface/coin/add',headers=headers,data={'aid':'' + coin_video + '','multiply':'' + str (coin_count) +'','csrf':'' + bili_jct +''}).text # 给视频投币，设置变量"none"防止打印返回数据  # 设置变量"none"来防止打印返回数据
                need_coin -= coin_count # 需要投币的数量减去已经给这个视频投币的数量
                if need_coin <= 0: # 如果需要投币的数量已经小于等于0
                    break # 跳出循环
    
    if "3" in choose: # 用户的选择中是否有“3”（分享）
        print ("正在完成任务：分享（5经验）……")
        none = requests.post ('https://api.bilibili.com/x/web-interface/share/add',headers=headers,data={'aid':'' + video [0] + '','csrf':'' + bili_jct + ''}).text # “分享”视频，实际上没有分享，只是告诉B站用户已经分享了视频  # 设置变量"none"来防止打印返回数据
    
    end = time.time() # 结束计时
    
    # 查询任务完成状态
    result = requests.get ('https://api.bilibili.com/x/member/web/exp/reward',headers=headers).text # 获取用户的任务完成状态
    
    data = eval (result).get ("data")
    
    if data.get ("login"): # 是否已登录
        login = "已完成（5经验）"
    else:
        login = "未完成"
    
    if data.get ("watch"): # 是否已观看视频
        watch = "已完成（5经验）"
    else:
        watch = "未完成"
    
    if data.get ("share"): # 是否已分享视频
        share = "已完成（5经验）"
    else:
        share = "未完成"
    
    result = requests.get ('https://api.bilibili.com/x/web-interface/coin/today/exp',headers=headers).text # 获取用户给视频投了多少枚硬币
    
    print ("登录：" + login + "，观看视频：" + watch + "，分享：" + share + "，投币：" + str (eval (result).get ("data")) + "经验") # 输出
    print ()
    print ("完成任务共用时："+str(round(end-start, 2))+"秒")
    os.system('pause >nul') # 防止程序运行结束后窗口自动关闭

# 程序开始运行时，运行以下代码
# 检查更新
update = requests.get ('https://happycola.gitee.io/bili-auto-task-update/index.json') # 从更新服务器获取数据
if str(update.status_code) == "200": # 判断服务器响应状态码是否正常
    update_message = eval(update.text).get("message")
    if update_message == "ok": # 判断该程序还能正常使用（如果变量update_message的值不等于“ok”，则代表该程序因特殊原因被作者停止使用）
        update_version = eval(update.text).get("data").get("version")
        if update_version != version:
            print ("检测到新版本：v" + update_version + "（当前版本：v" + version + "）")
            update_content = eval(update.text).get("data").get("content")
            print (update_content)
            print ()
            print ("是否更新？")
            update_choose = input("输入1立即更新，输入2则跳过更新 [1/2] ")
            if update_choose == "1":
                update_link = eval(update.text).get("data").get("link")
                update_filename = eval(update.text).get("data").get("filename")
                # 下载文件代码（开始）
                with closing(requests.get(update_link,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'},stream=True)) as update_file:
                    chunk_size = 1024 # 单次请求最大值
                    content_size = int(update_file.headers['content-length'])  # 下载文件总大小（用int()来格式化为整数）
                    data_count = 0
                    with open(".\\" + update_filename, "wb") as file:
                        for data in update_file.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            data_count = data_count + len(data) # 已下载的数据大小
                            progress = (data_count / content_size) * 100
                            print("\rDownloading：%.2f%% (%.2f MB/%.2f MB)" % (progress, data_count/1024/1024, content_size/1024/1024), end="") # 动态输出下载状态
                #下载文件代码（结束）
                print ()
                print ("更新完成，更新后的程序路径：" + os.getcwd() + "\\" + update_filename)
                print ("正在载入新版程序...")
                print ()
                os.system('"' + os.getcwd() + '\\' + update_filename + '"')
                os.system('pause >nul') # 防止程序运行结束后窗口自动关闭
            else:
                check ()
             
        else:
            check ()
     
    else:
        print (update_message)
        print ()
        print ("按任意键关闭本程序！")
        os.system('pause >nul')
        os.system('exit') # 按任意键后关闭本程序
     
else:
    print ("访问更新服务器时异常，程序可能无法及时更新！")
    check ()