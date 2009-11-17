/*
 * File: ftk_check_button.c    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   check button widget 
 *
 * Copyright (c) 2009  Li XianJing <xianjimli@hotmail.com>
 *
 * Licensed under the Academic Free License version 2.1
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

/*
 * History:
 * ================================================================
 * 2009-11-15 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_log.h"
#include "ftk_canvas.h"
#include "ftk_globals.h"
#include "ftk_window.h"
#include "ftk_style.h"
#include "ftk_icon_cache.h"
#include "ftk_check_button.h"
#include "ftk_radio_group.h"

typedef struct _PrivInfo
{
	int checked;
	int is_radio;
	int icon_at_right;
	FtkListener listener;
	void* listener_ctx;
}PrivInfo;

static Ret ftk_check_button_check(FtkWidget* thiz)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);
	
	if(priv->is_radio && ftk_widget_type(ftk_widget_parent(thiz)) == FTK_RADIO_GROUP)
	{
		ret = ftk_radio_group_set_checked(ftk_widget_parent(thiz), thiz);
	}
	else
	{
		ret = ftk_check_button_set_checked(thiz, !priv->checked);
	}

	return ret;
}

static Ret ftk_check_button_on_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);
	switch(event->type)
	{
		case FTK_EVT_MOUSE_DOWN:
		{
			ftk_widget_set_active(thiz, 1);
			ftk_window_grab(ftk_widget_toplevel(thiz), thiz);
			break;
		}
		case FTK_EVT_MOUSE_UP:
		{
			ftk_window_ungrab(ftk_widget_toplevel(thiz), thiz);
			ret = FTK_CALL_LISTENER(priv->listener, priv->listener_ctx, thiz);
			ftk_widget_set_active(thiz, 0);
			ftk_check_button_check(thiz);
			break;
		}
		case FTK_EVT_KEY_DOWN:
		{
			if(FTK_IS_ACTIVE_KEY(event->u.key.code))
			{
				ftk_widget_set_active(thiz, 1);
			}
			break;
		}
		case FTK_EVT_KEY_UP:
		{
			if(FTK_IS_ACTIVE_KEY(event->u.key.code))
			{
				ret = FTK_CALL_LISTENER(priv->listener, priv->listener_ctx, thiz);
				ftk_widget_set_active(thiz, 0);
				ftk_check_button_check(thiz);
			}
			break;
		}
		default:break;
	}

	return ret;
}

static const char* check_bg_on_imgs[FTK_WIDGET_STATE_NR] = 
{
	[FTK_WIDGET_NORMAL]      = "btn_check_on.png",
	[FTK_WIDGET_ACTIVE]      = "btn_check_on_pressed.png",
	[FTK_WIDGET_INSENSITIVE] = "btn_check_on_disable.png",
	[FTK_WIDGET_FOCUSED]     = "btn_check_on_selected.png"
};

static const char* check_bg_off_imgs[FTK_WIDGET_STATE_NR] = 
{
	[FTK_WIDGET_NORMAL]      = "btn_check_off.png",
	[FTK_WIDGET_ACTIVE]      = "btn_check_off_pressed.png",
	[FTK_WIDGET_INSENSITIVE] = "btn_check_off_disable.png",
	[FTK_WIDGET_FOCUSED]     = "btn_check_off_selected.png"
};

static const char* radio_bg_on_imgs[FTK_WIDGET_STATE_NR] = 
{
	[FTK_WIDGET_NORMAL]      = "btn_radio_on.png",
	[FTK_WIDGET_ACTIVE]      = "btn_radio_on_pressed.png",
	[FTK_WIDGET_INSENSITIVE] = "btn_radio_on.png",
	[FTK_WIDGET_FOCUSED]     = "btn_radio_on_selected.png"
};

static const char* radio_bg_off_imgs[FTK_WIDGET_STATE_NR] = 
{
	[FTK_WIDGET_NORMAL]      = "btn_radio_off.png",
	[FTK_WIDGET_ACTIVE]      = "btn_radio_off_pressed.png",
	[FTK_WIDGET_INSENSITIVE] = "btn_radio_off.png",
	[FTK_WIDGET_FOCUSED]     = "btn_radio_off_selected.png"
};

static Ret ftk_check_button_on_paint(FtkWidget* thiz)
{
	int dx = 0;
	int dy = 0;
	int icon_w = 0;
	int icon_h = 0;

	FtkBitmap* bitmap = NULL;
	DECL_PRIV0(thiz, priv);
	const char** bg_imgs = NULL;
	FTK_BEGIN_PAINT(x, y, width, height, canvas);
	
	if(priv->is_radio)
	{
		bg_imgs = priv->checked ? radio_bg_on_imgs : radio_bg_off_imgs;
	}
	else
	{
		bg_imgs = priv->checked ? check_bg_on_imgs : check_bg_off_imgs;
	}

	bitmap = ftk_icon_cache_load(ftk_default_icon_cache(), bg_imgs[ftk_widget_state(thiz)]);
	return_val_if_fail(bitmap != NULL, RET_FAIL);

	icon_w = ftk_bitmap_width(bitmap);
	icon_h = ftk_bitmap_height(bitmap);
	assert((icon_w) <= width && icon_h <= height);

	dy = (height - icon_h) / 2;
	dx = priv->icon_at_right ? width - icon_w : 0;
	ftk_canvas_draw_bitmap(canvas, bitmap, 0, 0, icon_w, icon_h, x + dx, y + dy);

	if(ftk_widget_get_text(thiz) != NULL)
	{
		dy = (height + 12)/2;
		dx = priv->icon_at_right ? 2 : icon_w;
		
		ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz)); 
		ftk_canvas_draw_string(canvas, x + dx, y + dy, ftk_widget_get_text(thiz), -1);
	}

	FTK_END_PAINT();
}

static void ftk_check_button_destroy(FtkWidget* thiz)
{
	if(thiz != NULL)
	{
		DECL_PRIV0(thiz, priv);
		FTK_ZFREE(priv, sizeof(PrivInfo));
	}

	return;
}

FtkWidget* ftk_check_button_create_ex(int id, int x, int y, int width, int height, int radio)
{
	FtkWidget* thiz = (FtkWidget*)FTK_ZALLOC(sizeof(FtkWidget));

	if(thiz != NULL)
	{
		FtkGc gc = {.mask = FTK_GC_FG | FTK_GC_BG};
		thiz->priv_subclass[0] = (PrivInfo*)FTK_ZALLOC(sizeof(PrivInfo));

		DECL_PRIV0(thiz, priv);
		priv->is_radio = radio;
		thiz->on_event = ftk_check_button_on_event;
		thiz->on_paint = ftk_check_button_on_paint;
		thiz->destroy  = ftk_check_button_destroy;

		ftk_widget_init(thiz, FTK_BUTTON, id);
		ftk_widget_move(thiz, x, y);
		ftk_widget_resize(thiz, width, height);

		gc.fg = ftk_style_get_color(FTK_COLOR_BTNTEXT);
		gc.bg = ftk_style_get_color(FTK_COLOR_BTNFACE);
		ftk_widget_set_gc(thiz, FTK_WIDGET_NORMAL, &gc);
		
		gc.fg = ftk_style_get_color(FTK_COLOR_GRAYTEXT);
		ftk_widget_set_gc(thiz, FTK_WIDGET_INSENSITIVE, &gc);
		
		gc.fg = ftk_style_get_color(FTK_COLOR_BTNTEXT);
		gc.bg = ftk_style_get_color(FTK_COLOR_BTNHIGHLIGHT);
		ftk_widget_set_gc(thiz, FTK_WIDGET_FOCUSED, &gc);
		ftk_widget_set_attr(thiz, FTK_ATTR_TRANSPARENT);
	}

	return thiz;
}

FtkWidget* ftk_check_button_create(int id, int x, int y, int width, int height)
{
	return ftk_check_button_create_ex(id, x, y, width, height, 0);	
}

FtkWidget* ftk_radio_button_create(int id, int x, int y, int width, int height)
{
	return ftk_check_button_create_ex(id, x, y, width, height, 1);	
}

int        ftk_check_button_get_checked(FtkWidget* thiz)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, 0);

	return priv->checked;
}

Ret ftk_check_button_set_icon_position(FtkWidget* thiz, int at_right)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, RET_FAIL);

	if(priv->icon_at_right != at_right)
	{
		priv->icon_at_right = at_right;
		ftk_widget_paint_self(thiz);
	}

	return RET_OK;
}

Ret        ftk_check_button_set_checked(FtkWidget* thiz, int checked)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, RET_FAIL);

	if(priv->checked != checked)
	{
		priv->checked = checked;
		ftk_widget_paint_self(thiz);
	}

	return RET_OK;
}

Ret ftk_check_button_set_clicked_listener(FtkWidget* thiz, FtkListener listener, void* ctx)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, RET_FAIL);

	priv->listener_ctx = ctx;
	priv->listener = listener;

	return RET_OK;
}

