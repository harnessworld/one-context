'use strict';

/**
 * Path resolver with subdirectory-first fallback for backward compatibility.
 * New standardized layout:
 *   - slides/presentation.html
 *   - subtitles/sub.srt
 *   - timing/wav-durations.json
 *   - timing/video-input.json
 *   - content/01-script.md (fallback to 讲稿.md)
 */

const fs = require('fs');
const path = require('path');

/**
 * Resolve a file path with subdirectory-first search and fallback to root.
 * For reads: checks subfolder first, then falls back to root.
 * For writes: returns subfolder path (caller should ensure directory exists).
 *
 * @param {string} projectRoot - Project root directory
 * @param {string} subfolder - Subdirectory name (e.g., 'slides', 'subtitles', 'timing')
 * @param {string} filename - Filename to resolve
 * @returns {string} - Resolved path (prefers subfolder if exists, otherwise falls back)
 */
function resolvePath(projectRoot, subfolder, filename) {
  const subPath = path.join(projectRoot, subfolder, filename);
  const rootPath = path.join(projectRoot, filename);

  // For reads: return the path that exists, preferring subfolder
  if (fs.existsSync(subPath)) {
    return subPath;
  }
  if (fs.existsSync(rootPath)) {
    return rootPath;
  }

  // Neither exists: return subfolder path as default (for new file writes)
  return subPath;
}

/**
 * Ensure the directory for a file path exists.
 *
 * @param {string} filePath - Full file path
 */
function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

module.exports = { resolvePath, ensureDir };
