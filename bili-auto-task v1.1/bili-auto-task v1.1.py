import os
import sys
import subprocess
import goto
from dominate.tags import label
from goto import with_goto#调用goto

appdata = os.getenv('APPDATA')
appdata = appdata.replace('\\','/')
if (os.path.exists(appdata+"/biliautotaskdata.txt")):
    print("是否使用上次的配置？")
    label .creturn#设置跳转点：creturn
    c=input("输入1立即使用上次的配置，输入2则重新配置 [1/2]")
    if c!=1:
        if c!=2:
            print("请输入数字：1或2")
            goto .creturn#跳转至creturn
    if c==1:
        label .start
        with open(appdata+"/biliautotaskdata.txt",'r') as x:
            line = x.readlines()
            coin = line[0]#读取第1行内容：投币数
            choose = line[1]#读取第2行内容：选择
            SESSDATA = line[2]#读取第3行内容：cookie（SESSDATA）
            bili_jct = line[3]#读取第4行内容：cookie（bili_jct）

        #获取curl返回值（验证cookie是否失效）
        result = subprocess.Popen('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'"-d "https://api.bilibili.com/x/member/web/exp/reward" -s',shell=True,stdout=subprocess.PIPE)
        res = result.communicate()  
        for check in res.splitlines():#将check设置为cookie失效检测返回值
            check = eval(check.decode('utf-8'))#转换变量“check”的编码为“utf-8”,转换类型为“词典”
            check = check.get("message")
        if check=="请求错误":
            print("cookie已失效，请重新填写cookie")
            print()
            goto .return2#跳转至return2
        elif check=="账号未登录":
            print("请正确填写cookie")
            print()
            goto .return2#跳转至return2

        result = subprocess.Popen('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'"-d "http://api.bilibili.com/x/web-interface/history/cursor" -s',shell=True,stdout=subprocess.PIPE)
        res = result.communicate()  
        for temp in res.splitlines():
            temp = eval(data.decode('utf-8'))
        video = temp.get("data")
        video = video.get("cursor")
        video = video.get("max")
        
        #判断程序后续将（投币或转发等操作）执行到哪个视频（如果历史记录存在视频，使用历史记录中最新的视频；如果历史记录不存在视频，使用视频排行榜中的视频）
        if video==0:
            result = subprocess.Popen('curl http://api.bilibili.com/x/web-interface/ranking -s',shell=True,stdout=subprocess.PIPE)
            res = result.communicate()  
            for temp in res.splitlines():
                temp = eval(temp.decode('utf-8'))
                video = temp.get("data")
                video = video.get("list")
                video = str(video)
                video = eval(video[1:-1])
                video = video[0].get("aid")
        else:
            video = temp.get("data")
            video = video.get("list")
            video = str(video)
            video = eval(video[1:-1])
            video = video.get("history")
            video = video.get("oid")


        temp1 = '1' in choose
        temp2 = '2' in choose
        temp3 = '3' in choose
        if temp1==True:
            os.system('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'" "https://api.bilibili.com/x/click-interface/web/heartbeat" -s')  
        if temp2==True:
            os.system('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'" -d "aid=!video!&multiply=!coin!&cross_domain=true" "https://api.bilibili.com/x/web-interface/coin/add" -s')
        if temp3==True:
            result = subprocess.Popen('curl https://api.bilibili.com/x/web-interface/view?aid=!video! -s',shell=True,stdout=subprocess.PIPE)
            res = result.communicate()  
            for temp in res.splitlines():
                true=True
                false=False
                data = eval(temp.decode('utf-8'))
                uid = data.get("data")
                uid = uid.get("owner")
                uid = uid.get("mid")
                result = subprocess.Popen('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'"-d "csrf_token='+bili_jct+'!&platform=pc&uid='+uid+'&type=8&content=temp&repost_code=20000&rid='+video+' "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share" -s',shell=True,stdout=subprocess.PIPE)
                res = result.communicate()  
            for temp in res.splitlines():
                true=True
                false=False
                data=eval(temp.decode('utf-8'))
                id = data.get("data")
                id = id.get("dynamic_id_str")
            os.system('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'" -d "dynamic_id='+id+'&csrf_token='+bili_jct+'&csrf='+bili_jct+'" "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic" -s')

        #查询任务完成状态
        result = subprocess.Popen('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'"-d "https://api.bilibili.com/x/member/web/exp/reward" -s',shell=True,stdout=subprocess.PIPE)
        res = result.communicate()  
        for temp in res.splitlines():
            true=True
            false=False
            data=eval(temp.decode('utf-8'))
            data = data.get("data")
            login = data.get("login")
            watch = data.get("watch")
            share = data.get("share")
        result1 = "登录："+login+",观看视频："+watch+",分享："+share
        result = subprocess.Popen('curl -b "SESSDATA='+SESSDATA+';bili_jct='+bili_jct+'"-d "https://api.bilibili.com/x/web-interface/coin/today/exp" -s',shell=True,stdout=subprocess.PIPE)
        res = result.communicate()  
        for temp in res.splitlines():
            data=eval(temp.decode('utf-8'))
            data = data.get("data")
        result2 = ",投币："+data
        print (result1+result2)
    elif c==2:
        if os.path.exists(appdata+"/biliautotaskdata.txt"):#如果文件存在
            os.remove(appdata+"/biliautotaskdata.txt")
        else:#如果文件不存在
            print("位于“"+appdata+"/biliautotaskdata.txt”的配置文件已被用户删除")
        print()
        print("请填写数据（填写好的数据将会被记录，以方便下次使用）")
        goto .return1#跳转至return1
if not (os.path.exists(appdata+"/biliautotaskdata.txt")):
    print("检测到第一次使用该程序，请先填写数据（填写好的数据将会被记录，以方便下次使用）")
    label .return1#设置跳转点：return1
    print("请选择要自动执行的操作：1、登录+观看视频（5+5经验）  2、投币（0/50经验）  3、分享（5经验）")
    choose=input("直接输入序号，如123，请填写：")
    print()
    label .return3#设置跳转点：return3
    coin = 0
    temp = '1' in choose
    if temp==True:
        temp = '2' in choose
        coin=input("每天投几个币？(填:1或2)")
        if temp==True:
            print("请输入小于等于2的正整数")
            print()
            goto .return3
            with open(appdata+"/biliautotaskdata.txt","a") as file:
                f.write(coin+'\r\n')
            label .return2#设置跳转点：return2
            SESSDATA=input("请输入SESSDATA值：")
            bili_jct=input("请输入bili_jct：")
            with open(appdata+"/biliautotaskdata.txt","a") as file:
                f.write(choose+'\r\n'+SESSDATA+'\r\n'+bili_jct)
            goto .start#跳转至start
