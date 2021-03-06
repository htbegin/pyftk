/*This file is generated by luagen.*/
#include "lua_ftk_xul.h"
#include "lua_ftk_callbacks.h"

static void tolua_reg_types (lua_State* L)
{
	tolua_usertype(L, "FtkXul");
}

static int lua_ftk_xul_load(lua_State* L)
{
	tolua_Error err = {0};
	FtkWidget* retv;
	char* xml;
	int length;
	int param_ok = tolua_isstring(L, 1, 0, &err) && tolua_isnumber(L, 2, 0, &err);

	return_val_if_fail(param_ok, 0);

	xml = (char*)tolua_tostring(L, 1, 0);
	length = tolua_tonumber(L, 2, 0);
	retv = ftk_xul_load(xml, length);
	tolua_pushusertype(L, (FtkWidget*)retv, "FtkWidget");

	return 1;
}

int tolua_ftk_xul_init(lua_State* L)
{
	tolua_open(L);
	tolua_reg_types(L);
	tolua_module(L, NULL, 0);
	tolua_beginmodule(L, NULL);
	tolua_cclass(L,"FtkXul", "FtkXul", "", NULL);
	tolua_beginmodule(L, "FtkXul");
	tolua_function(L, "Load", lua_ftk_xul_load);
	tolua_endmodule(L);
	tolua_endmodule(L);


	return 1;
}
