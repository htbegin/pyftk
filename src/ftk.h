/*
 * File: ftk.h    
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief: ftk global init, mainloop and deinit functions.  
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
 * 2009-10-03 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#ifndef FTK_H
#define FTK_H

#ifdef __cplusplus
extern "C" {
#endif/*__cplusplus*/

#include "ftk_log.h"
#include "ftk_bitmap.h"
#include "ftk_dialog.h"
#include "ftk_window.h"
#include "ftk_style.h"
#include "ftk_app_window.h"
#include "ftk_label.h"
#include "ftk_image.h"
#include "ftk_entry.h"
#include "ftk_button.h"
#include "ftk_globals.h"
#include "ftk_source_idle.h"
#include "ftk_source_timer.h"
#include "ftk_status_panel.h"
#include "ftk_status_item.h"
#include "ftk_menu_panel.h"
#include "ftk_menu_item.h"
#include "ftk_progress_bar.h"
#include "ftk_check_button.h"
#include "ftk_radio_group.h"

Ret  ftk_init(int argc, char* argv[]);
Ret  ftk_run(void);
void ftk_quit(void);

#ifdef __cplusplus
}
#endif/*__cplusplus*/

#endif/*FTK_H*/

