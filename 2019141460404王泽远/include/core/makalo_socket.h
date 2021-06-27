#ifndef MAKALO_SOCKET_H
#define MAKALO_SOCKET_H

#include <unistd.h>
#include <sys/socket.h>
#include <stdio.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
namespace Makalo
{
    class Socket
    {
    public:
        explicit Socket(int domain, int type, int protocol) : _sockfd(::socket(domain, type, protocol)), count(new int(1))
        {
        }
        explicit Socket(const int sockfd) : _sockfd(sockfd), count(new int(1))
        {
        }

        Socket(const Socket &s) : _sockfd(s._sockfd), count(s.count) { (*count)++; }

        Socket &operator=(const Socket &s)
        {
            if (this != &s)
            {
                if (--(*(this->count)) == 0)
                {
                    delete count;
                    close(_sockfd);
                }
                _sockfd = s._sockfd;
                count = s.count;
                (*count)++;
            }
            return *this;
        };

        ~Socket()
        {
            if (--(*(this->count)) == 0)
            {
                delete count;
                close(_sockfd);
                //printf("socket %d closed!\n", _sockfd);
            }
        }

        int get() const;
        void connect(char const *ip, const uint16_t port) const;
        int bind(const struct sockaddr *myaddr, socklen_t addrlen) const;
        Socket accept(struct sockaddr *__addr, socklen_t *__addr_len) const;
        int read(void *_buf, const size_t _nbytes) const;
        int recv(void *buf,const size_t _nbytes, const int _flags) const;
        int write(void *buf, const size_t _nbytes)const;

    private:
        int _sockfd;
        int *count;
    };
};
#endif
