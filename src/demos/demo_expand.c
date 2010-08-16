#include "ftk.h"
#include "ftk_animator_expand.h"

static void create_ani_window(int type, int sync);

static Ret button_to_east_south_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_EAST_SOUTH, 1);

	return RET_OK;
}

static Ret button_to_east_north_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_EAST_NORTH, 1);

	return RET_OK;
}

static Ret button_to_right_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_RIGHT, 0);

	return RET_OK;
}

static Ret button_to_down_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_DOWN, 0);

	return RET_OK;
}

static Ret button_to_up_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_UP, 0);

	return RET_OK;
}

static Ret button_to_brink_clicked(void* ctx, void* obj)
{
	create_ani_window(FTK_ANI_TO_BRINK, 0);

	return RET_OK;
}

static Ret button_close_clicked(void* ctx, void* obj)
{
	FtkWidget* win = ctx;
	ftk_logd("%s: close window %s\n", __func__, ftk_widget_get_text(win));
	ftk_widget_unref(win);

	return RET_OK;
}

static Ret button_quit_clicked(void* ctx, void* obj)
{
	FtkWidget* win = ctx;
	ftk_widget_unref(win);
	ftk_logd("%s: close window %s\n", __func__, ftk_widget_get_text(win));

	return RET_OK;
}

static void create_ani_window(int type, int sync)
{
	int delta = 0;
	int width = 0;
	int height = 0;
	FtkWidget* button = NULL;
	FtkGc gc = {0};
	char filename[FTK_MAX_PATH+1] = {0};
	FtkWidget* win = ftk_app_window_create();
	FtkAnimator* ani = ftk_animator_expand_create(1);
	
	gc.mask = FTK_GC_BITMAP;
	width = ftk_widget_width(win);
	height = ftk_widget_height(win);
	delta = height/6;

	button = ftk_button_create(win, width/3, height/3, width/3, 50);
	ftk_widget_set_text(button, "关闭");
	ftk_widget_show(button, 1);
	ftk_button_set_clicked_listener(button, button_close_clicked, win);
	
	ftk_snprintf(filename, FTK_MAX_PATH, "%s/jpeg1.jpg", TESTDATA_DIR);
	gc.bitmap = ftk_bitmap_factory_load(ftk_default_bitmap_factory(), filename);
	ftk_widget_set_gc(win, FTK_WIDGET_NORMAL, &gc);
	ftk_gc_reset(&gc);

	switch(type)
	{
		case FTK_ANI_TO_RIGHT:
		case FTK_ANI_TO_EAST_SOUTH:
		case FTK_ANI_TO_EAST_NORTH:
		{
			ftk_animator_set_param(ani, type, 100, width, delta, 200);
			break;
		}
		case FTK_ANI_TO_BRINK:
		case FTK_ANI_TO_DOWN:
		{
			ftk_animator_set_param(ani, type, 100, height, delta, 200);
			break;
		}
		case FTK_ANI_TO_UP:
		{
			ftk_animator_set_param(ani, type, height - 100, ftk_widget_top(win), delta, 200);
			break;
		}
		default:break;
	}
	ftk_animator_start(ani, win, 0);

	return;
}

static void create_app_window(void)
{
	char title[32] = {0};
	int width = 0;
	int height = 0;
	FtkWidget* win = ftk_app_window_create();
	FtkWidget* button = NULL;
	
	width = ftk_widget_width(win);
	height = ftk_widget_height(win);

	button = ftk_button_create(win, 5, height/6, width/2-5, 50);
	ftk_widget_set_text(button, "向右伸展");
	ftk_button_set_clicked_listener(button, button_to_right_clicked, win);

	button = ftk_button_create(win, width/2, height/6, width/2-5, 50);
	ftk_widget_set_text(button, "Down");
	ftk_button_set_clicked_listener(button, button_to_down_clicked, win);

	button = ftk_button_create(win, 5, height/6 + 60, width/2-5, 50);
	ftk_widget_set_text(button, "RightDown");
	ftk_button_set_clicked_listener(button, button_to_east_south_clicked, win);

	button = ftk_button_create(win, width/2, height/6 + 60, width/2-5, 50);
	ftk_widget_set_text(button, "RightUp");
	ftk_button_set_clicked_listener(button, button_to_east_north_clicked, win);
	
	button = ftk_button_create(win, 5, height/6 + 120, width/2-5, 50);
	ftk_widget_set_text(button, "Up");
	ftk_button_set_clicked_listener(button, button_to_up_clicked, win);
	
	button = ftk_button_create(win, width/2, height/6 + 120, width/2-5, 50);
	ftk_widget_set_text(button, "Brink");
	ftk_button_set_clicked_listener(button, button_to_brink_clicked, win);

	button = ftk_button_create(win, width/4-2, height/6 + 180, width/2-5, 50);
	ftk_widget_set_text(button, "Quit");
	ftk_button_set_clicked_listener(button, button_quit_clicked, win);

	ftk_snprintf(title, sizeof(title), "Expand Demo");
	ftk_widget_set_text(win, title);
	FTK_QUIT_WHEN_WIDGET_CLOSE(win);

	ftk_widget_show_all(win, 1);

	return;
}

#ifdef FTK_AS_PLUGIN
#include "ftk_app_demo.h"
FTK_HIDE int FTK_MAIN(int argc, char* argv[]);
FtkApp* ftk_app_demo_expand_create()
{
	return ftk_app_demo_create(_("expand"), ftk_main);
}
#else
#define FTK_HIDE extern
#endif /*FTK_AS_PLUGIN*/

FTK_HIDE int FTK_MAIN(int argc, char* argv[])
{
	FTK_INIT(argc, argv);
	
	create_app_window();

	FTK_RUN();

	return 0;
}

