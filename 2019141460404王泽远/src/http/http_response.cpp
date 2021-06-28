//
// Created by makalo on 2021/6/14.
//

#include "../../include/http/http_response.h"

namespace status{
    const char *OK = " 200 OK ";
    const char *Not_Found = " 404 Not Found";
    const char *Moved_Permanently=" 301 Moved Permanently";
    const char *Bad_Request=" 400 Bad Request";
    const char *Forbidden=" 403 Forbidden";
}

namespace content_type{
    namespace text{

        const char * plain_utf8="text/plain; charset=UTF-8";
        const char * html_utf8="text/html; charset=UTF-8";
    }
    namespace image{
        const char * gif="image/gif";
        const char * jpg="image/jpeg";
        const char * png="image/png";
    }
    namespace application{
        const char * json="application/json";
        const char* pdf="application/pdf";
    }
}

namespace connection{
    const char * keep_alive="Keep-Alive";
    const char * close="Close";
}

const char *Not_Found_html = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n";
const char *Bad_Request_html="<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n";




void set_http_response(std::string &response, const HTTPResponseHeadInfo &headInfo) {
    response.append("HTTP/1.1 ")
    .append(headInfo.Status+"\r\n")
    .append("Date:"+headInfo.Date)
    .append("Content-Type:"+headInfo.Content_Type+"\r\n")
    .append("Content-Length:"+headInfo.Content_Length+"\r\n")
    .append("Connection:"+headInfo.Connection+"\r\n")
    .append("\r\n");
}

const char* get_content_type(const std::string& suffix){
    if(suffix=="txt"){
        return content_type::text::plain_utf8;
    }else if(suffix=="html"||suffix=="htm"){
        return content_type::text::html_utf8;
    }else if(suffix=="gif"){
        return content_type::image::gif;
    }else if(suffix=="jpg"){
        return content_type::image::jpg;
    }else if(suffix=="png"){
        return content_type::image::png;
    }else if(suffix=="json"){
        return content_type::application::json;
    }else if(suffix=="pdf"){
        return content_type::application::pdf;
    }
    return content_type::text::plain_utf8;
}