local args = proc_get("spawn_args")
local ip = "0.0.0.0"
local port = 46542
args = json.decode(args)
if type(args) == "table" then
	ip = args.log_ip or ip
	port = args.log_port or port
else
	return function()return function()end end
end
return (function()
	local socket = require("socket")
	local select = select
	local insert = table.insert
	local deep_dump = table.deep_dump
	local type = type
	local getinfo = debug.getinfo
	local concat = table.concat
	local tostring = tostring
	local string_pack = string.pack
	local os_date = os.date
	local SendMessage = function(...)
		if not (ip and ip ~= '') then return end
		local s = socket.tcp()
		s:settimeout(2)
		if s:connect(ip, port) == 1 then
			local _m = {};
			for i = 1, select('#', ...) do
				local a = select(i, ...)
				if type(a) == 'table' then
					insert(_m, deep_dump(a))
				elseif type(a) == 'string' then
					local m = tostring(a):gsub('%[DATE%]',os_date('[%Y-%m-%d %H:%M:%S]')):gsub('%[LINE%]','['..tostring(getinfo(2).currentline)..']')
					insert(_m, m)
				else
					insert(_m, tostring(a))
				end
			end
			local _message = concat(_m, '\t')
			s:send(string_pack('>I', #_message) .. _message);
			s:receive(2)
			s:close()
		end
		return ...
	end
	return SendMessage
end)