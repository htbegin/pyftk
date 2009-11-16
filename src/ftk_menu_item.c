/*
 * File: ftk_menu_item.c    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   menu item. 
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
 * 2009-10-30 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_log.h"
#include "ftk_canvas.h"
#include "ftk_menu_item.h"
#include "ftk_globals.h"
#include "ftk_icon_cache.h"

typedef struct _PrivInfo
{
	int menu_item_down;
	FtkListener listener;
	void* listener_ctx;
}PrivInfo;

static Ret ftk_menu_item_on_event(FtkWidget* thiz, FtkEvent* event)
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
			ftk_widget_set_active(thiz, 0);
			ftk_window_ungrab(ftk_widget_toplevel(thiz), thiz);
			ret = FTK_CALL_LISTENER(priv->listener, priv->listener_ctx, thiz);
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
			}
			break;
		}
		default:break;
	}

	return ret;
}

static const char* bg_imgs[FTK_WIDGET_STATE_NR] = 
{
	[FTK_WIDGET_ACTIVE] = "menuitem_background_pressed.png",
	[FTK_WIDGET_FOCUSED] = "menuitem_background_focus.png"
};

static Ret ftk_menu_item_on_paint(FtkWidget* thiz)
{
	FtkBitmap* bitmap = NULL;
	FTK_BEGIN_PAINT(x, y, width, height, canvas);
	return_val_if_fail(width > 0 && height > 0, RET_FAIL);

	if(bg_imgs[ftk_widget_state(thiz)] != NULL)
	{
		bitmap = ftk_icon_cache_load(ftk_default_icon_cache(), bg_imgs[ftk_widget_state(thiz)]);
		ftk_canvas_draw_bg_image(canvas, bitmap, FTK_BG_FOUR_CORNER, x, y, width, height);
	}

	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	if(ftk_widget_get_text(thiz))
	{
		const char* text = ftk_widget_get_text(thiz);
		int fh = ftk_canvas_font_height(canvas);
		int fw = ftk_canvas_get_extent(canvas, text, -1);
		int dx = (width - fw)>>1;
		int dy = (height + 12)>>1;
	
		assert(fh < height && fw < width);
		ftk_canvas_draw_string(canvas, x + dx, y + dy, text, -1);
	}
	
	FTK_END_PAINT();
}

static void ftk_menu_item_destroy(FtkWidget* thiz)
{
	if(thiz != NULL)
	{
		DECL_PRIV0(thiz, priv);
		FTK_FREE(priv);
	}

	return;
}

FtkWidget* ftk_menu_item_create(int id)
{
	FtkWidget* thiz = (FtkWidget*)FTK_ZALLOC(sizeof(FtkWidget));

	if(thiz != NULL)
	{
		thiz->priv_subclass[0] = (PrivInfo*)FTK_ZALLOC(sizeof(PrivInfo));

		thiz->on_event = ftk_menu_item_on_event;
		thiz->on_paint = ftk_menu_item_on_paint;
		thiz->destroy  = ftk_menu_item_destroy;

		ftk_widget_init(thiz, FTK_MENU_ITEM, id);
		ftk_widget_set_attr(thiz, FTK_ATTR_TRANSPARENT);
	}

	return thiz;
}

Ret ftk_menu_item_set_clicked_listener(FtkWidget* thiz, FtkListener listener, void* ctx)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, RET_FAIL);

	priv->listener_ctx = ctx;
	priv->listener = listener;

	return RET_OK;
}

