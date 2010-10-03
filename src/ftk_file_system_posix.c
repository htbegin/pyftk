/*
 * File: ftk_file_system_posix.c
 * Author: Li XianJing <xianjimli@hotmail.com>
 * Brief:  posix implemented file system adaptor.
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
 * 2010-08-14 Li XianJing <xianjimli@hotmail.com> created
 *
 */

#include "ftk_util.h"
#include "ftk_file_system.h"

#ifdef RT_THREAD
#undef SEEK_CUR
#undef SEEK_END
#undef SEEK_SET
#include <dfs_posix.h>
#define DT_UNKNOWN	DFS_DT_UNKNOWN
#define DT_REG		DFS_DT_REG
#define DT_DIR		DFS_DT_DIR
#endif

Ret ftk_file_get_info(const char* file_name, FtkFileInfo* info)
{
	int ret = 0;
#ifndef RT_THREAD
	struct stat st;
#else
	struct _stat st;
#endif
	return_val_if_fail(file_name != NULL && info != NULL, RET_FAIL);

	if((ret = stat(file_name, &st)) == 0)
	{
#ifndef RT_THREAD
		info->uid  = st.st_uid;
		info->gid  = st.st_gid;
#else
		info->uid  = 0;
		info->gid  = 0;
#endif
		info->mode = st.st_mode;
		info->size = st.st_size; 
		info->is_dir = S_ISDIR(st.st_mode);
#ifndef RT_THREAD
		info->last_access = st.st_atime;
#else
		info->last_access = st.st_mtime;
#endif
		info->last_modify = st.st_mtime;

		return RET_OK;
	}

	return RET_FAIL;
}

FtkFsHandle ftk_file_open(const char* file_name, const char* mode)
{
	return_val_if_fail(file_name != NULL && mode != NULL, NULL);

#ifndef RT_THREAD
	return fopen(file_name, mode);
#else
	return (FtkFsHandle)(open(file_name, O_RDWR, 0777)+1);
#endif
}

int  ftk_file_read(FtkFsHandle file, void* buffer, size_t length)
{
#ifndef RT_THREAD
	return fread(buffer, 1, length, file);
#else
	return read((int)(file-1), buffer, length);
#endif
}

int  ftk_file_write(FtkFsHandle file, const void* buffer, size_t length)
{
#ifndef RT_THREAD
	return fwrite(buffer, 1, length, file);
#else
	return write((int)(file-1), buffer, length);
#endif
}

void ftk_file_close(FtkFsHandle file)
{
	return_if_fail(file != NULL);

#ifndef RT_THREAD
	fclose(file);
#else
	close((int)(file-1));
#endif

	return;
}

FtkFsHandle ftk_dir_open(const char* dir_name)
{
	return_val_if_fail(dir_name != NULL, NULL);

	return opendir(dir_name);
}

Ret  ftk_dir_read(FtkFsHandle dir, FtkFileInfo* info)
{
	struct dirent* ent = NULL;
	return_val_if_fail(dir != NULL && info != NULL, RET_FAIL);

	ent = readdir(dir);

	if(ent == NULL)
	{
		return RET_EOF;
	}

#ifdef DT_DIR
	if (ent->d_type != DT_UNKNOWN)
	{
		info->is_dir = ent->d_type & DT_DIR;
	}
	else
#endif
	{
#ifndef RT_THREAD
		struct stat st = {0};
#else
		struct _stat st = {0};
#endif
		stat(ent->d_name, &st);
		info->is_dir = S_ISDIR(st.st_mode);
	}

	ftk_strncpy(info->name, ent->d_name, FTK_MAX_PATH);

	return RET_OK;
}

void ftk_dir_close(FtkFsHandle dir)
{
	if(dir != NULL)
	{
		closedir(dir);
	}

	return;
}

Ret ftk_fs_get_cwd(char cwd[FTK_MAX_PATH+1])
{
	return_val_if_fail(cwd != NULL, RET_FAIL);

	ftk_getcwd(cwd, FTK_MAX_PATH);
	cwd[FTK_MAX_PATH] = '\0';

	return RET_OK;
}

Ret ftk_fs_delete_dir(const char* dir)
{
	return_val_if_fail(dir != NULL, RET_FAIL);

	return rmdir(dir) == 0 ? RET_OK : RET_FAIL;
}

Ret ftk_fs_delete_file(const char* file_name)
{
	return_val_if_fail(file_name != NULL, RET_FAIL);

	return unlink(file_name) == 0 ? RET_OK : RET_FAIL;
}

Ret ftk_fs_create_dir(const char* dir)
{
	char* p = NULL;
	FtkFileInfo info = {0};
	char name[FTK_MAX_PATH+1] = {0};
	return_val_if_fail(dir != NULL, RET_FAIL);

	strncpy(name, dir, FTK_MAX_PATH);
	ftk_normalize_path(name);
	p = name;
	while(1)
	{
		p = strchr(p + 1, FTK_PATH_DELIM);
		if(p != NULL)
		{
			*p = '\0';
		}
		
		if(ftk_file_get_info(name, &info) == RET_OK)
		{
			if(!info.is_dir)
			{
				return RET_EXIST;
			}
		}
		else
		{
			if(mkdir(name, 0770) != 0) break;
		}

		if(p != NULL)
		{
			*p = FTK_PATH_DELIM;
		}
		else
		{
			break;
		}
	}
	
	return RET_OK;
}

Ret ftk_fs_change_dir(const char* dir)
{
	return_val_if_fail(dir != NULL, RET_FAIL);

	return chdir(dir) == 0 ? RET_OK : RET_FAIL;
}

Ret ftk_fs_move(const char* dir_from, const char* dir_to)
{
	return_val_if_fail(dir_from != NULL && dir_to != NULL, RET_FAIL);

	return rename(dir_from, dir_to) == 0 ? RET_OK : RET_FAIL;
}


int ftk_fs_is_root(const char* path)
{
	return_val_if_fail(path != NULL, 0);

	return path[0] == FTK_PATH_DELIM && path[1] == '\0';
}
