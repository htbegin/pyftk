/*
 * File: ftk_main_loop.c    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   main loop.
 *
 * Copyright (c) 2009 - 2010  Li XianJing <xianjimli@hotmail.com>
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
 * 2009-10-03 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_log.h"
#include "ftk_event.h"
#include "ftk_globals.h"
#include "ftk_main_loop.h"
#include "ftk_source_primary.h"

Ret ftk_main_loop_add_source(FtkMainLoop* thiz, FtkSource* source)
{
	FtkEvent event = {0};
	return_val_if_fail(thiz != NULL && source != NULL, RET_FAIL);

	event.type = FTK_EVT_ADD_SOURCE;
	event.u.extra = source;

	ftk_source_enable(source);
	return ftk_source_queue_event(ftk_primary_source(), &event);
}

Ret ftk_main_loop_remove_source(FtkMainLoop* thiz, FtkSource* source)
{
	FtkEvent event = {0};
	return_val_if_fail(thiz != NULL && source != NULL, RET_FAIL);

	event.type = FTK_EVT_REMOVE_SOURCE;
	event.u.extra = source;

	ftk_source_disable(source);
	return ftk_source_queue_event(ftk_primary_source(), &event);
}

