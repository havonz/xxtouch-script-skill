if main_json_items == nil then
	local function __xxt_text(value, fallback)
		return type(value) == 'string' and value ~= '' and value or fallback
	end

	local function __xxt_read_main_json()
		local path = xpp.resource_path('main.json')
		if not path then
			return nil
		end
		local f = io.open(path, 'r')
		if not f then
			return nil
		end
		local content = f:read('*a')
		f:close()
		local ok, config = pcall(json.decode, content)
		return ok and type(config) == 'table' and config or nil
	end

	local function __xxt_options(item)
		local list = {}
		for _, value in ipairs(type(item.item) == 'table' and item.item or {}) do
			if type(value) == 'string' and value ~= '' then
				list[#list + 1] = value
			end
		end
		return list
	end

	local function __xxt_option_at(options, index)
		index = tonumber(index)
		return index and options[math.floor(index)] or nil
	end

	local function __xxt_checked_options(options, indexes)
		local values = {}
		for _, index in ipairs(type(indexes) == 'table' and indexes or {}) do
			local value = __xxt_option_at(options, index)
			if value then
				values[#values + 1] = value
			end
		end
		return #values > 0 and values or nil
	end

	local function __xxt_key(item, index)
		return __xxt_text(item.key, __xxt_text(item.caption, 'item_' .. tostring(index)))
	end

	local convert = {}

	function convert.Label(items, item)
		items[#items + 1] = {
			cell = 'StaticText';
			label = __xxt_text(item.caption, '');
			alignment = ({center = 'Center', right = 'Right'})[item.align] or 'Left';
		}
	end

	function convert.Edit(items, item, index, defaults)
		local label = __xxt_text(item.caption, '')
		if label ~= '' then
			items[#items + 1] = {cell = 'Group'; label = label}
		end
		local out = {
			cell = item.allowMultiline and 'Textarea' or 'TextField';
			defaults = defaults;
			key = __xxt_key(item, index);
			default = __xxt_text(item.text, '');
			placeholder = __xxt_text(item.placeholder, '');
		}
		if not item.allowMultiline then
			out.validationRegex = __xxt_text(item.validationRegex, item.nonEmpty and '.+' or nil)
			out.message = __xxt_text(item.patternMessage, nil)
		end
		items[#items + 1] = out
	end

	function convert.ComboBox(items, item, index, defaults)
		local options = __xxt_options(item)
		local label = __xxt_text(item.caption, '')
		if label ~= '' then
			items[#items + 1] = {cell = 'Group'; label = label}
		end
		if item.canEdit and tonumber(item.select) == 0 then
			items[#items + 1] = {
				cell = 'TextField';
				defaults = defaults;
				key = __xxt_key(item, index);
				default = __xxt_text(item.text, '');
				validationRegex = __xxt_text(item.validationRegex, item.nonEmpty and '.+' or nil);
				message = __xxt_text(item.patternMessage, nil);
			}
			return
		end
		items[#items + 1] = {
			cell = 'Option';
			label = label;
			popoverMode = true;
			defaults = defaults;
			key = __xxt_key(item, index);
			default = __xxt_option_at(options, item.select);
			options = options;
		}
	end

	function convert.RadioGroup(items, item, index, defaults)
		local options = __xxt_options(item)
		items[#items + 1] = {cell = 'Group'; label = __xxt_text(item.caption, '')}
		items[#items + 1] = {
			cell = 'Radio';
			defaults = defaults;
			key = __xxt_key(item, index);
			default = __xxt_option_at(options, item.select);
			numPerLine = tonumber(item.numPerLine) or 1;
			options = options;
		}
	end

	function convert.CheckBoxGroup(items, item, index, defaults)
		local options = __xxt_options(item)
		if item.orderedSelection then
			items[#items + 1] = {
				cell = 'OrderedOption';
				label = __xxt_text(item.caption, '');
				defaults = defaults;
				key = __xxt_key(item, index);
				default = __xxt_checked_options(options, item.select);
				options = options;
			}
		else
			items[#items + 1] = {cell = 'Group'; label = __xxt_text(item.caption, '')}
			items[#items + 1] = {
				cell = 'Checkbox';
				defaults = defaults;
				key = __xxt_key(item, index);
				default = __xxt_checked_options(options, item.select);
				numPerLine = tonumber(item.numPerLine) or 1;
				options = options;
			}
		end
	end

	function main_json_items(defaults)
		local config = __xxt_read_main_json()
		if not config then
			return nil
		end

		local items = {}
		for index, item in ipairs(type(config.UI) == 'table' and config.UI or config) do
			local fn = type(item) == 'table' and convert[item.type] or nil
			if fn then
				fn(items, item, index, defaults)
			end
		end
		return items
	end
end
