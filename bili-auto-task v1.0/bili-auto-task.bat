@echo off
Setlocal EnableDelayedExpansion
del /s /f /q C:\Users\Public\Documents\biliautotasktemp.txt >nul 2>nul
if exist "%appdata%\biliautotaskdata.txt" (
    echo �Ƿ�ʹ���ϴε����ã�
    set /p c=����Y������ʹ���ϴε����ã�����N���������� [Y/N]:
    if /i "!c!"=="Y" (
	    :start
        for /f "delims=" %%a in (!appdata!\biliautotaskdata.txt) do (set /a q+=1 & if !q!==2 set "choose=%%a")
        for /f "delims=" %%b in (!appdata!\biliautotaskdata.txt) do (set /a r+=1 & if !r!==3 set "SESSDATA=%%b")
        for /f "delims=" %%c in (!appdata!\biliautotaskdata.txt) do (set /a s+=1 & if !s!==4 set "bili_jct=%%c")
        for /f %%d in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "https://api.bilibili.com/x/member/web/exp/reward" -s') do (set check=%%d)
        if "!check:�������=!" NEQ "!check!" (
            echo cookie��ʧЧ����������дcookie
            echo.
            goto return2
        )
        if "!check:�˺�δ��¼=!" NEQ "!check!" (
            echo ����ȷ��дcookie
            echo.
            goto return2
        )

        for /f %%e in ('curl -b "SESSDATA=!SESSDATA!;bili_jct=!bili_jct!"-d "http://api.bilibili.com/x/web-interface/history/cursor" -s') do (set data=%%e)
        if "!data!"=="{"code":0,"message":"0","ttl":1,"data":{"cursor":{"max":0,"view_at":0,"business":"","ps":0},"tab":[{"type":"archive","name":"��Ƶ"},{"type":"live","name":"ֱ��"},{"type":"article","name":"ר��"}],"list":[]}}" (
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
        echo ����д���ݣ���д�õ����ݽ��ᱻ��¼���Է����´�ʹ�ã�
        goto return1
    )
)


if not exist %appdata%\biliautotaskdata.txt (
    echo ��⵽��һ��ʹ�øó���������д���ݣ���д�õ����ݽ��ᱻ��¼���Է����´�ʹ�ã�
    :return1
    echo ��ѡ��Ҫ�Զ�ִ�еĲ�����1����¼+�ۿ���Ƶ��5+5���飩  2��Ͷ�ң�0/50���飩  3������5���飩
    set /p choose=ֱ��������ţ���123������д��
    echo.
    :return3
	set coin=0
    if "!choose:2=!" NEQ "!choose!" (
        set /p coin=ÿ��Ͷ�����ң�(��:1��2��:
        if "!coin!" NEQ "1" (
            if "!coin!" NEQ "2" (
                echo ������С�ڵ���2��������
                echo.
                goto return3
            )
        )
    )
    echo !coin!>>!appdata!\biliautotaskdata.txt
    :return2
    set /p SESSDATA=������SESSDATAֵ��
    set /p bili_jct=������bili_jct��
    echo !choose!>>!appdata!\biliautotaskdata.txt
    echo !SESSDATA!>>!appdata!\biliautotaskdata.txt
    echo !bili_jct!>>!appdata!\biliautotaskdata.txt
    goto start
)