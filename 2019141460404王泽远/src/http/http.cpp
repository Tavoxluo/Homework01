//
// Created by makalo on 2021/6/14.
//

#include <string>
#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <ctime>

#include "../../include/http/http.h"
#include "../../include/http/http_response.h"

#include "../../include/utili/utili.h"

#define MAX_HTTP_MSG 2048

void http_handler(const Makalo::Socket &sock) {
    char buf[MAX_HTTP_MSG];
    ssize_t n;
    CONT:
    while ((n = sock.read(buf, MAX_HTTP_MSG)) > 0) {
        std::string request(buf);
        std::string response_head;
        HTTPResponseHeadInfo headInfo;//响应头信息
        std::vector<char> data;//响应数据

        if (request.find_first_of("GET") == 0) //如果请求体以GET开头
        {
            auto s1 = request.substr(4);
            auto file_path = s1.substr(1, s1.find_first_of(' ') - 1);//获取文件名
            auto p=file_path.find_last_of('.');
            auto file_suffix=file_path.substr(p+1);
            std::ifstream fs(file_path,std::ios::binary);
            if (fs.is_open()) {
                headInfo.Status=status::OK;
                appendFormFile(fs,data);
                headInfo.Content_Type= get_content_type(file_suffix);
                headInfo.Content_Length=std::to_string(data.size());
            }else{
                headInfo.Status=status::Not_Found;
                data.assign(Not_Found_html,Not_Found_html+ strlen(Not_Found_html));
                headInfo.Content_Type=content_type::text::html_utf8;
                headInfo.Content_Length=std::to_string(data.size());
            }
        }else{
            headInfo.Status=status::Bad_Request;
            data.assign(Bad_Request_html,Bad_Request_html+ strlen(Bad_Request_html));
            headInfo.Content_Type=content_type::text::html_utf8;
            headInfo.Content_Length=std::to_string(data.size());
        }
        headInfo.Connection=connection::keep_alive;
        const auto now = std::time(nullptr);
        headInfo.Date=std::asctime(std::localtime(&now));

        set_http_response(response_head,headInfo);

        std::vector<char> res;
        res.insert(res.begin(),response_head.begin(),response_head.end());
        res.insert(res.end(),data.begin(),data.end());
        sock.write(res.data(), res.size());
    }

    if(n==0&&errno==EINTR){
        goto CONT;
    }
}
