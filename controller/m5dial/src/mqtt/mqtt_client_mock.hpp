#pragma once

namespace m5dial {

/** Placeholder MQTT — simulator: no-op; device: swap implementation later */
class MqttClientMock {
public:
    void connect(const char* /*host*/, uint16_t /*port*/) {}
    void publish(const char* /*topic*/, const char* /*payload*/) {}
    bool is_connected() const { return false; }
};

} // namespace m5dial
