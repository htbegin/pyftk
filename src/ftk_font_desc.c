/*
 * 
 * File: ftk_font_desc.c
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   font description.
 *
 * Copyright (c) 2009 - 2011  Li XianJing <xianjimli@hotmail.com>
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
 * 2011-03-20 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_util.h"
#include "ftk_font_desc.h"

struct _FtkFontDesc
{
	int ref;
	int size;
	int is_bold;
	int is_italic;
};

#define FONT_DESC_FMT "size:%d bold:%d italic:%d"

static Ret ftk_font_desc_parse(FtkFontDesc* thiz, const char* font_desc)
{
	const char* p = NULL;
	font_desc = font_desc != NULL ? font_desc : FTK_DEFAULT_FONT;

	p = strstr(font_desc, "size:");
	if(p != NULL)
	{
		thiz->size = ftk_atoi(p + 5);
	}

	p = strstr(font_desc, "bold:");
	if(p != NULL)
	{
		thiz->is_bold = ftk_atoi(p + 5);
	}

	p = strstr(font_desc, "italic:");
	if(p != NULL)
	{
		thiz->is_italic = ftk_atoi(p + 7);
	}

	return RET_OK;
}

FtkFontDesc* ftk_font_desc_create(const char* font_desc)
{
	FtkFontDesc* thiz = FTK_ZALLOC(sizeof(FtkFontDesc));

	if(thiz != NULL)
	{
		thiz->ref = 1;
		ftk_font_desc_parse(thiz, font_desc);
	}

	return thiz;
}

int ftk_font_desc_is_equal(FtkFontDesc* thiz, FtkFontDesc* other)
{
	return_val_if_fail(thiz != NULL && other != NULL, 0);

	return memcmp(thiz, other, sizeof(FtkFontDesc)) == 0;
}

int  ftk_font_desc_is_bold(FtkFontDesc* thiz)
{
	return_val_if_fail(thiz != NULL, 0);

	return thiz->is_bold;
}

int  ftk_font_desc_is_italic(FtkFontDesc* thiz)
{
	return_val_if_fail(thiz != NULL, 0);

	return thiz->is_italic;
}

int  ftk_font_desc_get_size(FtkFontDesc* thiz)
{
	return_val_if_fail(thiz != NULL, 0);

	return thiz->size;
}

Ret  ftk_font_desc_set_bold(FtkFontDesc* thiz, int bold)
{
	return_val_if_fail(thiz != NULL, RET_FAIL);

	thiz->is_bold = bold;
	
	return RET_OK;
}

Ret  ftk_font_desc_set_italic(FtkFontDesc* thiz, int italic)
{
	return_val_if_fail(thiz != NULL, 0);

	thiz->is_italic = italic;

	return RET_OK;
}

Ret  ftk_font_desc_set_size(FtkFontDesc* thiz, int size)
{
	return_val_if_fail(thiz != NULL, 0);

	thiz->size = size;

	return RET_OK;
}

Ret ftk_font_desc_get_string(FtkFontDesc* thiz, char* desc, size_t len)
{
	return_val_if_fail(thiz != NULL && desc != NULL, RET_FAIL);

	ftk_snprintf(desc, len, FONT_DESC_FMT, 
		thiz->size, thiz->is_bold, thiz->is_italic);

	return RET_OK;
}

static void ftk_font_desc_destroy(FtkFontDesc* thiz)
{
	if(thiz != NULL)
	{
		FTK_FREE(thiz);
	}

	return;
}

int ftk_font_desc_ref(FtkFontDesc* thiz)
{
	return_val_if_fail(thiz != NULL, 0);

	thiz->ref++;

	return thiz->ref;
}

int ftk_font_desc_unref(FtkFontDesc* thiz)
{
	int ret = 0;
	return_val_if_fail(thiz != NULL, 0);

	ret = --thiz->ref;

	if(ret == 0)
	{
		ftk_font_desc_destroy(thiz);
	}

	return ret;
}

