/*
 * File: ftk_win32.c
 * Author:  Li XianJing <xianjimli@hotmail.com>
 * Brief:   win32 specific functions.
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
 * 2009-11-22 Li XianJing <xianjimli@hotmail.com> created
 *
 */
#include <string.h>
#include <assert.h>
#include "ftk_win32.h"
#include "ftk_log.h"

static char g_work_dir[MAX_PATH+1] = {0};
static char g_data_dir[MAX_PATH+1] = {0};
static char g_testdata_dir[MAX_PATH+1] = {0};

char* ftk_get_root_dir(void)
{
	return g_work_dir;
}

char* ftk_get_data_dir(void)
{
	return g_data_dir;
}

char* ftk_get_testdata_dir(void)
{
	return g_testdata_dir;
}

int ftk_platform_init(int argc, char** argv)
{
	int Ret = 0;
	char* p = NULL;
	WSADATA wsaData = {0};
    
	if ((Ret = WSAStartup(MAKEWORD(2,2), &wsaData)) != 0)
	{
		assert(!"WSAStartup failed with error %d\n");
		return 0;
	}
	
	if(_getcwd(g_work_dir, MAX_PATH) != NULL)
	{
		p = strstr(g_work_dir, "\\src");
		if(p != NULL)
		{
			*p = '\0';
			ftk_snprintf(g_data_dir, MAX_PATH, "%s\\data", g_work_dir);
			ftk_snprintf(g_testdata_dir, MAX_PATH, "%s\\testdata", g_work_dir);
		}
	}

	return 0;
}

void ftk_platform_deinit(void)
{
	if (WSACleanup() == SOCKET_ERROR)
	{
		ftk_logd("WSACleanup failed with error %d\n", WSAGetLastError());
	}

	return;
}

char* ftk_strncpy(char *dest, const char *src, size_t n)
{
	return strncpy(dest, src, n);
}

char* ftk_strdup(const char *s)
{
	return strdup(s);
}

int   ftk_snprintf(char *str, size_t size, const char *format, ...)
{
	int ret = 0;
	va_list args;
	va_start(args, format);
	ret = _vsnprintf(str, size-1, format, args);
	str[size-1] = '\0';

	return 0;
}

int   ftk_vsnprintf(char *str, size_t size, const char *format, va_list ap)
{
	return _vsnprintf(str, size-1, format, ap);
}

size_t ftk_get_relative_time(void)
{
	FILETIME        ft;
	LARGE_INTEGER   li;
	__int64         t;

	GetSystemTimeAsFileTime(&ft);
	li.LowPart  = ft.dwLowDateTime;
	li.HighPart = ft.dwHighDateTime;
	t  = li.QuadPart;       /* In 100-nanosecond intervals */
	t /= 10;                /* In microseconds */

	return t/1000;
}

/*http://cantrip.org/socketpair.c*/
/* socketpair.c
 * Copyright 2007 by Nathan C. Myers <ncm@cantrip.org>; all rights reserved.
 * This code is Free Software.  It may be copied freely, in original or 
 * modified form, subject only to the restrictions that (1) the author is
 * relieved from all responsibilities for any use for any purpose, and (2)
 * this copyright notice must be retained, unchanged, in its entirety.  If
 * for any reason the author might be held responsible for any consequences
 * of copying or use, license is withheld.  
 */
int win32_socketpair(SOCKET socks[2])
{
    int e;
    DWORD flags = 0;
    SOCKET listener;
    struct sockaddr_in addr;
    int addrlen = sizeof(addr);

    if (socks == 0) {
      WSASetLastError(WSAEINVAL);
      return SOCKET_ERROR;
    }

    socks[0] = socks[1] = INVALID_SOCKET;
    if ((listener = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) 
        return SOCKET_ERROR;

    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(0x7f000001);
    addr.sin_port = 0;

    e = bind(listener, (const struct sockaddr*) &addr, sizeof(addr));
    if (e == SOCKET_ERROR) {
        e = WSAGetLastError();
    	closesocket(listener);
        WSASetLastError(e);
        return SOCKET_ERROR;
    }

    e = getsockname(listener, (struct sockaddr*) &addr, &addrlen);
    if (e == SOCKET_ERROR) {
        e = WSAGetLastError();
    	closesocket(listener);
        WSASetLastError(e);
        return SOCKET_ERROR;
    }

    do {
        if (listen(listener, 1) == SOCKET_ERROR)                      break;
        if ((socks[0] = socket(AF_INET, SOCK_STREAM, 0))
                == INVALID_SOCKET)                                    break;
        if (connect(socks[0], (const struct sockaddr*) &addr,
                    sizeof(addr)) == SOCKET_ERROR)                    break;
        if ((socks[1] = accept(listener, NULL, NULL))
                == INVALID_SOCKET)                                    break;
        closesocket(listener);
        return 0;
    } while (0);
    e = WSAGetLastError();
    closesocket(listener);
    closesocket(socks[0]);
    closesocket(socks[1]);
    WSASetLastError(e);

    return SOCKET_ERROR;
}

