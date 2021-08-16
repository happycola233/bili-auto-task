global null
null=''
f=open('C:\\Users\\Public\\Documents\\biliautotasktemp.txt',mode='r', encoding='UTF-8')
f=f.read()
a=int(f[0])
b=f[1:]

if a==1:    
    data=eval(b)
    video = data.get("data")
    video = video.get("list")
    video = str(video)
    video = eval(video[1:-1])
    video = video.get("history")
    video = video.get("oid")
    print(video)
    

elif a==2:
    data=eval(b)
    video = data.get("data")
    video = video.get("list")
    video = str(video)
    video = eval(video[1:-1])
    video = video[0].get("aid")
    print(video)


elif a==3:
    true=True
    false=False
    data=eval(b)
    mid = data.get("data")
    mid = mid.get("owner")
    mid = mid.get("mid")
    print(mid)


elif a==4:
    true=True
    false=False
    data=eval(b)
    id = data.get("data")
    id = id.get("dynamic_id_str")
    print(id)


elif a==5:
    true=True
    false=False
    data=eval(b)
    data = data.get("data")
    login = data.get("login")
    watch = data.get("watch")
    share = data.get("share")
    print("登录：",login,",观看视频：",watch,",分享：",share)


elif a==6:
    data=eval(b)
    data = data.get("data")
    print(",投币：",data)
