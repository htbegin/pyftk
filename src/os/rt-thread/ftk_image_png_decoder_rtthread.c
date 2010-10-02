
#define PNG_SKIP_SETJMP_CHECK
#include <png.h>
#include "ftk_log.h"
#include "ftk_image_png_decoder.h"

#undef SEEK_CUR
#undef SEEK_END
#undef SEEK_SET

#include <dfs_posix.h>

static Ret ftk_image_png_decoder_match(FtkImageDecoder* thiz, const char* filename)
{
	return_val_if_fail(filename != NULL, RET_FAIL);

	return (strstr(filename, ".png") != NULL) ? RET_OK : RET_FAIL;
}

static void ftk_image_png_read_data(png_structp png_ptr, png_bytep data, png_size_t length)
{
	int fd = (int)png_ptr->io_ptr;

	read(fd, data, length);
}

png_voidp rt_png_malloc(png_structp png_ptr, png_size_t size)
{
	return rt_malloc(size);
}

void rt_png_free(png_structp png_ptr, png_voidp ptr)
{
	rt_free(ptr);
}

static FtkBitmap* load_png (const char *filename)
{
	int x = 0;
	int y = 0;
	int w = 0;
	int h = 0;
	int passes_nr = 0;
	int fd = -1;	
	FtkColor* dst = NULL;
	unsigned char* src = NULL;
	FtkBitmap* bitmap = NULL;
	FtkColor  bg = {0};
	png_structp png_ptr = NULL;
	png_infop info_ptr = NULL;
	png_bytep * row_pointers = NULL;

	bg.a = 0xff;
	if ((fd = open (filename, O_RDONLY, 0)) < 0)
	{
		ftk_logd("%s: open %s failed.\n", __func__, filename);
		return NULL;
	}

	if((png_ptr = png_create_read_struct_2(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL, NULL, rt_png_malloc, rt_png_free)) == NULL)
	{
		close(fd);
		return NULL;
	}

	if((info_ptr = png_create_info_struct(png_ptr)) == NULL)
	{
		close(fd);
		return NULL;
	}

	png_set_read_fn(png_ptr, fd, ftk_image_png_read_data);

	memset(info_ptr, 0x00, sizeof(*info_ptr));
	png_read_info(png_ptr, info_ptr);

	w = info_ptr->width;
	h = info_ptr->height;

	passes_nr = png_set_interlace_handling(png_ptr);
	png_read_update_info(png_ptr, info_ptr);

	row_pointers = (png_bytep*) FTK_ZALLOC(h * sizeof(png_bytep));
	for (y=0; y< h; y++)
	{
		row_pointers[y] = (png_byte*) FTK_ZALLOC(info_ptr->rowbytes);
	}

	png_read_image(png_ptr, row_pointers);

	bitmap = ftk_bitmap_create(w, h, bg);
	dst = ftk_bitmap_bits(bitmap);
	if (info_ptr->color_type == PNG_COLOR_TYPE_RGBA)
	{
		for(y = 0; y < h; y++)
		{
			src = row_pointers[y];
			for(x = 0; x < w; x++)
			{
				if(src[3])
				{
					dst->r = src[0];
					dst->g = src[1];
					dst->b = src[2];
				}
				dst->a = src[3];
				src +=4;
				dst++;
			}
		}
	}
	else if(info_ptr->color_type == PNG_COLOR_TYPE_RGB)
	{
		if(0 == info_ptr->num_trans)
		{
			for(y = 0; y < h; y++)
			{
				src = row_pointers[y];
				for(x = 0; x < w; x++)
				{
					dst->r = src[0];
					dst->g = src[1];
					dst->b = src[2];
					dst->a = 0xff;
					src += 3;
					dst++;
				}
			}
		}
		else 
		{
#if PNG_LIBPNG_VER > 10399
			png_byte red = png_ptr->trans_color.red & 0xff;
			png_byte green = png_ptr->trans_color.green & 0xff;
			png_byte blue = png_ptr->trans_color.blue & 0xff;
#else
			png_byte red = png_ptr->trans_values.red & 0xff;
			png_byte green = png_ptr->trans_values.green & 0xff;
			png_byte blue = png_ptr->trans_values.blue & 0xff;
#endif
			for(y = 0; y < h; y++)
			{
				src = row_pointers[y];
				for(x = 0; x < w; x++)
				{
					if(src[0] == red && src[1] == green && src[2] == blue)
					{
						dst->a = 0;
					}
					else
					{
						dst->a = 0xff;
					}
					dst->r = src[0];
					dst->g = src[1];
					dst->b = src[2];
					src += 3;
					dst++;
				}
			}
		}
	}
	else
	{
		assert(!"not supported.");
	}

	for(y = 0; y < h; y++)
	{
		FTK_FREE(row_pointers[y]);
	}
	FTK_FREE(row_pointers);
	png_destroy_read_struct(&png_ptr, &info_ptr, NULL); 
	close(fd);

	return bitmap;
}

static FtkBitmap* ftk_image_png_decoder_decode(FtkImageDecoder* thiz, const char* filename)
{
	return_val_if_fail(ftk_image_png_decoder_match(thiz, filename) == RET_OK, NULL);

	return load_png(filename);
}

static void ftk_image_png_decoder_destroy(FtkImageDecoder* thiz)
{
	if(thiz != NULL)
	{
		FTK_ZFREE(thiz, sizeof(thiz));
	}

	return;
}

FtkImageDecoder* ftk_image_png_decoder_create(void)
{
	FtkImageDecoder* thiz = (FtkImageDecoder*)FTK_ZALLOC(sizeof(FtkImageDecoder));

	if(thiz != NULL)
	{
		thiz->match   = ftk_image_png_decoder_match;
		thiz->decode  = ftk_image_png_decoder_decode;
		thiz->destroy = ftk_image_png_decoder_destroy;
	}

	return thiz;
}

