/*
 * File: ftk_icon_view.h    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   icon view
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
 * 2009-12-04 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#ifndef FTK_ICON_VIEW_H
#define FTK_ICON_VIEW_H

#include "ftk_widget.h"

FTK_INHERITE_FROM(Widget)

typedef struct _FtkIconViewItem
{
	char text[10];
	FtkBitmap* icon;
	void* user_data;
}FtkIconViewItem;

#define FTK_ICON_VIEW_ITEM_MIN 32
#define FTK_ICON_VIEW_ITEM_MAX 128

FtkWidget* ftk_icon_view_create(FtkWidget* parent, int x, int y, int width, int height);
Ret ftk_icon_view_set_clicked_listener(FtkWidget* thiz, FtkListener listener);
Ret ftk_icon_view_set_item_size(FtkWidget* thiz, size_t size);

size_t ftk_icon_view_get_count(FtkWidget* thiz);
Ret ftk_icon_view_remove(FtkWidget* thiz, size_t index);
Ret ftk_icon_view_add(FtkWidget* thiz, const FtkIconViewItem* item);
Ret ftk_icon_view_get(FtkWidget* thiz, size_t index, const FtkIconViewItem** item);

#endif/*FTK_ICON_VIEW_H*/

