@echo off

echo EasyNote��ݹ���
echo -------------------------------
echo ��ѡ�����
echo 1. ��ջ���
echo 2. �����־
echo 3. �༭����
echo 4. �˳�
echo -------------------------------

:choose
set /p oper=ѡ�������

if "%oper%"=="1" (
    del .\cache
    echo ���������
    goto choose
)
if "%oper%"=="2" (
    del .\logs
    echo ��־��ɾ��
    goto choose
)
if "%oper%"=="3" (
    echo ���ڴ�settings.json
    start settings.json
    goto choose
)
if "%oper%"=="4" (
    exit
)
echo �Ƿ����
goto choose