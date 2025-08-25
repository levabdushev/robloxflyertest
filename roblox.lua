local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local GuiService = game:GetService("StarterGui")

-- ==== Настройки ====
local config_path = "config.json"
local commands_path = "commands.json"

-- ==== Загрузка конфига ====
local cfg = {}
pcall(function
    cfg = HttpService:JSONDecode(readfile(config_path))
end)

local BOT_TOKEN = cfg["BOT_TOKEN"] or ""
local CHAT_ID = tostring(cfg["CHAT_ID"] or "")

local Http = (syn and syn.request) or http_request or request

-- ==== Функция уведомления в Telegram ====
local function notify_telegram(text)
    Http({
        Url = "https://api.telegram.org/bot" .. BOT_TOKEN .. "/sendMessage",
        Method = "POST",
        Headers = {["Content-Type"] = "application/json"},
        Body = HttpService:JSONEncode({
            chat_id = CHAT_ID,
            text = text
        })
    })
end

-- ==== Уведомление о запуске ====
notify_telegram("Пользователь **" .. LocalPlayer.Name .. "** запустил скрипт!")

-- ==== Функция отображения ошибки на экране ====
local function show_error_log(err)
    local screenGui = Instance.new("ScreenGui")
    screenGui.Name = "ErrorLogGui"
    screenGui.Parent = LocalPlayer:WaitForChild("PlayerGui")

    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1,0,0.5,0)
    frame.Position = UDim2.new(0,0,0.25,0)
    frame.BackgroundColor3 = Color3.fromRGB(50,0,0)
    frame.Parent = screenGui

    local textLabel = Instance.new("TextLabel")
    textLabel.Size = UDim2.new(1,-20,1,-50)
    textLabel.Position = UDim2.new(0,10,0,10)
    textLabel.Text = err
    textLabel.TextColor3 = Color3.fromRGB(255,255,255)
    textLabel.TextWrapped = true
    textLabel.TextScaled = true
    textLabel.BackgroundTransparency = 1
    textLabel.Parent = frame

    local copyBtn = Instance.new("TextButton")
    copyBtn.Size = UDim2.new(0,150,0,40)
    copyBtn.Position = UDim2.new(0.5,-75,1,-50)
    copyBtn.Text = "Copy All"
    copyBtn.BackgroundColor3 = Color3.fromRGB(200,200,200)
    copyBtn.TextColor3 = Color3.fromRGB(0,0,0)
    copyBtn.Parent = frame

    copyBtn.MouseButton1Click:Connect(function()
        setclipboard(err)
    end)
end

-- ==== Функция уведомления об успешном запуске ====
local function show_success()
    GuiService:SetCore("SendNotification", {
        Title = "Roblox Script",
        Text = "script executed ✅",
        Duration = 3
    })
end

-- ==== Основной цикл ====
local success, err = pcall(function()
    if isfile(commands_path) then
        local data = HttpService:JSONDecode(readfile(commands_path))
        local username = LocalPlayer.Name
        local command = data[username]
        if command then
            if command == "jump" then
                LocalPlayer.Character.Humanoid.Jump = true
            elseif command == "kill" then
                LocalPlayer.Character:BreakJoints()
            elseif command == "glitch" then
                for i=1,20 do
                    task.wait(0.05)
                    game.Lighting.Brightness = math.random()
                end
                game.Lighting.Brightness = 2
            elseif command == "lock" then
                LocalPlayer.PlayerScripts:ClearAllChildren()
            end
            data[username] = nil
            writefile(commands_path, HttpService:JSONEncode(data))
        end
    end
end)

-- ==== Проверка результата ====
if success then
    show_success()
else
    show_error_log(err)
end