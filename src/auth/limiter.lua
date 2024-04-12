local key = KEYS[1] -- 使用者的key, 例如 'user:loginfail:123'
local limit = tonumber(ARGV[1]) -- 失敗次數限制，這裡是5
local ttl = tonumber(ARGV[2]) -- 冷卻時間（秒），這裡是60秒
local reset_interval = tonumber(ARGV[3]) -- 重置間隔，例如600秒（10分鐘）

local current = redis.call('GET', key) or 0

if tonumber(current) >= limit then
    -- 如果已達到限制，檢查冷卻時間
    local ttl = redis.call('TTL', key)
    if ttl > 0 then
        -- 如果還在冷卻期，返回剩餘時間
        return {false, ttl}
    else
        -- 如果冷卻已過，重置計數並重新開始計時
        redis.call('SET', key, 1, 'EX', reset_interval)
        return {true, tonumber(current)}
    end
else
    -- 如果未達到限制，增加計數
    redis.call('INCR', key)
    redis.call('EXPIRE', key, reset_interval) -- 更新過期時間
    if tonumber(redis.call('GET', key)) == limit then
        -- 達到限制時設置冷卻時間
        redis.call('EXPIRE', key, ttl)
    end
    return {true, tonumber(current)}
end