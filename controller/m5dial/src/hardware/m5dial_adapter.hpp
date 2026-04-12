#pragma once

#include "hardware_adapter.hpp"

namespace m5dial {

/** Real M5Dial — implemented when building env:m5dial (M5Unified). */
class M5DialAdapter final : public HardwareAdapter {
public:
    void poll(EventQueue& events) override;
};

} // namespace m5dial
