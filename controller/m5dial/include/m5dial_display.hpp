#pragma once

/**
 * M5Stack M5Dial — resmi özelliklerle uyumlu sabitler
 * @see https://docs.m5stack.com/en/core/M5Dial
 *
 * - 1.28" yuvarlak TFT, sürücü GC9A01, dokunmatik FT3267
 * - Çözünürlük: 240×240 (kare framebuffer; fiziksel görünür alan daire)
 */

namespace m5dial {

inline constexpr int kDisplaySize = 240;
/** Görünür daire yarıçapı (240×240 merkez, kenar orta noktalarına teğet) */
inline constexpr float kRoundRadiusPx = 119.5f;
/** Daire içine sığan merkez kare (~170px) için minimum kenar boşluğu (px) */
inline constexpr int kRoundSafePadding = 36;

} // namespace m5dial
