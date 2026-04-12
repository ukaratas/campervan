#pragma once

#include "../core/event_queue.hpp"

namespace m5dial {

/**
 * Abstract input + tick source.
 * Desktop: SimAdapter (SDL keyboard).
 * Device: M5DialAdapter (encoder + button via M5Unified).
 */
class HardwareAdapter {
public:
    virtual ~HardwareAdapter() = default;
    /** Pump hardware; translate to AppEvent into queue */
    virtual void poll(EventQueue& events) = 0;
};

} // namespace m5dial
