// demo_xul.cpp : ����Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#include "demo_xul.h"

static int argc = 2;
static char* argv[] = {"ftk", "../../../demos/t1.xul", NULL};
extern "C" int ftk_main(int argc, char* argv[]);

int APIENTRY _tWinMain(HINSTANCE hInstance,
                     HINSTANCE hPrevInstance,
                     LPTSTR    lpCmdLine,
                     int       nCmdShow)
{

	return ftk_main(argc, argv);
}