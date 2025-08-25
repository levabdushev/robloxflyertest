local HttpService = game:GetService("HttpService")

-- Загружаем конфиг
local cfg = HttpService:JSONDecode(readfile("config.json"))
local BOT_TOKEN = cfg["BOT_TOKEN"]
local CHAT_ID = tostring(cfg["CHAT_ID"])

local Http = (syn and syn.request) or http_request or request
local username = game.Players.LocalPlayer.Name

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

notify_telegram("Пользователь **" .. username .. "** запустил ваш скрипт!")