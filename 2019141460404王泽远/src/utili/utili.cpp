//
// Created by makalo on 2021/5/27.
//

#include <fstream>
#include <iostream>

#include <vector>
#include <algorithm>

#include "../../include/utili/utili.h"

void appendFormFile(std::ifstream &fs,std::vector<char>& buf) {
    fs.seekg(0, std::ios::end);
    int length= fs.tellg();
    fs.seekg(0, std::ios::beg);
    char buffer[length];
    fs.read(buffer, length);
    //buffer[length-1]='\0';
    fs.close();
    buf.assign(buffer,(buffer+length));
}
