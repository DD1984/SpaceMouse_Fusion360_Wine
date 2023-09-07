#pragma once

extern "C" int __fastcall l_open(const char* filename, int flags, int mode);
extern "C" int __fastcall l_read(int fd, char* buf, unsigned int count);
extern "C" int __fastcall l_close(int fd);
extern "C" int __fastcall l_socket(int domain, int type, int protocol);
extern "C" int __fastcall l_socket_int80h(int domain, int type, int protocol);
extern "C" int __fastcall l_connect(int sockfd, const struct sockaddr* addr, unsigned int addrlen);
