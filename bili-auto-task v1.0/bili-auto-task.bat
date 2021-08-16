@echo off
Setlocal EnableDelayedExpansion
del /s /f /q C:\Users\Public\Documents\biliautotasktemp.txt >nul 2>nul
if exist "%appdata%\biliautotaskdata.txt" (
    echo 是否使用上次的配置？
    set /p c=输入Y则立即使用上次的配置，输入N则重新配置 [Y/N]:
    if /i "!c!"=="Y" (
	    :start
        for /f "delims=" %%a in (!appdata!\biliautotaskdata.txt) do (set /a q+=1 & if !q!==2 set "choose=%%a")
        for /f "delims=" %%b in (!appdata!\biliautotaskdata.txt) do (set /a r+=1 & if !r!==3 set "SESSDATA=%%b")
        for /f "delims=" %%c in (!appdata!\biliautotaskdata.txt) do (set /a s+=1 & if !s!==4 set "bili_jct=%%c")
        for /f %%d in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "https://api.bilibili.com/x/member/web/exp/reward" -s') do (set check=%%d)
        if "!check:请求错误=!" NEQ "!check!" (
            echo cookie已失效，请重新填写cookie
            echo.
            goto return2
        )
        if "!check:账号未登录=!" NEQ "!check!" (
            echo 请正确填写cookie
            echo.
            goto return2
        )

        for /f %%e in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "http://api.bilibili.com/x/web-interface/history/cursor" -s') do (set data=%%e)
        if "!data!"=="{"code":0,"message":"0","ttl":1,"data":{"cursor":{"max":0,"view_at":0,"business":"","ps":0},"tab":[{"type":"archive","name":"视频"},{"type":"live","name":"直播"},{"type":"article","name":"专栏"}],"list":[]}}" (
            for /f %%e in ('curl http://api.bilibili.com/x/web-interface/ranking -s') do (set data=%%e)
            echo 2!data!>C:\Users\Public\Documents\biliautotasktemp.txt
            for /f %%f in ('%~dp0helper.exe') do (set video=%%f)
        ) else (
            echo 1!data!>C:\Users\Public\Documents\biliautotasktemp.txt
            for /f %%f in ('%~dp0helper.exe') do (set video=%%f)
        )
        del /s /f /q C:\Users\Public\Documents\biliautotasktemp.txt >nul 2>nul

        if "!choose:1=!" NEQ "!choose!" (
	        curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!" -d "aid=!video!" "https://api.bilibili.com/x/click-interface/web/heartbeat" -s
	    )

        if "!choose:2=!" NEQ "!choose!" (
            for /f "delims=" %%g in (!appdata!\biliautotaskdata.txt) do (set /a p+=1 & if !p!==1 set "coin=%%g")
            curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!" -d "aid=!video!&multiply=!coin!&cross_domain=true" "https://api.bilibili.com/x/web-interface/coin/add" -s
        )

        if "!choose:3=!" NEQ "!choose!" (
            for /f %%h in ('curl https://api.bilibili.com/x/web-interface/view?aid=!video! -s') do (set data=%%h)
            echo 3!data!>C:\Users\Public\Documents\biliautotasktemp.txt
            for /f %%i in ('%~dp0helper.exe') do (set uid=%%i)
            curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!" -d "csrf_token=!bili_jct!&platform=pc&uid=!uid!&type=8&content=temp&repost_code=20000&rid=!video!" "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share" -s
            for /f %%j in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!" -d "csrf_token=!bili_jct!&platform=pc&uid=!uid!&type=8&content=temp&repost_code=20000&rid=!video!" "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/share" -s') do (set data=%%j)
            echo 4!data!>C:\Users\Public\Documents\biliautotasktemp.txt
            for /f %%k in ('%~dp0helper.exe') do (set id=%%k)
            curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!" -d "dynamic_id=!id!&csrf_token=!bili_jct!&csrf=!bili_jct!" "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic" -s
        )

        for /f %%l in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "https://api.bilibili.com/x/member/web/exp/reward" -s') do (set result=%%l)
        echo 5!result!>C:\Users\Public\Documents\biliautotasktemp.txt
        for /f %%m in ('%~dp0helper.exe') do (set result1=%%m)
        for /f %%n in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "https://api.bilibili.com/x/web-interface/coin/today/exp" -s') do (set result=%%n)
        echo 6!result!>C:\Users\Public\Documents\biliautotasktemp.txt
        for /f %%o in ('%~dp0helper.exe') do (set result2=%%o)
        echo !result1!!result2!
        pause>nul
        exit

    ) else (
        del /s /f /q "!appdata!\biliautotaskdata.txt" >nul 2>nul
		echo.
        echo 请填写数据（填写好的数据将会被记录，以方便下次使用）
        goto return1
    )
)


if not exist %appdata%\biliautotaskdata.txt (
    echo 检测到第一次使用该程序，请先填写数据（填写好的数据将会被记录，以方便下次使用）
    :return1
    echo 请选择要自动执行的操作：1、登录+观看视频（5+5经验）  2、投币（0/50经验）  3、分享（5经验）
    set /p choose=直接输入序号，如123，请填写：
    echo.
    :return3
	set coin=0
    if "!choose:2=!" NEQ "!choose!" (
        set /p coin=每天投几个币？(填:1或2）:
        if "!coin!" NEQ "1" (
            if "!coin!" NEQ "2" (
                echo 请输入小于等于2的正整数
                echo.
                goto return3
            )
        )
    )
    echo !coin!>>!appdata!\biliautotaskdata.txt
    :return2
    set /p SESSDATA=请输入SESSDATA值：
    set /p bili_jct=请输入bili_jct：
    echo !choose!>>!appdata!\biliautotaskdata.txt
    echo !SESSDATA!>>!appdata!\biliautotaskdata.txt
    echo !bili_jct!>>!appdata!\biliautotaskdata.txt
    goto start
)