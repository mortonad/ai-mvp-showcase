# AI MVP Showcase 上傳自動化腳本
# 用途：將 5 個 MVP 同步到 GitHub 倉庫

$projectName = "ai-mvp-showcase"

Write-Host "--- 準備上傳 AI MVP Portfolio ---" -ForegroundColor Cyan

# 1. 初始化
if (!(Test-Path .git)) {
    git init
}

# 2. 暫存與提交
git add .
git commit -m "feat: setup AI MVP Showcase with 5 core MVPs and Colab integration"

# 3. 指引
Write-Host ""
Write-Host "--- 下一步指令 ---" -ForegroundColor Cyan
Write-Host "請在 GitHub 建立一個名為 '$projectName' 的新倉庫，然後執行："
Write-Host "git remote add origin https://github.com/你的帳號/$projectName.git"
Write-Host "git branch -M main"
Write-Host "git push -u origin main"
Write-Host "----------------"
Write-Host "完成！Colab 連結將在 Push 後自動生效。" -ForegroundColor Green
