#include "sock_ll.h"
#include "sock.h"
#include "log.h"

int sock_connect(const char *sock_file)
{
	LOG(INFO) << "Creating socket";

	int fd = l_socket(AF_UNIX, SOCK_STREAM, 0);
	if (fd < 0) {
		LOG(ERROR) << "l_socket() return err: 0x" << std::hex << fd;

		/* workaround because l_socket() sometime return strange 0xc0000002 value */
		LOG(INFO) << "trying l_socket_int80h()";
		fd = l_socket_int80h(AF_UNIX, SOCK_STREAM, 0);
		if (fd < 0) {
			LOG(ERROR) << "l_socket_int80h() return err: 0x" << std::hex << fd;
			LOG(ERROR) << "Failed to create socket";
			return -1;
		}
	}

	LOG(INFO) << "fd: " << fd;

	struct sockaddr_un addr;
	addr.sun_family = AF_UNIX;
	snprintf(addr.sun_path, sizeof(addr.sun_path), sock_file);

	LOG(INFO) << "Attempting to connect to " << addr.sun_path;

	if (l_connect(fd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
		LOG(ERROR) << "Failed to connect";

		l_close(fd);

		return -1;
	}

	return fd;
}

int sock_read(int fd, char* buf, size_t count)
{
	return l_read(fd, buf, count);
}

void sock_close(int fd)
{
	l_close(fd);
}