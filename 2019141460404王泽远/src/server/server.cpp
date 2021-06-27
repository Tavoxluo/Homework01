#include "../../include/server/server.h"
#include "../../include/core/threadpool.h"

int Server::listenAt(const int port, const int backlag)
{
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(port);
    if(listensock.bind((sockaddr *)&servaddr, sizeof(servaddr))!=0)
        return -1;
    return listen(listensock.get(), backlag);
}
void Server::run(size_t tp_size,Handler handler) const//no-blocking
{
    if(isRunning){
        return;
    }
    isRunning = true;
    //开启后台任务以防阻塞在while循环
    std::thread t([&]()
                {
                    ThreadPool<Makalo::Socket> pool(4);
                    while (isRunning)
                    {
                        struct sockaddr_in cliaddr{};
                        socklen_t cli_len = sizeof(cliaddr);
                        Makalo::Socket connesock = listensock.accept((sockaddr *)&cliaddr, &cli_len); //blocking
                        //printf("client [address]%d connect to [socket]%d\n", cliaddr.sin_addr.s_addr,connesock.get());
                        pool.execute(handler,connesock);
                    }
                    std::cout<<"server terminate"<<std::endl;
                });
    t.detach();
    printf("server is running at background\n");

}
void Server::stop()
{
    isRunning = false;
}
