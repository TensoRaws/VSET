import type { TaskConfig } from '@shared/type/taskConfig'
import { writeFileSync } from 'node:fs'
import path from 'node:path'

import { getExtraSRModelPath, getGenSettingsPath } from './getCorePath'

export async function writeSettingsJson(_, taskConfig: TaskConfig): Promise<void> {
  const filePath = getGenSettingsPath(taskConfig)
  writeFileSync(filePath, JSON.stringify(taskConfig, null, 2))
}

export async function writeVpyFile(_, vpyPath: string, vpyContent: string, videoPath: string): Promise<void> {
  vpyContent = vpyContent
    .replace(/__VIDEO_PATH__/g, path.normalize(videoPath))
    .replace(/__EXTRA_MODEL_PATH__/g, getExtraSRModelPath())
  writeFileSync(vpyPath, vpyContent)
}
