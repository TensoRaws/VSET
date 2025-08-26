import type { TaskConfig } from '@shared/type/taskConfig'
import { writeFileSync } from 'node:fs'
import path from 'node:path'
import { MagicStr } from '@shared/constant/magicStr'

import { getExtraSRModelPath, getGenSettingsPath } from './getCorePath'

export async function writeSettingsJson(_, taskConfig: TaskConfig): Promise<void> {
  const filePath = getGenSettingsPath(taskConfig)
  writeFileSync(filePath, JSON.stringify(taskConfig, null, 2))
}

export async function writeVpyFile(_, vpyPath: string, vpyContent: string, videoPath: string): Promise<void> {
  vpyContent = vpyContent
    .replace(new RegExp(MagicStr.VIDEO_PATH, 'g'), path.normalize(videoPath))
    .replace(new RegExp(MagicStr.EXTRA_MODEL_PATH, 'g'), getExtraSRModelPath())
  writeFileSync(vpyPath, vpyContent)
}
