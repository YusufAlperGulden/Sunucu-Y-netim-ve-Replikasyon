@echo off
echo =======================================================
echo     Sunucu Yonetim ve Replikasyon - FastAPI
echo =======================================================
echo.
echo Sanal ortam (venv) baslatiliyor...
call venv\Scripts\activate.bat

echo FastAPI sunucusu baslatiliyor (uvicorn)...
echo.
echo Tarayiciniz otomatik olarak acilacaktir... (http://127.0.0.1:8000)
echo.
echo Sunucuyu durdurmak ve programi kapatmak icin bu pencereyi kapatabilirsiniz.
echo =======================================================
start http://127.0.0.1:8000
uvicorn main:app --reload
pause
