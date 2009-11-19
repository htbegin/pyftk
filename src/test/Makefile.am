INCLUDES=-Wall -g -DHAS_PNG -DHAS_JPEG -DFTK_FONT="\"unicode.fnt\"" -DDATA_DIR="\"$(datadir)/ftk\"" \
	-DLINUX -I$(abs_top_srcdir)/src -DTESTDATA_DIR="\"$(abs_top_srcdir)/src/testdata\""
MYLDFLAGS=$(abs_top_builddir)/src/.libs/libftk.a -lpng -ljpeg

noinst_PROGRAMS=label_test widget_test \
	canvas_test ftk_test bitmap_test font_test primary_source_test\
	bitmap_factory_test main_loop_test png_test log_test util_test \
	sources_manager_test text_buffer_test icon_cache_test 

if FTK_BACKEND_FB
noinst_PROGRAMS +=display_fb_test input_test
display_fb_test_SOURCES=display_fb_test.c
display_fb_test_LDFLAGS=$(MYLDFLAGS)
input_test_SOURCES=input_test.c
input_test_LDFLAGS=$(MYLDFLAGS)
endif

icon_cache_test_SOURCES=icon_cache_test.c
icon_cache_test_LDFLAGS=$(MYLDFLAGS)

sources_manager_test_SOURCES=sources_manager_test.c
sources_manager_test_LDFLAGS=$(MYLDFLAGS)

text_buffer_test_SOURCES=text_buffer_test.c
text_buffer_test_LDFLAGS=$(MYLDFLAGS)

util_test_SOURCES=util_test.c
util_test_LDFLAGS=$(MYLDFLAGS)

log_test_SOURCES=log_test.c
log_test_LDFLAGS=$(MYLDFLAGS)

png_test_SOURCES=png_test.c
png_test_LDFLAGS=$(MYLDFLAGS)

font_test_SOURCES=font_test.c
font_test_LDFLAGS=$(MYLDFLAGS)

bitmap_test_SOURCES=bitmap_test.c
bitmap_test_LDFLAGS=$(MYLDFLAGS)

label_test_SOURCES=label_test.c
label_test_LDFLAGS=$(MYLDFLAGS)

widget_test_SOURCE=widget_test.c
widget_test_LDFLAGS=$(MYLDFLAGS)

canvas_test_SOURCES=canvas_test.c
canvas_test_LDFLAGS=$(MYLDFLAGS)

ftk_test_SOURCES=ftk_test.c
ftk_test_LDFLAGS=$(MYLDFLAGS)

bitmap_factory_test_SOURCES=bitmap_factory_test.c
bitmap_factory_test_LDFLAGS=$(MYLDFLAGS)

main_loop_test_SOURCES=main_loop_test.c
main_loop_test_LDFLAGS=$(MYLDFLAGS)

primary_source_test_SOURCES=primary_source_test.c
primary_source_test_LDFLAGS=$(MYLDFLAGS)
