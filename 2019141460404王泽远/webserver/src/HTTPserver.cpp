#include "../include/server/server.h"
#include "../include/http/http.h"
#include <cstdio>
#include <csignal>
#include <cstdlib>

bool shouldclose =false;

void signal_handler(int)
{
    shouldclose=true;
    puts("server closed!\n");
}


int main(int argc,char **argv)
{
    size_t n_threads;
    int port;
    
    if(argc!=3){
        printf("usage: webserver [threads] [port]\n");
        return 0;
    }
    n_threads=atoi(argv[1]);
    port=atoi(argv[2]);
    
    std::signal(SIGINT, signal_handler);
    Server server;
    if(server.listenAt(port,1024)!=0)
    {
        printf("server start fail\n");
        return -1;
    }
    
    server.run(n_threads, http_handler);
    printf("CTRL+C to terminate\n");
    while(!shouldclose);
    
    server.stop();
}
