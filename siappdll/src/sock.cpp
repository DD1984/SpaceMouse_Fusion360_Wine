#include "sock_ll.h"
#include "sock.h"
#include "log.h"

bool int80h = false;

int sock_connect(const char *sock_file)
{
	LOG(INFO) << "Creating socket";

	int fd = -1;
	if (int80h || (fd = l_socket(AF_UNIX, SOCK_STREAM, 0)) < 0) {
		LOG(ERROR) << "l_socket() return err: 0x" << std::hex << fd;

		/* workaround because l_socket() sometime return strange 0xc0000002 value */
		LOG(INFO) << "trying l_socket_int80h()";
		fd = l_socket_int80h(AF_UNIX, SOCK_STREAM, 0);
		if (fd < 0) {
			LOG(ERROR) << "l_socket_int80h() return err: 0x" << std::hex << fd;
			LOG(ERROR) << "Failed to create socket";
			return -1;
		}

		LOG(INFO) << "Using int80h api!!!";
		int80h = true;
	}

	LOG(INFO) << "fd: " << fd;

	struct sockaddr_un addr;
	addr.sun_family = AF_UNIX;
	snprintf(addr.sun_path, sizeof(addr.sun_path), sock_file);

	LOG(INFO) << "Attempting to connect to " << addr.sun_path;

	int (*connect_func)(int sockfd, const struct sockaddr* addr, unsigned int addrlen) = l_connect;
	if (int80h)
		connect_func = l_connect_int80h;

	int ret;
	if ((ret = connect_func(fd, (struct sockaddr*)&addr, sizeof(addr))) < 0) {
		LOG(ERROR) << "connect() return err: 0x" << std::hex << ret;
		LOG(ERROR) << "Failed to connect";

		sock_close(fd);
		return -1;
	}

	return fd;
}

int sock_read(int fd, char* buf, size_t count)
{
	int (*read_func)(int fd, char* buf, unsigned int count) = l_read;
	if (int80h)
		read_func = l_read_int80h;

	return read_func(fd, buf, count);
}

void sock_close(int fd)
{
	int (*close_func)(int fd) = l_close;
	if (int80h)
		close_func = l_close_int80h;
}