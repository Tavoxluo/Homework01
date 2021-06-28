#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <thread>
#include <vector>
#include <queue>
#include <exception>
#include <functional>
#include <cstdio>
#include <mutex>
#include <iostream>
#include <condition_variable>

#define TRACE std::cout << __FILE__ << "," << __LINE__ << std::endl;

template <typename Arg>
struct Task
{
public:
    Task(std::function<void(Arg)> _fn, Arg _arg) : fn(_fn), arg(_arg) {}
    std::function<void(Arg)> fn;
    Arg arg;
};

template <typename Arg>
class ThreadPool
{
public:
    explicit ThreadPool(unsigned int size)
    {
        if (size <= 0)
            throw std::exception();
        tasks=new std::queue<Task<Arg>>;
        for (int i = 0; i < size; i++)
        {
            workers.emplace_back([this]()
                                 {
                                     while (true)
                                     {
                                         //进入临界区
                                         std::unique_lock<std::mutex> u(qmux);
                                         con_var.wait(u, [this]()
                                                      { return !tasks->empty() || stopped; });//队列空且不停止，则阻塞直到生产者将其唤醒
                                         if (stopped && tasks->empty())
                                             return; //线程结束
                                         auto task = tasks->front();
                                         tasks->pop();
                                         u.unlock();
                                         //退出临界区
                                         task.fn(task.arg);
                                     }
                                 });
        }
    }

    ~ThreadPool()
    {
        stopped = true;
        con_var.notify_all();
        for (auto & t : workers)
            t.join();
        delete tasks;
    }

public:
    void execute(const std::function<void(Arg)> handler, Arg arg)
    {
        std::unique_lock<std::mutex> u(qmux);
        tasks->emplace(handler, arg);
        u.unlock();
        con_var.notify_one();
    }

private:
    std::mutex qmux;
    std::condition_variable con_var;
    std::vector<std::thread> workers;
    std::queue<Task<Arg>>* tasks;
    bool stopped=false;
};

#endif