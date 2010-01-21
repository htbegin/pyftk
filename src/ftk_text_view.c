/*
 * File: ftk_text_view.c    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   multi line editor
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
 * 2009-12-31 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_log.h"
#include "ftk_util.h"
#include "ftk_text_view.h"
#include "ftk_globals.h"
#include "ftk_text_buffer.h"
#include "ftk_source_timer.h"

#define FTK_TEXT_VIEW_MAX_LINE 512
typedef struct _PrivInfo
{
	int   caret;
	int   caret_x;
	int   caret_y;
	int   caret_at_line;
	int   caret_visible;
	
	int   visible_start_line;
	int   visible_end_line;

	int   readonly;
	int   selected_start;
	int   selected_end;
	int   preedit_start;
	int   preedit_end;
	int   v_margin;
	int   total_lines;
	int   visible_lines;
	FtkSource* caret_timer;
	FtkTextBuffer* text_buffer;
	unsigned short line_offset[FTK_TEXT_VIEW_MAX_LINE];
}PrivInfo;

#define TEXT_VIEW_H_MARGIN 4
#define TEXT_VIEW_V_MARGIN  1
#define TEXT_VIEW_TOP_MARGIN  3
#define TB_TEXT priv->text_buffer->buffer
#define TB_LENGTH (int)(priv->text_buffer->length)
#define HAS_TEXT(priv) (priv != NULL && priv->text_buffer != NULL && TB_LENGTH > 0) 

static Ret ftk_text_view_on_paint_caret(FtkWidget* thiz);

static Ret ftk_text_view_update_caret(FtkWidget* thiz)
{
	int i = 0;
	DECL_PRIV0(thiz, priv);
	
	priv->caret = priv->caret < 0 ? 0 : priv->caret;
	priv->caret = priv->caret >  TB_LENGTH ? TB_LENGTH : priv->caret;

	for(i = 0; i < priv->total_lines; i++)
	{
		if(priv->caret >= priv->line_offset[i] && priv->caret < priv->line_offset[i+1])
		{
			priv->caret_at_line = i;
			break;
		}
	}

	if((priv->caret_at_line) < priv->visible_start_line)
	{
		priv->visible_start_line = priv->caret_at_line;
		priv->visible_end_line = FTK_MIN((priv->visible_start_line + priv->visible_lines), priv->total_lines);
	}
	else if((priv->caret_at_line) >= priv->visible_end_line)
	{
		priv->visible_end_line = priv->caret_at_line + 1;
		priv->visible_start_line = FTK_MAX(0, (priv->visible_end_line - priv->visible_lines));
	}

	ftk_widget_invalidate(thiz);

	return RET_OK;
}

static Ret ftk_text_view_move_caret(FtkWidget* thiz, int offset)
{
	int caret = 0;
	DECL_PRIV0(thiz, priv);
	
	if(!HAS_TEXT(priv))
	{
		priv->caret = 0;
		return RET_OK;
	}

	caret = priv->caret;
	priv->caret_visible = 0;
	ftk_text_view_on_paint_caret(thiz);
	priv->caret += ftk_text_buffer_chars_bytes(priv->text_buffer, priv->caret, offset);

	ftk_logd("%s: %d->%d\n", __func__, caret, priv->caret);
	return ftk_text_view_update_caret(thiz);
}

static Ret ftk_text_view_set_caret(FtkWidget* thiz, int caret)
{
	DECL_PRIV0(thiz, priv);
	
	if(!HAS_TEXT(priv))
	{
		priv->caret = 0;
		return RET_OK;
	}

	if(priv->total_lines <= 0)
	{
		priv->caret = caret;

		return RET_OK;
	}

	priv->caret_visible = 0;
	ftk_text_view_on_paint_caret(thiz);
	priv->caret = caret;

	return ftk_text_view_update_caret(thiz);
}

static Ret ftk_text_view_calc_lines(FtkWidget* thiz)
{
	int font_height = 0;
	DECL_PRIV0(thiz, priv);
	FTK_BEGIN_PAINT(x, y, width, height, canvas);
	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	font_height = ftk_canvas_font_height(canvas);

	(void)x;(void)y;(void)width;
	priv->visible_lines = (height - 2 * TEXT_VIEW_TOP_MARGIN) / (font_height + TEXT_VIEW_V_MARGIN);
	priv->v_margin = ((height - 2 * TEXT_VIEW_TOP_MARGIN) % (font_height + TEXT_VIEW_V_MARGIN))/2;

	return RET_OK;
}

static Ret ftk_text_view_relayout(FtkWidget* thiz, int start)
{
	int i = 0;
	int save_w = 0;
	int extent = 0;
	DECL_PRIV0(thiz, priv);
	const char* iter = NULL;
	const char* text = TB_TEXT;
	const char* prev_iter = NULL;

	unsigned short unicode = 0;
	FTK_BEGIN_PAINT(x, y, width, height, canvas);
	return_val_if_fail(thiz != NULL && canvas != NULL && text != NULL, RET_FAIL);

	(void)x;(void)y;(void)height;
	start = start < 0 ? 0 : start;
	start = start > FTK_TEXT_VIEW_MAX_LINE ? FTK_TEXT_VIEW_MAX_LINE : start;

	iter = text + priv->line_offset[start];
	for(i = start ; i < FTK_TEXT_VIEW_MAX_LINE; i++)
	{
		save_w = width;
		priv->line_offset[i] = iter - text;
		
		width -= 2 * TEXT_VIEW_H_MARGIN;
		while(width > 0)
		{
			prev_iter = iter;
			unicode = utf8_get_char(iter, &iter);
			if(unicode == 0 || unicode == 0xffff || unicode == '\n') 
			{
				break;
			}
			extent = ftk_canvas_get_char_extent(canvas, unicode);
			if(extent > width)
			{
				iter = prev_iter;
				break;
			}
			width -= extent;
		}

		width = save_w;
		
		if(unicode == 0 || unicode == 0xffff)
		{
			i++;
			priv->line_offset[i] = iter - text;
			break;
		}
	}

	priv->total_lines = i;
	ftk_text_view_calc_lines(thiz);
	priv->visible_end_line = FTK_MIN(priv->total_lines, priv->visible_start_line + priv->visible_lines);
	
	for(i = 0; i < priv->total_lines; i++)
	{
		if(priv->caret >= priv->line_offset[i] && priv->caret <= priv->line_offset[i+1])
		{
			priv->caret_at_line = i;
			break;
		}
	}

	ftk_text_view_update_caret(thiz);

	return RET_OK;
}

static Ret ftk_text_view_get_offset_by_pointer(FtkWidget* thiz, int px, int py)
{
	int dh = 0;
	int caret = 0;
	int start = 0;
	int index = 0;
	int font_height = 0;
	DECL_PRIV0(thiz, priv);
	const char* other_side = NULL;
	FTK_BEGIN_PAINT(x, y, width, height, canvas);

	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	font_height = ftk_canvas_font_height(canvas);
	
	dh = py - y - TEXT_VIEW_V_MARGIN - TEXT_VIEW_TOP_MARGIN;
	index = priv->visible_start_line + dh/(font_height + TEXT_VIEW_V_MARGIN);
	index = index < priv->visible_end_line ? index : priv->visible_end_line - 1;

	start = priv->line_offset[index];
	other_side = ftk_canvas_calc_str_visible_range(canvas, TB_TEXT, start, -1, px - x - TEXT_VIEW_H_MARGIN + 1);

	if((index + 1) < priv->total_lines)
	{
		caret = FTK_MIN((other_side - TB_TEXT), (priv->line_offset[index+1] - 1));
	}
	else
	{
		caret = other_side - TB_TEXT;
	}
	
	ftk_text_view_set_caret(thiz, caret);

	return 0;
}

static Ret ftk_text_view_handle_mouse_evevnt(FtkWidget* thiz, FtkEvent* event)
{
	return ftk_text_view_get_offset_by_pointer(thiz, event->u.mouse.x, event->u.mouse.y);
}

static Ret ftk_text_view_input_char(FtkWidget* thiz, char c)
{
	char str[2] = {0};
	DECL_PRIV0(thiz, priv);

	if(!priv->readonly)
	{
		str[0] = c;
		ftk_text_buffer_insert(priv->text_buffer, priv->caret, str);
		ftk_text_view_relayout(thiz, priv->caret_at_line);
		ftk_text_view_move_caret(thiz, 1);	
	}

	return RET_OK;
}

static Ret ftk_text_view_v_move_caret(FtkWidget* thiz, int offset)
{
	int caret = 0;
	int start = 0;
	int width = 0;
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);
	const char* other_side = NULL;
	FtkCanvas* canvas = ftk_widget_canvas(thiz);

	if(offset < 0)
	{
		ret = priv->caret_at_line > 0 ? RET_REMOVE: RET_OK;
	}
	else
	{
		ret = (priv->caret_at_line + 1) < priv->total_lines ? RET_REMOVE: RET_OK;
	}

	if(ret == RET_OK)
	{
		return ret;
	}

	priv->caret_at_line += offset;
	priv->caret_at_line = priv->caret_at_line < 0 ? 0 : priv->caret_at_line;
	priv->caret_at_line = priv->caret_at_line >= priv->total_lines ? priv->total_lines - 1 : priv->caret_at_line;

	start = priv->line_offset[priv->caret_at_line];

	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	width = priv->caret_x - TEXT_VIEW_H_MARGIN - FTK_PAINT_X(thiz) + 1;
	other_side = ftk_canvas_calc_str_visible_range(canvas, TB_TEXT, start, -1, width);
	if((priv->caret_at_line + 1) < priv->total_lines)
	{
		caret = FTK_MIN((other_side - TB_TEXT), (priv->line_offset[priv->caret_at_line+1] - 1));
	}
	else
	{
		caret = other_side - TB_TEXT;
	}

	ftk_text_view_set_caret(thiz, caret);

	return ret;
}

static Ret ftk_text_view_up_caret(FtkWidget* thiz)
{
	return ftk_text_view_v_move_caret(thiz, -1);
}

static Ret ftk_text_view_down_caret(FtkWidget* thiz)
{
	return ftk_text_view_v_move_caret(thiz, 1);
}

static Ret ftk_text_view_handle_key_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);

	switch(event->u.key.code)
	{
		case FTK_KEY_HOME:
		{
			ftk_text_view_set_caret(thiz, 0);
			break;
		}
		case FTK_KEY_END:
		{
			ftk_text_view_set_caret(thiz, TB_LENGTH);
			break;
		}
		case FTK_KEY_LEFT:
		{
			ftk_text_view_move_caret(thiz, -1);
			ret = RET_REMOVE;
			break;
		}
		case FTK_KEY_RIGHT:
		{
			ftk_text_view_move_caret(thiz, 1);
			ret = RET_REMOVE;
			break;
		}
		case FTK_KEY_UP:
		{
			ret = ftk_text_view_up_caret(thiz);	
			break;
		}
		case FTK_KEY_DOWN:
		{
			ret = ftk_text_view_down_caret(thiz);	
			break;
		}
		case FTK_KEY_DELETE:
		{
			if(priv->readonly) break;
			ftk_text_buffer_delete_chars(priv->text_buffer, priv->caret, 1);
			ftk_text_view_relayout(thiz, priv->caret_at_line);
			ftk_text_view_move_caret(thiz, 0);
			break;
		}
		case FTK_KEY_BACKSPACE:
		{
			int caret = priv->caret;
			if(priv->readonly) break;
			ftk_text_view_move_caret(thiz, -1);
			if(ftk_text_buffer_delete_chars(priv->text_buffer, caret, -1) == RET_OK)
			{
				ftk_text_view_relayout(thiz, priv->caret_at_line-1);
			}
			break;
		}
		default:
		{
			if(priv->readonly) break;
			if((event->u.key.code < 0xff && isprint(event->u.key.code)) 
				|| event->u.key.code == FTK_KEY_ENTER)
			{
				if(event->u.key.code == FTK_KEY_ENTER)
				{
					ftk_text_view_input_char(thiz, '\n');
				}
				else
				{
					ftk_text_view_input_char(thiz, event->u.key.code);
				}
				ftk_text_view_relayout(thiz, priv->caret_at_line);
			}
			break;
		}
	}

	return ret;
}

static Ret ftk_text_view_on_event(FtkWidget* thiz, FtkEvent* event)
{
	Ret ret = RET_OK;
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL && event != NULL, RET_FAIL);

	switch(event->type)
	{
		case FTK_EVT_FOCUS_IN:
		{
			ftk_source_ref(priv->caret_timer);
			ftk_main_loop_add_source(ftk_default_main_loop(), priv->caret_timer);
			break;
		}
		case FTK_EVT_FOCUS_OUT:
		{
			ftk_main_loop_remove_source(ftk_default_main_loop(), priv->caret_timer);
			break;
		}
		case FTK_EVT_KEY_DOWN:
		case FTK_EVT_KEY_UP:
		{
			if(event->type == FTK_EVT_KEY_DOWN)
			{
				ret = ftk_text_view_handle_key_event(thiz, event);
			}
			else
			{
				ret = event->u.key.code == FTK_KEY_LEFT || event->u.key.code == FTK_KEY_RIGHT 
					|| event->u.key.code == FTK_KEY_UP || event->u.key.code == FTK_KEY_DOWN
					? RET_REMOVE : RET_OK;
			}
			break;
		}
		case FTK_EVT_MOUSE_UP:
		{
			ret = ftk_text_view_handle_mouse_evevnt(thiz, event);
			break;
		}
		default:break;
	}

	return ret;
}

static Ret ftk_text_view_on_paint_caret(FtkWidget* thiz)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, RET_FAIL);

	if(ftk_widget_is_focused(thiz))
	{
		FtkGc gc = {0};
		int font_height = 0;
		FTK_BEGIN_PAINT(x, y, width, height, canvas);
		ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
		font_height = ftk_canvas_font_height(canvas);
		(void)x;(void)y;(void)width;(void)height;	
		
		gc.mask = FTK_GC_FG;
		gc.fg = priv->caret_visible ? ftk_widget_get_gc(thiz)->fg : ftk_widget_get_gc(thiz)->bg;
		ftk_canvas_reset_gc(canvas, &gc);
		ftk_canvas_draw_vline(canvas, priv->caret_x, priv->caret_y, font_height);
		priv->caret_visible = !priv->caret_visible;
		FTK_END_PAINT();
	}

	return RET_OK;
}

static Ret ftk_text_view_paint_border(FtkWidget* thiz, FtkCanvas* canvas, int x, int y, int width, int height)
{
	FtkGc gc = {0};
	gc.mask = FTK_GC_FG;
	gc.fg = ftk_theme_get_border_color(ftk_default_theme(), FTK_TEXT_VIEW, ftk_widget_state(thiz));
	ftk_canvas_set_gc(canvas, &gc);
	
	ftk_canvas_draw_hline(canvas, x + 2, y, width-4);
	ftk_canvas_draw_hline(canvas, x + 1, y + 1, width-2);
	ftk_canvas_draw_vline(canvas, x, y + 2, height - 4);
	ftk_canvas_draw_vline(canvas, x + 1, y + 1, height - 2);
	
	ftk_canvas_draw_vline(canvas, x+width-1, y + 2, height - 4);
	ftk_canvas_draw_vline(canvas, x + width -2, y + 1, height - 2);
	ftk_canvas_draw_hline(canvas, x + 1, y + height - 1, width-2);
	ftk_canvas_draw_hline(canvas, x + 2, y + height - 2, width-4);

	return RET_OK;
}

static Ret ftk_text_view_on_paint(FtkWidget* thiz)
{
	int dx = 0;
	int dy = 0;
	int font_height = 0;
	DECL_PRIV0(thiz, priv);
	FTK_BEGIN_PAINT(x, y, width, height, canvas);
	
	ftk_text_view_paint_border(thiz, canvas, x, y, width, height);

	if(priv->total_lines <= 0 && TB_LENGTH > 0)
	{
		ftk_text_view_relayout(thiz, 0);
	}

	ftk_canvas_set_gc(canvas, ftk_widget_get_gc(thiz));
	if(priv->text_buffer != NULL)
	{
		int i = 0;
		int len = 0;
		int start = 0;
		
		font_height = ftk_canvas_font_height(canvas);
		dy = y + priv->v_margin + TEXT_VIEW_TOP_MARGIN;
		dx = x + TEXT_VIEW_H_MARGIN;

		for(i = priv->visible_start_line; i < priv->visible_end_line; i++)
		{
			start = priv->line_offset[i];
			if((i + 1) < priv->total_lines)
			{
				len = priv->line_offset[i+1] - priv->line_offset[i];
			}
			else
			{
				len = TB_LENGTH - priv->line_offset[i];
			}

			if(priv->caret >= priv->line_offset[i] && priv->caret <= priv->line_offset[i+1])
			{
				priv->caret_at_line = i;
				priv->caret_y = dy + TEXT_VIEW_V_MARGIN;
				priv->caret_x = dx + ftk_canvas_get_extent(canvas, TB_TEXT + start, priv->caret - start) - 1;
			}
			
			if(len <= 0) 
			{
				break;
			}

			dy += TEXT_VIEW_V_MARGIN;
			ftk_canvas_draw_string_ex(canvas, dx, dy+font_height/2, TB_TEXT + start, len, 1);
			dy += font_height;
		}
	}
	else
	{
		priv->caret_x = TEXT_VIEW_H_MARGIN;
		priv->caret_y = TEXT_VIEW_V_MARGIN;
	}

	ftk_text_view_on_paint_caret(thiz);

	FTK_END_PAINT();
}

static void ftk_text_view_destroy(FtkWidget* thiz)
{
	if(thiz != NULL)
	{
		DECL_PRIV0(thiz, priv);
		
		ftk_source_disable(priv->caret_timer);
		ftk_main_loop_remove_source(ftk_default_main_loop(), priv->caret_timer);
		ftk_source_unref(priv->caret_timer);
		ftk_text_buffer_destroy(priv->text_buffer);
		FTK_FREE(priv);
	}

	return;
}

FtkWidget* ftk_text_view_create(FtkWidget* parent, int x, int y, int width, int height)
{
	FtkWidget* thiz = (FtkWidget*)FTK_ZALLOC(sizeof(FtkWidget));
	return_val_if_fail(thiz != NULL, NULL);

	thiz->priv_subclass[0] = (PrivInfo*)FTK_ZALLOC(sizeof(PrivInfo));
	if(thiz->priv_subclass[0] != NULL)
	{
		int min_height = 0;
		DECL_PRIV0(thiz, priv);

		thiz->on_event = ftk_text_view_on_event;
		thiz->on_paint = ftk_text_view_on_paint;
		thiz->destroy  = ftk_text_view_destroy;

		min_height = ftk_font_height(ftk_default_font()) + TEXT_VIEW_V_MARGIN * 2;
		height = height < min_height ? min_height : height;
		ftk_widget_init(thiz, FTK_TEXT_VIEW, 0);
		ftk_widget_move(thiz, x, y);
		ftk_widget_resize(thiz, width, height);

		priv->caret_timer = ftk_source_timer_create(500, (FtkTimer)ftk_text_view_on_paint_caret, thiz);
		priv->text_buffer = ftk_text_buffer_create(128);
		ftk_widget_append_child(parent, thiz);
	}
	else
	{
		FTK_FREE(thiz);
	}

	return thiz;
}

Ret ftk_text_view_set_text(FtkWidget* thiz, const char* text)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL && text != NULL, RET_FAIL);

	ftk_text_buffer_delete(priv->text_buffer, 0, TB_LENGTH);
	
	return ftk_text_view_insert_text(thiz, 0, text);
}

Ret ftk_text_view_insert_text(FtkWidget* thiz, size_t pos, const char* text)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL && text != NULL, RET_FAIL);

	pos = pos < TB_LENGTH ? pos : TB_LENGTH;
	ftk_text_buffer_insert(priv->text_buffer, pos, text);
	
	ftk_text_view_relayout(thiz, 0);
	ftk_text_view_set_caret(thiz, pos + strlen(text));

	return RET_OK;
}

const char* ftk_text_view_get_text(FtkWidget* thiz)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(thiz != NULL, NULL);

	return TB_TEXT;
}

Ret ftk_text_view_set_readonly(FtkWidget* thiz, int readonly)
{
	DECL_PRIV0(thiz, priv);
	return_val_if_fail(priv != NULL, RET_FAIL);

	priv->readonly = readonly;

	return RET_OK;
}
