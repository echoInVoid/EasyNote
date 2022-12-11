@echo off

echo EasyNote快捷工具
echo -------------------------------
echo 请选择操作
echo 1. 清空缓存
echo 2. 清空日志
echo 3. 编辑设置
echo 4. 退出
echo -------------------------------

:choose
set /p oper=选择操作：

if "%oper%"=="1" (
    del .\cache
    echo 缓存已清空
    goto choose
)
if "%oper%"=="2" (
    del .\logs
    echo 日志已删除
    goto choose
)
if "%oper%"=="3" (
    echo 正在打开settings.json
    start settings.json
    goto choose
)
if "%oper%"=="4" (
    exit
)
echo 非法命令！
goto choose