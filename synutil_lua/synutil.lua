local _M = {}

local ffi = require("ffi")
ffi.cdef[[
char *synutil_get_unique_hexa_identifier();
void g_free(void *data);
int link(const char *oldpath, const char *newpath);
]]
local synutil = ffi.load("synutil")

function _M.get_unique_hexa_identifier()
   if synutil == nil then
       return nil
    end
    local cres = synutil.synutil_get_unique_hexa_identifier()
    local res = ffi.string(cres)
    synutil.g_free(cres)
    return res
end

function _M.link(oldpath, newpath)
    return ffi.C.link(oldpath, newpath)
end

function _M.exit_with_ngx_error(code, message, log_message)
    if log_message ~= nil then
        if log_message == "SAME" then
            ngx.log(ngx.ERR, message)
        else
            ngx.log(ngx.ERR, log_message)
        end
    end
    ngx.status = code
    ngx.say(message)
    ngx.exit(200) -- yes this is normal
end

return _M
