@echo off
echo ========================================
echo Snake Game - Anime Edition 打包脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    pause
    exit /b 1
)

echo.
echo 正在检查依赖包...
pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: pygame未安装，正在安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo 错误: 依赖包安装失败
        pause
        exit /b 1
    )
)

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: pyinstaller未安装，正在安装...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo 错误: pyinstaller安装失败
        pause
        exit /b 1
    )
)

echo.
echo 正在清理旧的构建文件...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo 正在打包游戏...
echo 这可能需要几分钟时间，请耐心等待...

REM 检查图标文件是否存在
set ICON_PARAM=
if exist "assets\icon.ico" (
    set ICON_PARAM=--icon=assets\icon.ico
    echo 使用自定义图标: assets\icon.ico
) else (
    echo 警告: 未找到图标文件 assets\icon.ico，将使用默认图标
)

REM 执行打包命令
pyinstaller --onefile --windowed --clean %ICON_PARAM% --name="SnakeGame-AnimeEdition" main.py

if %errorlevel% neq 0 (
    echo.
    echo 错误: 打包失败！
    echo 请检查错误信息并重试
    pause
    exit /b 1
)

echo.
echo ========================================
echo 打包完成！
echo ========================================
echo.
echo 可执行文件位置: dist\SnakeGame-AnimeEdition.exe
echo 文件大小:
dir "dist\SnakeGame-AnimeEdition.exe" | find ".exe"
echo.
echo 注意事项:
echo 1. 首次运行时会自动创建 config.json 配置文件
echo 2. assets 文件夹中的资源文件已打包到exe中
echo 3. 游戏数据会保存在exe同目录下的 config.json 文件中
echo.
echo 按任意键退出...
pause >nul