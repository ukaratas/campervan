#pragma once

#include "hardware_adapter.hpp"
#include <cstdint>

namespace m5dial {

/**
 * Desktop: ←/→ encoder, Enter bırakma süresi = kısa/uzun basış, Esc = uzun basış.
 */
class SimAdapter final : public HardwareAdapter {
public:
    void poll(EventQueue& events) override;

private:
    bool prev_left_{false};
    bool prev_right_{false};
    bool prev_enter_{false};
    bool prev_esc_{false};
    bool enter_pending_{false};
    uint32_t enter_down_ms_{0};

    static constexpr uint32_t kLongPressMs = 500;
    static constexpr uint32_t kMinTapMs = 40;
};

} // namespace m5dial
