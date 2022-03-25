#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <unistd.h>
#include <poll.h>
#include <time.h>

#define DEBUG
#ifdef DEBUG
	#define DPRN(format, args...) printf(format, ##args)
#else
	#define DPRN(format, args...) do {} while (0)
#endif

#define ARRAY_SIZE(x) (sizeof(x) / sizeof(x[0]))

#define SOCK_FILE "/var/run/spnav.sock"
#define PORT 11111

// decreasing events rate from spacemouse - this need for decrease rate of screen refresh in fusion360 - decrease cpu load
#define SHAPE
#define SHAPE_DELAY_MS 30
#define SHAPE_DELAY_US (SHAPE_DELAY_MS * 1000)

#ifdef SHAPE
#define POLL_TIMEOUT SHAPE_DELAY_MS
#else
#define POLL_TIMEOUT -1
#endif

#ifdef SHAPE
unsigned int get_time_us(void)
{
	struct timespec tp;
	clock_gettime(CLOCK_MONOTONIC_RAW, &tp);
	return tp.tv_sec * 1000000 + tp.tv_nsec / 1000;
}
#endif

int daem_connect(void)
{
	int daemfd = socket(AF_UNIX, SOCK_STREAM, 0);
	if (daemfd < 0) {
		DPRN("could not create unix sock\n");
		return -1;
	}

	struct sockaddr_un addr_un = {0};

	addr_un.sun_family = AF_UNIX;
	strncpy(addr_un.sun_path, SOCK_FILE, sizeof(addr_un.sun_path) - 1);

	if (connect(daemfd, (struct sockaddr*)&addr_un, sizeof(addr_un))) {
		DPRN("could not connect to spacenavd\n");
		close(daemfd);
		return -1;
	}

	return daemfd;
}

void daem_close(int fd)
{
	close(fd);
}

int main(void)
{
	if (daemon(0, 1)) {
		DPRN("could not daemonize\n");
		return -1;
	}

	int listenfd = socket(AF_INET, SOCK_STREAM, 0);
	if (listenfd < 0) {
		DPRN("could not create inet sock\n");
		return -1;
	}

	int enable = 1;
	setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int));

	struct sockaddr_in addr_in = {0};
	addr_in.sin_family = AF_INET;
	addr_in.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
	addr_in.sin_port = htons(PORT);

	if (bind(listenfd, (struct sockaddr*)&addr_in, sizeof(addr_in))) {
		DPRN("could bind\n");
		close(listenfd);
		return -1;
	}

	listen(listenfd, 1);

	while (1) {
		DPRN("waiting for connection\n");

		int confd = accept(listenfd, (struct sockaddr*)NULL, NULL);
		if (confd < 0) {
			printf("could not accept\n");
			continue;
		}

		DPRN("connection accepted\n");

		int daemfd = daem_connect();
		if (daemfd >= 0)
			DPRN("daemon connection success\n");
		else
			continue;

		struct pollfd fds[2];

		fds[0].fd = confd;
		fds[0].events = POLLIN;

		fds[1].fd = daemfd;
		fds[1].events = POLLIN;

		int motion[8] = {0};

#ifdef SHAPE
		unsigned int last = get_time_us();
#endif
		int run = 1;
		while (run) {
			int i;
			int ret = poll(fds, ARRAY_SIZE(fds), POLL_TIMEOUT);

#ifdef SHAPE
			unsigned int now = get_time_us();

			if ((now - last) > SHAPE_DELAY_US) {
				int sum = 0;
				for (i = 1; i < 7; i++)
					sum |= motion[i];
				if (sum) {
					if (write(confd, motion, sizeof(motion)) != sizeof(motion)) {
						run = 0;
						break;
					}
					bzero(motion, sizeof(motion));
				}

				last = now;
			}
#endif

			if (ret <= 0) {
				if (ret < 0)
					DPRN("poll() failed\n");
				continue;
			}

			for (i = 0; i < ARRAY_SIZE(fds); i++) {
				if(fds[i].revents == 0)
					continue;

				if(fds[i].revents != POLLIN) {
					DPRN("poll() invalid revents == 0x%04x fds[%d]\n", fds[i].revents, i);
					continue;
				}

				if (fds[i].fd == confd) {
					run = 0;
					break;
				}

				if (fds[i].fd == daemfd) {
					int data[8];
					ssize_t len = read(daemfd, data, sizeof(data));
					if (len <= 0) {
						run = 0;
						break;
					}
#ifdef SHAPE
					if (data[0] == 0) {
						int j;
						for (j = 1; j < 7; j++)
							motion[j] += data[j];
					}
					else
#endif
					{
						if (write(confd, data, len) != len) {
							run = 0;
							break;
						}
					}
				}
			}
		}

		DPRN("daemon connection close\n");
		daem_close(daemfd);

		DPRN("close connection\n");
		close(confd);
	}

	close(listenfd);

	return 0;
}
