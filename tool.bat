@echo off

echo EasyNote��ݹ���
echo -------------------------------
echo ��ѡ�����
echo 1. ��ջ���
echo 2. �����־
echo 3. �˳�
echo -------------------------------

:choose
set /p oper=ѡ�������

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
echo �Ƿ����
goto choose