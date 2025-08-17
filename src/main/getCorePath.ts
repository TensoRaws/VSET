import path from 'node:path'
import { app } from 'electron'

/**
 * 获取 VSET-core 的路径
 * dev模式下，存放在项目根目录下的 resources
 * 在 electron-builder 中配置 extraResources，ASAR 打包时将它放入 app.asar 同级目录
 * @returns {string} VSET-core 的路径
 */
export function getCorePath(): string {
  if (process.env.NODE_ENV === 'development') {
    return path.join(app.getAppPath(), 'resources', 'VSET-core')
  }
  else {
    return path.join(app.getAppPath(), '..', 'VSET-core')
  }
}

/**
 * 获取 VSET-core 中的可执行文件路径
 * @returns {object} 包含 vspipe、ffmpeg 和 ffprobe 的路径
 */
export function getExecPath(): { vspipe: string, ffmpeg: string, ffprobe: string } {
  return {
    vspipe: path.join(getCorePath(), 'VSPipe.exe'),
    ffmpeg: path.join(getCorePath(), 'ffmpeg.exe'),
    ffprobe: path.join(getCorePath(), 'ffprobe.exe'),
  }
}

/**
 * 获取 VSET-core 中的额外超分模型文件夹路径
 * @returns {string} 额外超分模型文件夹路径
 */
export function getExtraSRModelPath(): string {
  return path.join(getCorePath(), 'vs-coreplugins', 'models', 'VSET_ExtraSrModel')
}

/**
 * 获取 VSET 生成的设置文件路径
 * 暂时存放在 config_json.outputfolder 目录下
 * @param config_json
 */
export function getGenSettingsPath(config_json): string {
  return path.join(config_json.outputfolder, 'setting.json')
}

/**
 * 获取 VSET 生成的 vpy 文件路径
 * 暂时存放在 config_json.outputfolder 目录下
 * @param config_json
 * @param base_name 生成的 vpy 文件名（不含扩展名）
 */
export function getGenVpyPath(config_json, base_name: string): string {
  return path.join(config_json.outputfolder, `${base_name}.vpy`)
}
