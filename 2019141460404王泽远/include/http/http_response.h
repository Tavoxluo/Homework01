//
// Created by makalo on 2021/6/10.
//

#ifndef WEBSERVER_HTTP_RESPONSE_H
#define WEBSERVER_HTTP_RESPONSE_H

#include <string>

namespace status{
    extern const char *OK;
    extern const char *Not_Found;
    extern const char *Moved_Permanently;
    extern const char *Bad_Request;
    extern const char *Forbidden;
}

namespace content_type{
    namespace text{
        extern const char * plain_utf8;
        extern const char * html_utf8;
    }
    namespace image{
        extern const char * gif;
        extern const char * jpg;
        extern const char * png;
    }
    namespace application{
        extern const char * json;
        extern const char* pdf;
    }
}

namespace connection{
    extern const char * keep_alive;
    extern const char * close;
}

extern const char *Not_Found_html ;
extern const char *Bad_Request_html;

struct HTTPResponseHeadInfo{
    std::string Status;
    std::string Date;
    std::string Content_Type;
    std::string Content_Length;
    std::string Connection;
};

void set_http_response(std::string &response,const HTTPResponseHeadInfo& headInfo);

const char* get_content_type(const std::string& suffix);
#endif //WEBSERVER_HTTP_RESPONSE_H
