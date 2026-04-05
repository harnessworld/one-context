'use strict';

/**
 * ASS / libass 颜色：PrimaryColour、BackColour 等为 &HAABBGGRR。
 * Alpha：00 = 完全不透明，FF = 全透明（与常见 RGBA 相反）。
 */

/** #RRGGBB → 不透明时的 BGR 后缀 bbggrr（不含 &H 前缀） */
function hexToAssBgrSuffix(hex) {
  if (!hex || typeof hex !== 'string') return null;
  const m = hex.trim().match(/^#?([0-9a-fA-F]{6})$/);
  if (!m) return null;
  const n = parseInt(m[1], 16);
  const r = (n >> 16) & 0xff;
  const g = (n >> 8) & 0xff;
  const b = n & 0xff;
  const bb = b.toString(16).padStart(2, '0');
  const gg = g.toString(16).padStart(2, '0');
  const rr = r.toString(16).padStart(2, '0');
  return `${bb}${gg}${rr}`;
}

/** #RRGGBB → libass PrimaryColour 不透明 &H00BBGGRR */
function hexToAssBgr(hex) {
  const suf = hexToAssBgrSuffix(hex);
  return suf ? `&H00${suf}` : null;
}

/**
 * #RRGGBB + ASS alpha 字节（0=不透明，255=全透明）→ &HAABBGGRR
 */
function hexToAssPrimaryColour(hex, alphaByte) {
  const suf = hexToAssBgrSuffix(hex || '#FFFF00');
  if (!suf) return '&H6C00FFFF';
  const raw = Number(alphaByte);
  const a = Number.isFinite(raw)
    ? Math.max(0, Math.min(255, Math.round(raw)))
    : 0;
  const ah = a.toString(16).padStart(2, '0').toUpperCase();
  return `&H${ah}${suf}`;
}

/** 带透明度：alpha 0–255（此处与 BackColour 一致，由调用方约定含义）→ ASS &HAABBGGRR */
function hexToAssWithAlpha(hex, alpha255) {
  const a = Math.max(0, Math.min(255, Math.round(Number(alpha255) || 255)));
  const ah = a.toString(16).padStart(2, '0').toUpperCase();
  const inner = hexToAssBgr(hex || '#000000');
  if (!inner) return `&H${ah}000000`;
  return `&H${ah}${inner.slice(4)}`;
}

/** wav-auto / wav 烧录与 tts 共用的默认字幕外观 */
const DEFAULT_SUBTITLE_STYLE = {
  fontSize: 18,
  marginV: 18,
  primaryColour: '#FFFF00',
  /** 字幕字色半透明：ASS alpha，0 不透明，255 全透明 */
  primaryAlpha: 108,
};

module.exports = {
  hexToAssBgr,
  hexToAssWithAlpha,
  hexToAssPrimaryColour,
  DEFAULT_SUBTITLE_STYLE,
};
