#pragma once

#include "events.hpp"
#include <deque>
#include <mutex>

namespace m5dial {

class EventQueue {
public:
    void push(const AppEvent& e) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push_back(e);
    }

    bool pop(AppEvent& out) {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.empty()) {
            return false;
        }
        out = queue_.front();
        queue_.pop_front();
        return true;
    }

    void clear() {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.clear();
    }

private:
    std::deque<AppEvent> queue_;
    std::mutex mutex_;
};

} // namespace m5dial
