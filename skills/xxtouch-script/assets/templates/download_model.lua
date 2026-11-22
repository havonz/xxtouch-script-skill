-- 仅在开发者要求设备端准备模型时生成；调用方决定何时下载和如何展示错误。
local model_id = "@@MODEL_ID@@"
local model_files = {
@@FILES@@
}

return function(model_dir)
    model_dir = model_dir or (XXT_HOME_PATH .. "/models/" .. model_id)
    local openssl = require("openssl")

    local function verify(path, spec)
        if file.size(path) ~= spec.size then
            return false
        end
        local input, err = io.open(path, "rb")
        if not input then
            return nil, err
        end
        -- 分块计算摘要，避免把大型模型一次性读入 Lua 内存。
        local ok, digest = pcall(function()
            local ctx = openssl.digest.new("sha256")
            while true do
                local chunk, read_err = input:read(1024 * 1024)
                if not chunk then
                    if read_err then error(read_err) end
                    break
                end
                assert(ctx:update(chunk))
            end
            return ctx:final()
        end)
        input:close()
        if not ok then
            return nil, digest
        end
        return digest == spec.sha256
    end

    for i = 1, #model_files do
        local spec = model_files[i]
        local target = model_dir .. "/" .. spec.path
        local valid, verify_err = verify(target, spec)
        if verify_err then
            return nil, verify_err
        end
        if not valid then
            local ok, err = file.mkdir_p(target:match("^(.*)/[^/]+$"))
            if not ok then return nil, err end
            local partial = target .. "." .. utils.gen_uuid() .. ".part"
            local completed, failure = pcall(function()
                local status = http.get{
                    url = spec.url,
                    timeout = @@TIMEOUT@@,
                    download_file = partial,
                }
                if status ~= 200 then
                    error("模型下载失败 HTTP " .. tostring(status) .. "：" .. spec.path)
                end
                local matches, check_err = verify(partial, spec)
                if not matches then
                    error(check_err or ("模型大小或 SHA256 校验失败：" .. spec.path))
                end
                local moved, move_err = file.move(partial, target, "overwrite")
                if not moved then error(move_err) end
            end)
            if not completed then
                file.remove(partial)
                return nil, tostring(failure)
            end
        end
    end
    return model_dir
end
