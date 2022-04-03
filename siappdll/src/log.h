#pragma once

#include <string>
#include <memory>
#include <sstream>
#include <iostream>
#include <functional>

//#define DEBUG

class Logger
{
    using Stream = std::ostringstream;
    using Buffer_p = std::unique_ptr<Stream, std::function<void(Stream*)>>;

public:
    void log(const std::string& cmd) {
#ifdef DEBUG
        std::cout << cmd << std::endl;
#endif
    }

    Buffer_p log() {
        return Buffer_p(new Stream, [&](Stream* st) {
            log(st->str());
            });
    }
};

extern Logger logger;

#define LOG(x) *(logger.log()) << #x << " "
