xml=[[
<?xml version="1.0" encoding="utf-8"?>
<window value="Entry Label">
	<label  id="1" x="5" y="5" w="$ww/4" h="30" value="Name" />
	<entry  id="2" x="$ww/4+5" y="5" w="3*$ww/4-15" h="30" value="Li XianJing" />
	
	<label  id="3" x="5" y="40" w="$ww/4" h="30" value="EMail" />
	<entry  id="4" x="$ww/4+5" y="40" w="3*$ww/4-15" h="30" value="xianjimli@hotmail.com" />
	
	<label  id="5" x="5" y="75" w="$ww/4" h="30" value="Mobile" />
	<entry  id="6" x="$ww/4+5" y="75" w="3*$ww/4-15" h="30" value="+8613911112222" />
	
	<button id="99" x="5" y="3*$wh/4" w="$ww/2-5" h="50" value="Save" />
	<button id="100" x="$ww/2" y="3*$wh/4" w="$ww/2-5" h="50" attr="$FTK_ATTR_FOCUSED" value="Quit" />
</window>
]]

function OnQuit(button)
	ftk_quit()
	print(button:GetText() .. " Clicked.")
	return RET_OK
end

function OnSave(button)
	print(button:GetText() .. " Clicked.")
	return RET_OK
end

Ftk.Init(1, {"demo4"})
win=FtkXul.Load(xml, #xml)

button = win:Lookup(99)
FtkButton.SetClickedListener(button, "OnSave")

button=win:Lookup(100)
FtkButton.SetClickedListener(button, "OnQuit")

win:ShowAll(1)
Ftk.Run()


