#pragma once

#include <string>
#include <memory>
#include <sstream>
#include <iostream>
#include <functional>

enum class DbgType {
    INFO_T = 0,
    ERROR_T,
    TRACE_T,
};

class Logger
{
    using Stream = std::ostringstream;
    using Buffer_p = std::unique_ptr<Stream, std::function<void(Stream*)>>;

public:
    void log(const std::string& cmd) {
        std::cout << cmd << std::endl;
    }

    Buffer_p log(DbgType l) {
        return Buffer_p(new Stream, [&, this, l](Stream* st) {
            if (l <= dbgLevel)
                log(st->str());
            });
    }

private:
    DbgType dbgLevel = DbgType::ERROR_T;
};

extern Logger logger;

#define LOG(x) *(logger.log(DbgType:: ## x ## _T)) << "[*** SPMOUSE ***] " << #x << " "
