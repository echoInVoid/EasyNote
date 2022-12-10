@echo off

echo EasyNote快捷工具
echo -------------------------------
echo 请选择操作
echo 1. 清空缓存
echo 2. 清空日志
echo 3. 退出
echo -------------------------------

:choose
set /p oper=选择操作：

if "%oper%"=="1" (
    del .\cache
    goto choose
)
if "%oper%"=="2" (
    del .\logs
    goto choose
)
if "%oper%"=="3" (
    exit
)
echo 非法命令！
goto choose