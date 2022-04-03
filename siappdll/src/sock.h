#pragma once

#define SOCK_FILE "/var/run/spnav.sock"

#define AF_UNIX     1
#define SOCK_STREAM 1

struct sockaddr_un {
	unsigned short sun_family;               /* AF_UNIX */
	char           sun_path[108];            /* pathname */
};

int sock_connect(const char* sock_file);
int sock_read(int fd, char* buf, size_t count);
void sock_close(int fd);