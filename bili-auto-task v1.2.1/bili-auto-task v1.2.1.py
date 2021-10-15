# 哔哩哔哩自动完成任务 V1.2.1
# 本程序可以帮你自动完成B站可获取经验值的任务，让你快速涨经验值、升级！
# 作者：B站用户“肥宅水水呀”（https://space.bilibili.com/324042405）（编写代码主体）、B站用户“wuziqian211”（https://space.bilibili.com/425503913）（修改错误、完善代码、增加新功能）
# 2020年9月26日 由“肥宅水水呀”编写批处理版本
# 2020年9月28日 由“肥宅水水呀”重写python版本
# 2020年10月6日 由“wuziqian211”修改python版本
# 2020年10月10日 本程序主体功能已完善

import os
import subprocess

appdata = os.getenv ("APPDATA") # 获取环境变量APPDATA的值
true = True
false = False
null = None

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
    
    # 获取API返回值（验证Cookie是否失效）
    result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" "https://api.bilibili.com/x/web-interface/nav" -s', shell = True, stdout = subprocess.PIPE) # 获取当前用户登录信息
    code = eval (result.communicate () [0].decode ("utf-8")).get ("code") # 转换变量“check”的编码为“utf-8”，转换类型为“词典”，并获取API返回值
    
    if code != 0: # 账号未登录（-101），请求错误（-400），或者是其他原因导致的失败
        print ("请正确填写有效的Cookie！")
        Cookie () # 重新输入Cookie
        return
    # 判断程序后续将投币或转发等操作执行到哪些视频（如果历史记录存在视频，使用历史记录中的视频，并使用视频排行榜中的视频）
    
    video = []
    result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" "https://api.bilibili.com/x/web-interface/history/cursor" -s', shell = True, stdout = subprocess.PIPE) # 获取视频历史记录
    for history in eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("list"): # 根据历史记录中的视频来循环
        if history.get ("history").get ("business") == "archive": # 如果这一条记录是视频（不是视频将无法投币）
            video.append (str (history.get ("history").get ("oid"))) # 获取这个视频的av号，并添加进数组
    
    result = subprocess.Popen ('curl "https://api.bilibili.com/x/web-interface/ranking" -s', shell = True, stdout = subprocess.PIPE) # 获取视频排行榜中的视频
    for hot in eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("list"): # 根据视频排行榜中的视频来循环
        video.append (str (hot.get ("aid"))) # 获取这些视频的av号，并添加进数组

    if video == []: # 没有有效的视频可用
        print ("无法找到有效的视频，无法完成任务！")
        return
    
    if "1" in choose: # 用户的选择中是否有“1”（登录+观看视频）
        print ("正在完成任务：登录+观看视频（5+5=10经验）……")
        subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" -d "aid=' + video [0] + '" "https://api.bilibili.com/x/click-interface/web/heartbeat" -s', shell = True) # 告诉B站：用户“点击”了一个视频
    
    if "2" in choose: # 用户的选择中是否有“2”（投币）
        print ("正在完成任务：投币（每投一枚硬币增加10经验，最多50经验）……")
        need_coin = int (coin) # 需要投的硬币数
        for coin_video in video: # 根据可以投币的视频的数量来循环
            result = subprocess.Popen ('curl "https://api.bilibili.com/x/web-interface/view?aid=' + coin_video + '" -s', shell = True, stdout = subprocess.PIPE) # 获取视频的信息
            if eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("copyright") == 1: # 视频为自制（1）
                can_coin = 2 # 这个视频可以投2个币
            else: # 视频为转载（2）或者其他类型
                can_coin = 1 # 这个视频可以投1个币
            
            result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" "https://api.bilibili.com/x/web-interface/archive/coins?aid=' + coin_video + '" -s', shell = True, stdout = subprocess.PIPE) # 获取当前用户为这个视频投的硬币数
            already_coin = eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("multiply") # 用户已经为这个视频投币的数量
            if already_coin < can_coin: # 用户为这个视频投的硬币数小于这个视频可以投的硬币数，就可以继续操作；否则，会提示投的硬币数超过上限
                can_coin -= already_coin # 这个视频可以投的硬币数减去用户已经为这个视频的投币数
                
                if can_coin <= 0: # 这个视频不能投币
                    continue # 到循环尾
                if need_coin >= 2: # 需要投的硬币数大于等于2
                    coin_count = can_coin # 给这个视频的投币数就是这个视频可以投币的数量
                elif need_coin == 1: # 需要投的硬币数等于1
                    coin_count = 1 # 给这个视频的投币数为1
                
                subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" -d "aid=' + coin_video + '&multiply=' + str (coin_count) + '&csrf=' + bili_jct + '" "https://api.bilibili.com/x/web-interface/coin/add" -s', shell = True) # 给视频投币
                need_coin -= coin_count # 需要投币的数量减去已经给这个视频投币的数量
                if need_coin <= 0: # 如果需要投币的数量已经小于等于0
                    break # 跳出循环
    
    if "3" in choose: # 用户的选择中是否有“3”（分享）
        print ("正在完成任务：分享（5经验，会发布一条临时动态，任务完成后会自动删除这条动态）……")
        result = subprocess.Popen ('curl "https://api.bilibili.com/x/web-interface/view?aid=' + video [0] + '" -s', shell = True, stdout = subprocess.PIPE) # 获取视频的信息
        uid = str (eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("owner").get ("mid")) # 获取视频的UP主UID
        
        result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" -d "platform=pc&uid=' + uid + '&type=8&content=temp&repost_code=20000&rid=' + video [0] + '&csrf=' + bili_jct + '" "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share" -s', shell = True, stdout = subprocess.PIPE) # 把这个视频转发到动态，以告诉B站用户已经分享了视频
        id = eval (result.communicate () [0].decode ("utf-8")).get ("data").get ("dynamic_id_str") # 获取动态的ID
        
        subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct+'" -d "dynamic_id=' + id + '&csrf_token=' + bili_jct + '&csrf=' + bili_jct + '" "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic" -s', shell = True) # 删除这条动态，不然会留下一条多余的动态，毕竟这条动态不是用户自己发布的
    
    # 查询任务完成状态
    result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" "https://api.bilibili.com/x/member/web/exp/reward" -s', shell = True, stdout = subprocess.PIPE) # 获取用户的任务完成状态
    
    data = eval (result.communicate () [0].decode ("utf-8")).get ("data")
    
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
    
    result = subprocess.Popen ('curl -b "SESSDATA=' + SESSDATA + ';bili_jct=' + bili_jct + '" "https://api.bilibili.com/x/web-interface/coin/today/exp" -s', shell = True, stdout = subprocess.PIPE) # 获取用户给视频投了多少枚硬币
    
    print ("登录：" + login + "，观看视频：" + watch + "，分享：" + share + "，投币：" + str (eval (result.communicate () [0].decode ("utf-8")).get ("data")) + "经验") # 输出

# 程序开始运行时，运行以下代码
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
