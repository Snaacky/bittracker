math.randomseed(os.time())

local function rand_str(n)
    local chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    local s = ""
    for i = 1, n do
        s = s .. chars:sub(math.random(1, #chars), math.random(1, #chars))
    end
    return s
end

local function maybe(value)
    if math.random() < 0.7 then
        return value
    else
        return nil
    end
end

local function random_event()
    if math.random() < 0.7 then
        local events = {"started", "stopped", "paused"}
        return events[math.random(1, #events)]
    else
        return nil
    end
end

local function random_announce_query()
    local params = {
        info_hash = rand_str(20),
        peer_id   = rand_str(20),
        port      = tostring(math.random(1025, 65535)),
        uploaded  = maybe(tostring(math.random(0, 100000))),
        downloaded= maybe(tostring(math.random(0, 100000))),
        left      = maybe(tostring(math.random(0, 50000))),
        compact   = maybe(tostring(math.random(0,1))),
        numwant   = maybe(tostring(math.random(10, 50))),
        event     = random_event()
    }

    local query_parts = {}
    for k, v in pairs(params) do
        if v then
            table.insert(query_parts, k .. "=" .. v)
        end
    end

    return "/announce?" .. table.concat(query_parts, "&")
end

request = function()
    local path = random_announce_query()
    return wrk.format("GET", path)
end
