// demo_sprite.cpp : ����Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "demo_sprite.h"

static int argc = 1;
static char* argv[] = {"ftk", NULL};
extern "C" int ftk_main(int argc, char* argv[]);

int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{

	return ftk_main(argc, argv);
}
