@echo off
REM Script para rodar E-Lixo com Docker (inclui monitoramento)

echo.
echo ===== E-Lixo Docker Launcher =====
echo.

REM Verificar se Docker está rodando
docker ps > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker nao esta rodando. Inicie Docker Desktop.
    pause
    exit /b 1
)

echo [1/3] Verificando imagem e-lixo:latest...
docker images | find "e-lixo" > nul
if errorlevel 1 (
    echo [ERROR] Imagem nao encontrada. Execute primeiro:
    echo   docker compose build --no-cache
    pause
    exit /b 1
)
echo [OK] Imagem encontrada

echo.
echo [2/3] Iniciando container...
docker compose up

echo.
echo [3/3] Finalizando...
echo Acesse: http://localhost:8000
pause
