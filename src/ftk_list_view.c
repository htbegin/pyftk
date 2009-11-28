/*
 * File: ftk_list_view.h    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   list view
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

#include "ftk_key.h"
#include "ftk_style.h"
#include "ftk_event.h"
#include "ftk_globals.h"
#include "ftk_window.h"
#include "ftk_list_view.h"
#include "ftk_scroll_bar.h"

typedef struct _PrivInfo
{
	int current;
	int visible_nr;
	int item_height;
	int visible_start;

	int is_active;
	int top_margin;
	int botton_margin;
	int scrolled_by_me;
	FtkListModel*  model;
	FtkListRender* render;
	FtkWidget* vscroll_bar;
	
	FtkBitmap* bg_normal;
	FtkBitmap* bg_focus;
	FtkBitmap* bg_active;

	void* listener_ctx;
	FtkListener listener;
}PrivInfo;

static Ret ftk_list_view_set_cursor(FtkWidget* thiz, int current)
{
	DECL_PRIV0(thiz, priv);
	int total = ftk_list_model_get_total(priv->model);
	return_val_if_fail(total > 0, RET_FAIL);

	if(priv->current == current)
	{
		ftk_widget_paint_self(thiz);

		return RET_OK;
	}

	priv->current = current;

	if(priv->current < 0) priv->current = 0;
	if(priv->current >= total) priv->current = total - 1;

	if(priv->current < priv->visible_start)
	{
		priv->visible_start = priv->current;
	}

	if(priv->current > (priv->visible_start + priv->visible_nr - 1))
	{
		priv->visible_start = priv->current - (priv->visible_nr - 1);
	}

	ftk_widget_paint_self(thiz);

	return RET_REMOVE;
}

static Ret ftk_list_view_move_cursor(FtkWidget* thiz, int offset)
{
	DECL_PRIV0(thiz, priv);
	int total = ftk_list_model_get_total(priv->model);
	return_val_if_fail(total > 0, RET_FAIL);
	return_val_if_fail(priv->visible_nr > 0, RET_FAIL);

	if(priv->current == 0 && offset < 0)
	{
		return RET_FAIL;
	}
	else if((priv->current + 1) == total && offset > 0)
	{
		return RET_FAIL;
	}

	return ftk_list_view_set_cursor(thiz, priv->current + offset);
}

static Ret ftk_list_view_set_cursor_by_pointer(FtkWidget* thiz, int x, int y)
{
	int current = 0;
	DECL_PRIV0(thiz, priv);
	int offset = y - ftk_widget_top_abs(thiz) - priv->top_margin;
	if(offset <= 0) return RET_OK;

	current = priv->visible_start + offset/priv->item_height;

	return ftk_list_view_set_cursor(thiz, current);
}

static Ret ftk_list_view_on_key_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);
	switch(event->u.key.code)
	{
		case FTK_KEY_DOWN:
		{
			if(event->type == FTK_EVT_KEY_DOWN)
			{
				ret = ftk_list_view_move_cursor(thiz, 1);
			}
			break;
		}
		case FTK_KEY_UP:
		{
			if(event->type == FTK_EVT_KEY_DOWN)
			{
				ret = ftk_list_view_move_cursor(thiz, -1);
			}
			break;
		}
		default:
		{
			if(FTK_IS_ACTIVE_KEY(event->u.key.code))
			{
				if(event->type == FTK_EVT_KEY_DOWN)
				{
					priv->is_active = 1;
					ftk_list_view_set_cursor(thiz, priv->current);
				}
				else
				{
					FTK_CALL_LISTENER(priv->listener, priv->listener_ctx, thiz);
					priv->is_active = 0;
					ftk_list_view_set_cursor(thiz, priv->current);
				}
			}

			break;
		}
	}

	return ret;
}

static Ret ftk_list_view_on_mouse_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);

	switch(event->type)
	{
		case FTK_EVT_MOUSE_DOWN:
		{
			priv->is_active = 1;
			ftk_list_view_set_cursor_by_pointer(thiz, event->u.mouse.x, event->u.mouse.y);
			ftk_window_grab(ftk_widget_toplevel(thiz), thiz);
			break;
		}
		case FTK_EVT_MOUSE_UP:
		{
			ftk_window_ungrab(ftk_widget_toplevel(thiz), thiz);
			if(priv->is_active)
			{
				ret = FTK_CALL_LISTENER(priv->listener, priv->listener_ctx, thiz);
				priv->is_active = 0;
				ftk_list_view_set_cursor_by_pointer(thiz, event->u.mouse.x, event->u.mouse.y);
			}
			break;
		}
		default:break;
	}

	return ret;
}

static Ret ftk_list_view_on_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_FAIL;

	switch(event->type)
	{
		case FTK_EVT_KEY_UP:
		case FTK_EVT_KEY_DOWN:
		{
			ret = ftk_list_view_on_key_event(thiz, event);
			break;
		}
		case FTK_EVT_MOUSE_UP:
		case FTK_EVT_MOUSE_DOWN:
		{
			ret = ftk_list_view_on_mouse_event(thiz, event);
			break;
		}
		default:break;
	}

	return ret;
}

static Ret ftk_list_view_on_paint(FtkWidget* thiz)
{
	int i = 0;
	int dx = 0;
	int dy = 0;
	DECL_PRIV0(thiz, priv);
	FtkBitmap* bitmap = NULL;
	int total = ftk_list_model_get_total(priv->model);
	FTK_BEGIN_PAINT(x, y, width, height, canvas);

	(void)height;
	dy = y + priv->top_margin;
	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	for(i = 0; i < priv->visible_nr; i++)
	{
		int w  = 0;
		if((priv->visible_start + i) >= total)
		{
			break;
		}

		if((priv->visible_start + i) == priv->current)
		{
			bitmap = priv->is_active ? priv->bg_active : priv->bg_focus;
		}
		else
		{
			bitmap = priv->bg_normal;
		}

		dx = x + FTK_H_MARGIN;
		w = width - 2 * FTK_H_MARGIN - FTK_SCROLL_BAR_WIDTH;
		ftk_canvas_draw_bg_image(canvas, bitmap, FTK_BG_FOUR_CORNER, dx, dy, w, priv->item_height);
		ftk_list_render_paint(priv->render, canvas, priv->visible_start + i, dx, dy, w, priv->item_height);
		dy += priv->item_height;
	}

	priv->scrolled_by_me = 1;
	if(priv->visible_nr < total)
	{
		ftk_widget_show(priv->vscroll_bar, 0);
	}
	else
	{
		ftk_scroll_bar_set_param(priv->vscroll_bar, priv->current, total, priv->visible_nr);
		ftk_widget_show(priv->vscroll_bar, priv->visible_nr < total);
	}
	priv->scrolled_by_me = 0;

	FTK_END_PAINT();
}

static void ftk_list_view_destroy(FtkWidget* thiz)
{
	if(thiz != NULL)
	{
		DECL_PRIV0(thiz, priv);
		ftk_bitmap_unref(priv->bg_normal);
		ftk_bitmap_unref(priv->bg_focus);
		ftk_bitmap_unref(priv->bg_active);
		FTK_ZFREE(priv, sizeof(PrivInfo));
	}

	return;
}

FtkWidget* ftk_list_view_create(FtkWidget* parent, int x, int y, int width, int height)
{
	FtkWidget* thiz = (FtkWidget*)FTK_ZALLOC(sizeof(FtkWidget));
	return_val_if_fail(thiz != NULL, NULL);
	
	thiz->priv_subclass[0] = (PrivInfo*)FTK_ZALLOC(sizeof(PrivInfo));
	if(thiz->priv_subclass[0] != NULL)
	{
		FtkGc gc = {0};
		DECL_PRIV0(thiz, priv);
		thiz->on_event = ftk_list_view_on_event;
		thiz->on_paint = ftk_list_view_on_paint;
		thiz->destroy  = ftk_list_view_destroy;

		ftk_widget_init(thiz, FTK_LIST_VIEW, 0);
		ftk_widget_move(thiz, x, y);
		ftk_widget_resize(thiz, width, height);
		ftk_widget_append_child(parent, thiz);

		gc.mask = FTK_GC_BG;
		gc.bg = ftk_style_get_color(FTK_COLOR_LIST_BG);
		ftk_widget_set_gc(thiz, FTK_WIDGET_NORMAL, &gc);
		ftk_widget_set_gc(thiz, FTK_WIDGET_FOCUSED, &gc);
		ftk_widget_set_gc(thiz, FTK_WIDGET_ACTIVE, &gc);
		ftk_widget_set_gc(thiz, FTK_WIDGET_INSENSITIVE, &gc);

		priv->bg_normal = ftk_icon_cache_load(ftk_default_icon_cache(), 
			"list_selector_background_disabled"FTK_STOCK_IMG_SUFFIX);
		priv->bg_focus = ftk_icon_cache_load(ftk_default_icon_cache(), 
			"list_selector_background_focus"FTK_STOCK_IMG_SUFFIX);
		priv->bg_active = ftk_icon_cache_load(ftk_default_icon_cache(), 
			"list_selector_background_pressed"FTK_STOCK_IMG_SUFFIX);
	}
	else
	{
		FTK_ZFREE(thiz, sizeof(FtkWidget));
	}

	return thiz;
}

static Ret ftk_list_view_on_scroll(FtkWidget* thiz, void* obj)
{
	DECL_PRIV0(thiz, priv);

	if(!priv->scrolled_by_me)
	{
		ftk_list_view_set_cursor(thiz, ftk_scroll_bar_get_value(priv->vscroll_bar));
	}

	return RET_OK;
}

Ret ftk_list_view_init(FtkWidget* thiz, FtkListModel* model, FtkListRender* render, int item_height)
{
	int width = 0;
	int height = 0;
	int margin = 0;
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(priv != NULL && render != NULL && model != NULL && item_height > 0, RET_FAIL);
	
	priv->model       = model;
	priv->render      = render;
	priv->item_height = item_height;
	ftk_list_render_init(render, model);

	width  = ftk_widget_width(thiz);
	height = ftk_widget_height(thiz);

	margin = ftk_widget_height(thiz)%item_height;
	priv->visible_nr = ftk_widget_height(thiz)/item_height;
	return_val_if_fail(priv->visible_nr > 0, RET_FAIL);

	priv->top_margin = FTK_HALF(margin);
	priv->botton_margin = FTK_HALF(margin);
	priv->visible_start = 0;
	priv->current      = -1;
	priv->is_active = 0;
	priv->vscroll_bar = ftk_scroll_bar_create(thiz, width - FTK_SCROLL_BAR_WIDTH, priv->top_margin, 
		FTK_SCROLL_BAR_WIDTH, item_height * priv->visible_nr);
	ftk_scroll_bar_set_listener(priv->vscroll_bar, (FtkListener)ftk_list_view_on_scroll, thiz);

	return RET_OK;
}

int ftk_list_view_get_selected(FtkWidget* thiz)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(priv != NULL, -1);

	return priv->current;
}

FtkListModel* ftk_list_view_get_model(FtkWidget* thiz)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(priv != NULL, NULL);

	return priv->model;
}

Ret ftk_list_view_set_clicked_listener(FtkWidget* thiz, FtkListener listener, void* ctx)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(priv != NULL, RET_FAIL);

	priv->listener = listener;
	priv->listener_ctx = ctx;

	return RET_OK;
}

