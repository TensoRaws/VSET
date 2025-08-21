import type { TaskConfig } from '@shared/type/taskConfig'
import { writeFileSync } from 'node:fs'
import path from 'node:path'

import { getExtraSRModelPath, getGenSettingsPath } from './getCorePath'

export async function writeSettingsJson(_, task_config: TaskConfig): Promise<void> {
  const filePath = getGenSettingsPath(task_config)
  writeFileSync(filePath, JSON.stringify(task_config, null, 2))
}

export async function writeVpyFile(_, vpy_path: string, vpy_content: string, video_path: string): Promise<void> {
  vpy_content = vpy_content
    .replace(/__VIDEO_PATH__/g, path.normalize(video_path))
    .replace(/__EXTRA_MODEL_PATH__/g, getExtraSRModelPath())
  writeFileSync(vpy_path, vpy_content)
}
