
#ifndef SERVER_H
#define SERVER_H

#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <string.h>
#include <future>
#include <functional>
#include "../core/makalo_socket.h"
#include <stdio.h>
#include "../core/threadpool.h"

class Server
{
public:
using Handler=std::function<void(Makalo::Socket)>;
public:
    explicit Server() : listensock(AF_INET, SOCK_STREAM, 0){}
    int listenAt(const int port, const int backlag);
    void run(size_t tp_size,Handler task) const;
    void stop();
private:
    Makalo::Socket listensock;
    struct sockaddr_in servaddr{};
    mutable bool isRunning = false;
};

#endif