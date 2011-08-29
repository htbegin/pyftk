/*
 * File: ftk_canvas.c    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   default canvas implemntation.
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
 * 2009-10-03 Li XianJing <xianjimli@hotmail.com> created
 */

#include "ftk_log.h"
#include "ftk_util.h"
#include "ftk_bitmap.h"
#include "ftk_canvas.h"

#define PUT_PIXEL(pdst, color, alpha) \
	do\
	{\
		if(likely(alpha == 0xff))\
		{\
			*(unsigned int*)(pdst) = *(unsigned int*)(color);\
		}\
		else\
		{\
			FTK_ALPHA(color, pdst, alpha);\
		}\
	}while(0);

#define FTK_MAX_CLIP_REGION_NR 2

typedef struct _PrivInfo
{
	size_t w;
	size_t h;
	FtkColor* bits;
	FtkRegion* clip;
	FtkBitmap* bitmap;
	FtkRegion  clip_regions[FTK_MAX_CLIP_REGION_NR];
}PrivInfo;

#define FOR_EACH_CLIP(priv) \
	for(priv->clip = priv->clip_regions; priv->clip != NULL; priv->clip = priv->clip->next)

#define FTK_POINT_IN_RECT(xx, yy, r) ((xx >= r.x && xx < (r.x + r.width)) \
	&& (yy >= r.y && yy < (r.y + r.height)))

static Ret ftk_rect_and(const FtkRect *r1, const FtkRect *r2, FtkRect *r)
{
	return_val_if_fail(r1 != NULL, RET_FAIL);
	return_val_if_fail(r2 != NULL, RET_FAIL);
	return_val_if_fail(r != NULL, RET_FAIL);

	Ret ret = RET_FAIL;
	int x = FTK_MAX(r1->x, r2->x);
	int y = FTK_MAX(r1->y, r2->y);
	int width = FTK_MIN(r1->x + r1->width, r2->x + r2->width) - x;
	int height = FTK_MIN(r1->y + r1->height, r2->y + r2->height) - y;

	// the horizontal range is [x, x + width), so width == 0 is still invalid
	// the vertical range is [y, y + height), so height == 0 is still invalid
	if(width > 0 && height > 0)
	{
		r->x = x;
		r->y = y;
		r->width = width;
		r->height = height;
		ret = RET_OK;
	}

	return ret;
}

static Ret ftk_canvas_default_sync_gc(FtkCanvas* thiz)
{
	return RET_OK;
}

static Ret ftk_canvas_default_set_clip(FtkCanvas* thiz, FtkRegion* clip)
{
	size_t i = 0;
	DECL_PRIV(thiz, priv);
	FtkRegion* iter = NULL;
	
	if(clip != NULL)
	{
		for(i = 0, iter = clip; i < FTK_MAX_CLIP_REGION_NR && iter != NULL; i++, iter = iter->next)
		{
			FtkRect* r = &(priv->clip_regions[i].rect);
			priv->clip_regions[i] = *iter;

			r->x = r->x < 0 ? 0 : r->x;
			r->y = r->y < 0 ? 0 : r->y;
			r->width = r->width < priv->w ? r->width : priv->w;
			r->height = r->height < priv->h ? r->height : priv->h;

			ftk_logi("%s: add clip %d,%d@%dx%d\n", __func__, r->x, r->y, r->width, r->height);

			priv->clip_regions[i].next = NULL;
			if(i > 0)
			{
				priv->clip_regions[i - 1].next = priv->clip_regions+i;
			}
		}
	}
	else
	{
		priv->clip_regions[0].rect.x = 0;
		priv->clip_regions[0].rect.y = 0;
		priv->clip_regions[0].rect.width = priv->w;
		priv->clip_regions[0].rect.height = priv->h;
		priv->clip_regions[0].next = NULL;
	}

#if 0
	for(iter = priv->clip_regions; iter != NULL; iter = iter->next)
	{
		ftk_logd("%s:%d clip(%d %d %d %d)\n", __func__, __LINE__, 
			iter->rect.x, iter->rect.y, iter->rect.width, iter->rect.height);
	}
#endif
	return RET_OK;
}

