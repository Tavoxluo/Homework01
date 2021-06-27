#include "../../include/core/makalo_socket.h"

namespace Makalo
{
    int Socket::get() const
    {
        return _sockfd;
    }
    void Socket::connect(char const *ip, const uint16_t port) const
    {
        struct sockaddr_in servaddr;
        bzero(&servaddr, sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        inet_pton(AF_INET, ip, &servaddr.sin_addr);
        servaddr.sin_port = htons(port);
        ::connect(_sockfd, (sockaddr *)&servaddr, sizeof(servaddr));
    }
    int Socket::bind(const struct sockaddr *myaddr, socklen_t addrlen) const
    {
        return ::bind(_sockfd, myaddr, addrlen);
    }

    Socket Socket::accept(struct sockaddr *__addr, socklen_t *__addr_len) const
    {
        return Socket(::accept(_sockfd, __addr, __addr_len));
    }
    int Socket::read(void *_buf, const size_t _nbytes) const
    {
        return ::read(_sockfd, _buf, _nbytes);
    }
    int Socket::write(void *buf, const size_t n) const
    {
        return ::write(_sockfd, buf, n);
    }
    int Socket::recv(void *buf,const size_t _nbytes, const int _flags) const
    {
        return ::recv(_sockfd,buf,_nbytes,_flags);
    }
}