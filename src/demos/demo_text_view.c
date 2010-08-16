#include "ftk.h"

static Ret button_quit_clicked(void* ctx, void* obj)
{
	ftk_widget_unref(ctx);

	return RET_OK;
}

#define TEXT_STR "Multi line editor:\nfirst\nsecond\nthird\nforth\n012345667890qwertyuiopasdfghjklkzxcbnmcutukakdfasiwerksjdfaksdjfaksdjifiwjkaldfkjkalsdfjieirnlkkafjiierklaaa\n1\n2\n3\n\n4\n5\n6\n7\n8\nlast line"

#define TEXT1_STR "a\n\n4\n5\n6\n7\n8\nlast line"

#ifdef FTK_AS_PLUGIN
#include "ftk_app_demo.h"
FTK_HIDE int FTK_MAIN(int argc, char* argv[]);
FtkApp* ftk_app_demo_text_view_create()
{
	return ftk_app_demo_create(_("text_view"), ftk_main);
}
#else
#define FTK_HIDE extern
#endif /*FTK_AS_PLUGIN*/
FTK_HIDE int FTK_MAIN(int argc, char* argv[])
{
	int width = 0;
	int height = 0;
	FtkWidget* win = NULL;
	FtkWidget* button = NULL;
	FtkWidget* text_view  = NULL;

	FTK_INIT(argc, argv);

	win = ftk_app_window_create();
	width = ftk_widget_width(win);
	height = ftk_widget_height(win);
	
	text_view = ftk_text_view_create(win, 10, 10, ftk_widget_width(win) - 20, height/3);
	ftk_text_view_set_text(text_view, TEXT1_STR);
	
	text_view = ftk_text_view_create(win, 10, 15 + height/3, ftk_widget_width(win) - 20, height/3);
	ftk_text_view_set_text(text_view, TEXT_STR);
	ftk_text_view_set_readonly(text_view, 1);

	button = ftk_button_create(win, width/4, 3*height/4, width/2, 60);
	ftk_widget_set_text(button, "quit");
	ftk_button_set_clicked_listener(button, button_quit_clicked, win);
	ftk_window_set_focus(win, button);

	ftk_widget_set_text(win, "text_view demo");
	ftk_widget_show_all(win, 1);
	FTK_QUIT_WHEN_WIDGET_CLOSE(win);

	FTK_RUN();

	return 0;
}