static Ret ftk_canvas_default_draw_pixels(FtkCanvas* thiz, FtkPoint* points, size_t nr)
{
	size_t x = 0;
	size_t y = 0;
	size_t i = 0;
	DECL_PRIV(thiz, priv);
	FtkColor* pdst = NULL;
	FtkColor* color = &(thiz->gc.fg);
	FtkRect clip = priv->clip->rect;
	unsigned char alpha = thiz->gc.mask & FTK_GC_ALPHA ? thiz->gc.alpha :  thiz->gc.fg.a;

	for(i = 0; i < nr; i++)
	{
		x = points[i].x;
		y = points[i].y;
		if(FTK_POINT_IN_RECT(x, y, clip))
		{
			pdst = priv->bits + y * priv->w + x;
			PUT_PIXEL(pdst, color, alpha);
		}
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_vline(FtkCanvas* thiz, size_t x, size_t y, size_t h)
{
	int i = 0;
	size_t width = 0;
	size_t height = 0;
	FtkColor* bits = NULL;
	unsigned char alpha = 0;
	FtkColor* pdst = NULL;
	FtkColor* color = NULL;
	DECL_PRIV(thiz, priv);	
	width  = priv->w;
	height = priv->h;
	bits   = priv->bits;
	return_val_if_fail(bits != NULL && y < height, RET_FAIL);
	alpha = thiz->gc.mask & FTK_GC_ALPHA ? thiz->gc.alpha :  thiz->gc.fg.a;

	x = x < 0 ? 0 : x;
	y = y < 0 ? 0 : y;
	h = (y + h) < height ? h : (height - y);

	pdst = bits + width * y + x;
	color = &(thiz->gc.fg);
	
	for(i = h; i > 0; i--, pdst+=width)
	{
		PUT_PIXEL(pdst, color, alpha);
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_hline(FtkCanvas* thiz, size_t x, size_t y, size_t w)
{
	int i = 0;
	size_t width = 0;
	size_t height = 0;
	FtkColor* bits = NULL;
	unsigned char alpha = 0;
	FtkColor* pdst = NULL;
	FtkColor* color = NULL;	
	DECL_PRIV(thiz, priv);	
	width  = priv->w;
	height = priv->h;
	bits   = priv->bits;
	return_val_if_fail(bits != NULL && x < width, RET_FAIL);
	return_val_if_fail(y < height, RET_FAIL);	
	alpha = thiz->gc.mask & FTK_GC_ALPHA ? thiz->gc.alpha :  thiz->gc.fg.a;

	x = x < 0 ? 0 : x;
	y = y < 0 ? 0 : y;
	w = (x + w) < width ? w : width - x;
	color = &(thiz->gc.fg);
	pdst = bits + y * width + x;
	
	for(i = w; i > 0; i--, pdst++)
	{
		PUT_PIXEL(pdst, color, alpha);
	}

	return RET_OK;
}

/*FROM: http://blog.csdn.net/zwh37333/article/details/2507661*/
#define swap_int(a, b) {v = a; a = b; b = v;}
static Ret ftk_canvas_default_draw_normal_line(FtkCanvas* thiz, int x1, int y1, int x2, int y2)
{  
	int v = 0;
	int x = 0;
	int y = 0;
	int dx = abs(x2 - x1);  
	int dy = abs(y2 - y1);  
	int direction = 0;  
	int inc_x = 0;  
	int inc_y = 0;  
	int cur_x = x1;  
	int cur_y = y1;  
	int two_dy = 0;  
	int two_dy_dx = 0;  
	int init_d = 0;	
	DECL_PRIV(thiz, priv);
	FtkColor* pdst = NULL;
	FtkColor* color = &(thiz->gc.fg);
	unsigned char alpha = thiz->gc.mask & FTK_GC_ALPHA ? thiz->gc.alpha :  thiz->gc.fg.a;

	if (dx < dy)	
	{  
		// y direction is step direction	
		swap_int(x1, y1);  
		swap_int(dx, dy);  
		swap_int(x2, y2);    
		direction = 1;  
	}  
  
	// calculate the x, y increment  
	inc_x = (x2 - x1) > 0  ? 1 : -1;  
	inc_y = (y2 - y1) > 0  ? 1 : -1;  
  
	cur_x = x1;  
	cur_y = y1;  
	two_dy = 2 * dy;  
	two_dy_dx = 2 * (dy - dx);  
	init_d = 2 * dy - dx;	

	while (cur_x !=  x2)  // cur_x == x2 can not use in bitmap   
	{  
		if(init_d < 0)  
		{  
			init_d += two_dy;	
		}  
		else  
		{  
			cur_y += inc_y;  
			init_d += two_dy_dx;	
		}  
		if (direction)  
		{  
			x = cur_y;
			y = cur_x;
		}  
		else  
		{  
			x = cur_x;
			y = cur_y;
		}  
		pdst = priv->bits + y * priv->w + x;
		PUT_PIXEL(pdst, color, alpha);

		cur_x += inc_x;  
	} 

	return RET_OK;  
}  

static Ret ftk_canvas_default_draw_line(FtkCanvas* thiz, size_t x1, size_t y1, size_t x2, size_t y2)
{
	size_t len = 0;
	size_t min = 0;
	size_t max = 0;
	Ret ret = RET_FAIL;
	DECL_PRIV(thiz, priv);
	FtkRect clip = priv->clip->rect;

	if(!FTK_POINT_IN_RECT(x1, y1, clip) && !FTK_POINT_IN_RECT(x2, y2, clip))
	{
		return RET_OK;
	}

	if(x1 == x2 && y1 == y2)
	{
		FtkPoint p = {0};
		p.x = x1;
		p.y = y1;

		return ftk_canvas_default_draw_pixels(thiz, &p, 1);
	}

	if(x1 == x2)
	{
		min = FTK_MIN(y1, y2);
		max = FTK_MAX(y1, y2);

		if(FTK_POINT_IN_RECT(x1, min, clip))
		{
			if(!FTK_POINT_IN_RECT(x1, max, clip))
			{
				max = clip.y + clip.height;		
			}
		}
		else
		{
			min = clip.y;
		}

		len = max - min;
		ret = ftk_canvas_default_draw_vline(thiz, x1, min, len);
	}
	else if(y1 == y2)
	{
		min = FTK_MIN(x1, x2);
		max = FTK_MAX(x1, x2);
		
		if(FTK_POINT_IN_RECT(min, y1, clip))
		{
			if(!FTK_POINT_IN_RECT(max, y1, clip))
			{
				max = clip.x + clip.width;
			}
		}
		else
		{
			min = clip.x;
		}

		len = max - min;
		ret = ftk_canvas_default_draw_hline(thiz, min, y1, len);
	}
	else
	{
		ret = ftk_canvas_default_draw_normal_line(thiz, x1, y1, x2, y2);
	}

	return ret;
}

static Ret ftk_canvas_default_clear_rect(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h)
{
	size_t width = 0;
	int iter_w = 0;
	int iter_h = 0;
	FtkColor* color = NULL;
	FtkColor* bits = NULL;
	FtkColor* pdst = NULL;
	DECL_PRIV(thiz, priv);	
	
	FtkRect rect = {0};
	rect.x = x;
	rect.y = y;
	rect.width = w;
	rect.height = h;

	ftk_logi("%s: clear rect %d,%d@%dx%d\n", __func__, rect.x, rect.y, rect.width, rect.height);
	ftk_logi("%s: clip rect %d,%d@%dx%d\n", __func__,
			priv->clip->rect.x, priv->clip->rect.y,
			priv->clip->rect.width, priv->clip->rect.height);

	if (ftk_rect_and(&rect, &priv->clip->rect, &rect) != RET_OK)
	{
//		ftk_logd("%s: skip.\n", __func__);
		return RET_OK;
	}

	ftk_logi("%s: ANDed-clear rect %d,%d@%dx%d\n", __func__, rect.x, rect.y, rect.width, rect.height);

	width = priv->w;
	bits = priv->bits;

	x = rect.x;
	y = rect.y;
	w = rect.width;
	h = rect.height;

	iter_w = w;
	iter_h = h;
	bits += y * width;

	color = &(thiz->gc.fg);
	while(iter_h--)
	{
		pdst = bits + x;
		while(iter_w--)
		{
			*(unsigned int*)pdst = *(unsigned int*)color;
			pdst++;
		}
		iter_w = w;
		bits += width;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_rect_impl(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h, int fill)
{
	int i = 0;
	size_t width  = 0;
	size_t height = 0;
	DECL_PRIV(thiz, priv);
	width  = priv->w;
	height = priv->h;
	return_val_if_fail(x < width && y < height, RET_FAIL);

	if(fill)
	{
		for(i = 0; i < h; i++)
		{
			if((y + i) < height)
			{
				ftk_canvas_default_draw_hline(thiz, x, (y+i), w);	
			}
		}
	}
	else
	{
		ftk_canvas_default_draw_hline(thiz, x,   y, w);		
		ftk_canvas_default_draw_hline(thiz, x,   y+h-1, w);		
		ftk_canvas_default_draw_vline(thiz, x,   y, h);		
		ftk_canvas_default_draw_vline(thiz, x+w-1, y, h);		
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_round_rect(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h, int fill)
{
	size_t width  = 0;
	size_t height = 0;
	DECL_PRIV(thiz, priv);

	width  = priv->w;
	height = priv->h;
	return_val_if_fail(x < width && y < height, RET_FAIL);
	return_val_if_fail(w > 8 && h > 8, RET_FAIL);

	ftk_canvas_default_draw_hline(thiz, x + 2, y, w-4);
	ftk_canvas_default_draw_hline(thiz, x + 1, y + 1, w-2);
	ftk_canvas_default_draw_vline(thiz, x, y + 2, h - 4);
	ftk_canvas_default_draw_vline(thiz, x + 1, y + 1, h - 2);

	ftk_canvas_default_draw_vline(thiz, x+w-1, y + 2, h - 4);
	ftk_canvas_default_draw_vline(thiz, x + w -2, y + 1, h - 2);
	ftk_canvas_default_draw_hline(thiz, x + 1, y + h - 1, w-2);
	ftk_canvas_default_draw_hline(thiz, x + 2, y + h - 2, w-4);

	if(fill)
	{
		ftk_canvas_default_draw_rect_impl(thiz, x + 2, y + 2, w - 4, h - 4, fill);
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_rect(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h, 
	int round, int fill)
{
	Ret ret = RET_FAIL;
	FtkRect rect = {0};
	DECL_PRIV(thiz, priv);
	rect.x = x;
	rect.y = y;
	rect.width = w;
	rect.height = h;

	if(ftk_rect_and(&rect, &priv->clip->rect, &rect) != RET_OK)
	{
//		ftk_logd("%s: skip.\n", __func__);
		return RET_OK;
	}

	x = rect.x;
	y = rect.y;
	w = rect.width;
	h = rect.height;

	if(round)
	{
		ret = ftk_canvas_default_draw_round_rect(thiz, x, y, w, h, fill);
	}
	else
	{
		ret = ftk_canvas_default_draw_rect_impl(thiz, x, y, w, h, fill);
	}

	return ret;
}

static Ret ftk_canvas_default_draw_bitmap_normal(FtkCanvas* thiz, FtkBitmap* bitmap, FtkRect* s, FtkRect* d)
{
	int i = 0;
	int j = 0;
	int k = 0;
	size_t x = s->x;
	size_t y = s->y;
	size_t w = s->width;
	size_t h = s->height;
	size_t xoffset = d->x;
	size_t yoffset = d->y;
	FtkColor* src = NULL;
	FtkColor* dst = NULL;
	FtkColor* psrc = NULL;
	FtkColor* pdst = NULL;
	unsigned char alpha = 0;
	DECL_PRIV(thiz, priv);
	size_t width  = priv->w;
	size_t height = priv->h;
	int bitmap_width   = ftk_bitmap_width(bitmap);
	int bitmap_height  = ftk_bitmap_height(bitmap);

	return_val_if_fail(thiz != NULL && bitmap != NULL, RET_FAIL);
	return_val_if_fail(x < bitmap_width, RET_FAIL);
	return_val_if_fail(y < bitmap_height, RET_FAIL);
	return_val_if_fail(xoffset < width, RET_FAIL);
	return_val_if_fail(yoffset < height, RET_FAIL);

	src = ftk_bitmap_bits(bitmap);
	dst = priv->bits;

	w = (x + w) < bitmap_width  ? w : bitmap_width - x;
	w = (xoffset + w) < width  ? w : width  - xoffset;
	h = (y + h) < bitmap_height ? h : bitmap_height - y;
	h = (yoffset + h) < height ? h : height - yoffset;
	
	w += x;
	h += y;

	src += y * bitmap_width;
	dst += yoffset * width;

	if(thiz->gc.mask & FTK_GC_ALPHA)
	{
		for(i = y; i < h; i++)
		{
			for(j = x, k = xoffset; j < w; j++, k++)
			{
				pdst = dst+k;
				psrc = src+j;
				alpha = (psrc->a * thiz->gc.alpha) >> 8;
				PUT_PIXEL(pdst, psrc, alpha);
			}
			src += bitmap_width;
			dst += width;
		}
	}
	else
	{
		for(i = y; i < h; i++)
		{
			for(j = x, k = xoffset; j < w; j++, k++)
			{
				pdst = dst+k;
				psrc = src+j;
				alpha = psrc->a;

				PUT_PIXEL(pdst, psrc, alpha);
			}
			src += bitmap_width;
			dst += width;
		}
	}

	return RET_OK;
}

static Ret ftk_canvas_draw_bitmap_resize(FtkCanvas* thiz, FtkBitmap* src_i, FtkRect* src_r, FtkRect* dst_r)
{
	FtkColor* s = NULL;
	FtkColor* d = NULL;
	FtkColor* src = NULL;
	FtkColor* dst = NULL;
	FtkColor* psrc = NULL;
	FtkColor* pdst = NULL;
	DECL_PRIV(thiz, priv);
	FtkBitmap* dst_i = priv->bitmap;	
	int i=0, j=0, m=0, n=0;
	int dst_i_w = ftk_bitmap_width(dst_i); 
	int dst_i_h = ftk_bitmap_height(dst_i);
	int src_i_w = ftk_bitmap_width(src_i);
	int src_i_h = ftk_bitmap_height(src_i);

	int dst_x = dst_r->x;
	int dst_y = dst_r->y;
	int dst_w = dst_r->width;
	int dst_h = dst_r->height;

	int src_x = src_r->x;
	int src_y = src_r->y;
	int src_w = src_r->width;
	int src_h = src_r->height;

	int scale_w = (src_w << 8)/dst_w;
	int scale_h = (src_h << 8)/dst_h;

	return_val_if_fail(dst_i != NULL && ftk_bitmap_bits(dst_i) != NULL && dst_r != NULL, RET_FAIL);
	return_val_if_fail(src_i != NULL && ftk_bitmap_bits(src_i) != NULL && src_r != NULL, RET_FAIL);
	
	return_val_if_fail(dst_x >= 0 && dst_w > 0 && (dst_x + dst_w) <= dst_i_w, RET_FAIL);
	return_val_if_fail(dst_y >= 0 && dst_h > 0 && (dst_y + dst_h) <= dst_i_h, RET_FAIL);
	
	return_val_if_fail(src_x >= 0 && src_w > 0 && (src_x + src_w) <= src_i_w, RET_FAIL);
	return_val_if_fail(src_y >= 0 && src_h > 0 && (src_y + src_h) <= src_i_h, RET_FAIL);
	
	src = ftk_bitmap_bits(src_i) + src_y * src_i_w + src_x;
	dst = ftk_bitmap_bits(dst_i) + dst_y * dst_i_w + dst_x;
        
	if(thiz->gc.mask & FTK_GC_ALPHA)
	{
		int alpha = thiz->gc.alpha; 
		for(j=0; j<dst_h; j++)
		{
			n = (j*scale_h) >> 8;
			pdst = dst + j * dst_i_w;
			psrc = src + n * src_i_w;

			for(i=0 ; i<dst_w ; i++)
			{
				m = (i*scale_w) >> 8;
				d = pdst+i;
				s = psrc+m;
				PUT_PIXEL(d, s, alpha);
			}	
		}
	}
	else
	{
		for(j=0; j<dst_h; j++)
		{
			n = (j*scale_h) >> 8;
			pdst = dst + j * dst_i_w;
			psrc = src + n * src_i_w;

			for(i=0 ; i<dst_w ; i++)
			{
				m = (i*scale_w) >> 8;
				d = pdst+i;
				s = psrc+m;

				PUT_PIXEL(d, s, s->a);
			}	
		}
	}

	return 	RET_OK;
}

static Ret ftk_canvas_default_draw_bitmap(FtkCanvas* thiz, FtkBitmap* bitmap, 
	FtkRect* src_r, FtkRect* dst_r, int alpha)
{
	Ret ret = RET_FAIL;
	FtkRect rect = *dst_r;
	DECL_PRIV(thiz, priv);
	return_val_if_fail(thiz != NULL && bitmap != NULL && dst_r != NULL && src_r != NULL, RET_FAIL);

	if(ftk_rect_and(&rect, &priv->clip->rect, &rect) != RET_OK)
	{
//		ftk_logd("%s: skip.\n", __func__);
		return RET_OK;
	}

	if(alpha == 0)
	{
		return RET_OK;
	}
	else if(alpha == 0xff)
	{
		thiz->gc.alpha = 0xff;
		thiz->gc.mask = thiz->gc.mask & (~FTK_GC_ALPHA);
	}
	else
	{
		FtkGc gc;
		gc.mask = FTK_GC_ALPHA;
		gc.alpha = alpha;
		ftk_canvas_set_gc(thiz, &gc);
	}

	if(dst_r->width == src_r->width && dst_r->height == src_r->height)
	{
#if 0
		/*TODO*/
		src_r->x = src_r->x + (rect.x - dst_r->x);
		src_r->y = src_r->y + (rect.y - dst_r->y);
		
		*dst_r = rect;
		src_r->width = dst_r->width;
		src_r->height = dst_r->height;
#endif
		ret = ftk_canvas_default_draw_bitmap_normal(thiz, bitmap, src_r, dst_r);
	}
	else
	{
#if 1	
		int scale_w = (src_r->width << 8)/dst_r->width;
		int scale_h = (src_r->height << 8)/dst_r->height;

		src_r->x = src_r->x + (((rect.x - dst_r->x) * scale_w) >> 8);
		src_r->y = src_r->y + (((rect.y - dst_r->y) * scale_h) >> 8);
		
		*dst_r = rect;
		src_r->width = (dst_r->width * scale_w) >> 8;
		src_r->height = (dst_r->height * scale_h) >> 8;
#endif		
		ret = ftk_canvas_draw_bitmap_resize(thiz, bitmap, src_r, dst_r);
	}

	return ret;
}

static Ret ftk_canvas_default_draw_boxed_string(FtkCanvas* thiz, size_t x, size_t y,
	const FtkRect* box, const char* str, int len, int vcenter)
{
	int i = 0;
	int j = 0;
	size_t ox = x;
	size_t oy = y;
	size_t right = 0;
	size_t bottom = 0;
	unsigned char data = 0;
	int vcenter_offset = 0;
	FtkGlyph glyph = {0};
	FtkColor color = {0};
	FtkColor fg = {0};
	FtkColor bg = {0};
	FtkColor* bits = NULL;
	unsigned short code = 0;
	const char* iter = str;
	DECL_PRIV(thiz, priv);
	FtkRect clip = {0};

	if(ftk_rect_and(box, &priv->clip->rect, &clip) != RET_OK)
	{
		ftk_logi("%s: no intersection between %d,%d@%dx%d and %d,%d@%dx%d\n",
			__func__,
			box->x, box->y, box->width, box->height,
			priv->clip->rect.x, priv->clip->rect.y, priv->clip->rect.width, priv->clip->rect.height);
		return RET_OK;
	}

	ftk_logi("%s: %d,%d@%dx%d AND %d,%d@%dx%d = %d,%d@%dx%d\n",
			__func__,
			box->x, box->y, box->width, box->height,
			priv->clip->rect.x, priv->clip->rect.y, priv->clip->rect.width, priv->clip->rect.height,
			clip.x, clip.y, clip.width, clip.height);

	bits   = priv->bits;
	right = clip.x + clip.width;
	bottom = clip.y + clip.height;

	color.a = 0xff;
	fg = thiz->gc.fg;

	/*FIXME: vcenter_offset maybe not correct.*/
	vcenter_offset = ftk_font_height(thiz->gc.font)/3;
	while(*iter && (iter - str) < len)
	{
		size_t offset = 0;
		code = utf8_get_char(iter, &iter);

		if(code == ' ' )
		{
			x += FTK_SPACE_WIDTH;
			ox = x;
			continue;
		}
		else if(code == '\t')
		{
			x += FTK_TAB_WIDTH * FTK_SPACE_WIDTH;
			ox = x;
			continue;
		}

		if(code == 0xffff || code == 0) break;
		if(code == '\r' || code == '\n' || ftk_font_lookup(thiz->gc.font, code, &glyph) != RET_OK) 
			continue;
		glyph.y = vcenter ? glyph.y - vcenter_offset : glyph.y;
		if((x + glyph.x + glyph.w) >= right) {
			ftk_logi("%d too right\n", code);
			break;
		}
		if((y - glyph.y + glyph.h) >= bottom) {
			ftk_logi("%d too bottom\n", code);
			ftk_logi("glyph.x %d, glyph.y %d, glyph.w %d, glyph.h %d\n",
					glyph.x, glyph.y, glyph.w, glyph.h);
			break;
		}

		x = x + glyph.x;
		y = y - glyph.y;
		for(i = 0; i < glyph.h; i++,y++)
		{
			for(j = 0, x= ox; j < glyph.w; j++,x++)
			{
				if(!FTK_POINT_IN_RECT(x, y, clip))
				{
					ftk_logi("(%d, %d) of %d out of clip\n", x, y, code);
					break;
				}
				data = glyph.data[i * glyph.w + j];
				offset = y * priv->w + x;
				bg = bits[offset];
				if(data)
				{
					color.r = FTK_ALPHA_1(fg.r, bg.r, data);
					color.g = FTK_ALPHA_1(fg.g, bg.g, data);
					color.b = FTK_ALPHA_1(fg.b, bg.b, data);
					*(unsigned int*)(bits+offset) = *(unsigned int*)&color;
				}
			}
		}

		y = oy;
		x = ox + glyph.x + glyph.w + 1;
		ox = x;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_string(FtkCanvas* thiz, size_t x, size_t y,
	const char* str, int len, int vcenter)
{
	int i = 0;
	int j = 0;
	size_t ox = x;
	size_t oy = y;
	size_t right = 0;
	size_t bottom = 0;
	unsigned char data = 0;
	int vcenter_offset = 0;
	FtkGlyph glyph = {0};
	FtkColor color = {0};
	FtkColor fg = {0};
	FtkColor bg = {0};
	FtkColor* bits = NULL;
	unsigned short code = 0;
	const char* iter = str;
	DECL_PRIV(thiz, priv);
	FtkRect clip = priv->clip->rect;

	ftk_logi("string clip: %d,%d@%dx%d\n",
			clip.x, clip.y, clip.width, clip.height);

	bits   = priv->bits;
	right = clip.x + clip.width;
	bottom = clip.y + clip.height;

	color.a = 0xff;
	fg = thiz->gc.fg;

	/*FIXME: vcenter_offset maybe not correct.*/
	vcenter_offset = ftk_font_height(thiz->gc.font)/3;
	while(*iter && (iter - str) < len)
	{
		size_t offset = 0;
		code = utf8_get_char(iter, &iter);

		if(code == ' ' )
		{
			x += FTK_SPACE_WIDTH;
			ox = x;
			continue;
		}
		else if(code == '\t')
		{
			x += FTK_TAB_WIDTH * FTK_SPACE_WIDTH;
			ox = x;
			continue;
		}

		if(code == 0xffff || code == 0) break;
		if(code == '\r' || code == '\n' || ftk_font_lookup(thiz->gc.font, code, &glyph) != RET_OK) 
			continue;
		glyph.y = vcenter ? glyph.y - vcenter_offset : glyph.y;
		if((x + glyph.x + glyph.w) >= right) {
			ftk_logi("%d too right\n", code);
			break;
		}
		if((y - glyph.y + glyph.h) >= bottom) {
			ftk_logi("%d too bottom\n", code);
			ftk_logi("glyph.x %d, glyph.y %d, glyph.w %d, glyph.h %d\n",
					glyph.x, glyph.y, glyph.w, glyph.h);
			break;
		}

		x = x + glyph.x;
		y = y - glyph.y;
		for(i = 0; i < glyph.h; i++,y++)
		{
			for(j = 0, x= ox; j < glyph.w; j++,x++)
			{
				if(!FTK_POINT_IN_RECT(x, y, clip))
				{
					ftk_logi("(%d, %d) of %d out of clip\n", x, y, code);
					break;
				}
				data = glyph.data[i * glyph.w + j];
				offset = y * priv->w + x;
				bg = bits[offset];
				if(data)
				{
					color.r = FTK_ALPHA_1(fg.r, bg.r, data);
					color.g = FTK_ALPHA_1(fg.g, bg.g, data);
					color.b = FTK_ALPHA_1(fg.b, bg.b, data);
					*(unsigned int*)(bits+offset) = *(unsigned int*)&color;
				}
			}
		}

		y = oy;
		x = ox + glyph.x + glyph.w + 1;
		ox = x;
	}

	return RET_OK;
}

static Ret fk_canvas_default_lock_buffer(FtkCanvas* thiz, FtkBitmap** bitmap)
{
	DECL_PRIV(thiz, priv);
	return_val_if_fail(bitmap != NULL, RET_FAIL);

	*bitmap = priv->bitmap;

	return RET_OK;
}

static Ret ftk_canvas_default_unlock_buffer(FtkCanvas* thiz)
{
	return RET_OK;
}

static void ftk_canvas_default_destroy(FtkCanvas* thiz)
{
	DECL_PRIV(thiz, priv);
	ftk_bitmap_unref(priv->bitmap);
	FTK_FREE(thiz);

	return;
}

static Ret ftk_canvas_default_draw_pixels_clip(FtkCanvas* thiz, FtkPoint* points, size_t nr) 
{
	DECL_PRIV(thiz, priv);
	return_val_if_fail(points != NULL, RET_FAIL);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_pixels(thiz, points, nr);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_line_clip(FtkCanvas* thiz, size_t x1, size_t y1, size_t x2, size_t y2)
{
	DECL_PRIV(thiz, priv);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_line(thiz, x1, y1, x2, y2);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_clear_rect_clip(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h)
{
	DECL_PRIV(thiz, priv);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_clear_rect(thiz, x, y, w, h);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_rect_clip(FtkCanvas* thiz, size_t x, size_t y, size_t w, size_t h, 
	int round, int fill)
{
	DECL_PRIV(thiz, priv);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_rect(thiz, x, y, w, h, round, fill);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_bitmap_clip(FtkCanvas* thiz, FtkBitmap* bitmap, 
	FtkRect* src_r, FtkRect* dst_r, int alpha)
{
	DECL_PRIV(thiz, priv);
	return_val_if_fail(bitmap != NULL && src_r != NULL && dst_r != NULL, RET_FAIL);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_bitmap(thiz, bitmap, src_r, dst_r, alpha);
		if(priv->clip == NULL) break;
	}

	return RET_OK;

}

static Ret ftk_canvas_default_draw_boxed_string_clip(FtkCanvas* thiz, size_t x, size_t y,
	const FtkRect* box, const char* str, int len, int vcenter)
{
	DECL_PRIV(thiz, priv);
	return_val_if_fail(str != NULL, RET_FAIL);
	len = len >= 0 ? len : (int)strlen(str);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_boxed_string(thiz, x, y, box, str, len, vcenter);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

static Ret ftk_canvas_default_draw_string_clip(FtkCanvas* thiz, size_t x, size_t y,
	const char* str, int len, int vcenter)
{
	DECL_PRIV(thiz, priv);
	return_val_if_fail(str != NULL, RET_FAIL);
	len = len >= 0 ? len : (int)strlen(str);

	FOR_EACH_CLIP(priv)
	{
		ftk_canvas_default_draw_string(thiz, x, y, str, len, vcenter);
		if(priv->clip == NULL) break;
	}

	return RET_OK;
}

FtkCanvas* ftk_canvas_create(size_t w, size_t h, FtkColor* clear_color)
{
	FtkCanvas* thiz = NULL;
	return_val_if_fail(w > 0 && h > 0 && clear_color != NULL, NULL);

	if((thiz = FTK_NEW_PRIV(FtkCanvas)) != NULL)
	{
		DECL_PRIV(thiz, priv);

		thiz->sync_gc = ftk_canvas_default_sync_gc;
		thiz->set_clip = ftk_canvas_default_set_clip;
		thiz->draw_pixels = ftk_canvas_default_draw_pixels_clip;
		thiz->draw_line = ftk_canvas_default_draw_line_clip;
		thiz->draw_rect = ftk_canvas_default_draw_rect_clip;
		thiz->clear_rect = ftk_canvas_default_clear_rect_clip;
		thiz->draw_bitmap = ftk_canvas_default_draw_bitmap_clip;
		thiz->draw_string = ftk_canvas_default_draw_string_clip;
		thiz->draw_boxed_string = ftk_canvas_default_draw_boxed_string_clip;
		thiz->lock_buffer = fk_canvas_default_lock_buffer;
		thiz->unlock_buffer = ftk_canvas_default_unlock_buffer;
		thiz->destroy = ftk_canvas_default_destroy;

		thiz->gc.bg = *clear_color;
		thiz->gc.fg.a = 0xff;
		thiz->gc.fg.r = 0xff - clear_color->r;
		thiz->gc.fg.g = 0xff - clear_color->g;
		thiz->gc.fg.b = 0xff - clear_color->b;
		thiz->gc.mask = FTK_GC_FG | FTK_GC_BG;

		priv->bitmap = ftk_bitmap_create(w, h, *clear_color);
		priv->bits = ftk_bitmap_bits(priv->bitmap);
		priv->w = ftk_bitmap_width(priv->bitmap);
		priv->h = ftk_bitmap_height(priv->bitmap);

		ftk_canvas_set_clip_region(thiz, NULL);
	}

	return thiz;
}

