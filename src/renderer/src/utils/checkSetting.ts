import useOutputconfigStore from '@renderer/store/OutputStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'
import { storeToRefs } from 'pinia'

export function CheckSetting(): true | string {
  const VfiSettingStore = useVfisettingconfigStore()
  const OutputConfigStore = useOutputconfigStore()

  const {
    useVfi,
    RifeModelValue,
    RifeScaleValue,
    RifeEnsembleValue,
  } = storeToRefs(VfiSettingStore)
  const {
    outputFolder,
  } = storeToRefs(OutputConfigStore)

  if (!outputFolder.value) {
    return '输出文件夹为空，无法启动渲染流程'
  }

  if (useVfi.value === true) {
    // ensemble参数判断
    if (RifeEnsembleValue.value === true) {
      if (RifeModelValue.value === 'v4_21' || RifeModelValue.value === 'v4_22' || RifeModelValue.value === 'v4_22_lite' || RifeModelValue.value === 'v4_23'
        || RifeModelValue.value === 'v4_25' || RifeModelValue.value === 'v4_25_lite' || RifeModelValue.value === 'v4_25_heavy' || RifeModelValue.value === 'v4_26'
        || RifeModelValue.value === 'v4_26_heavy') {
        return '该模型不支持ensemble模式'
      }
      if (RifeScaleValue.value !== 1.0) {
        return 'ensemble模式下，该模型的光流参数只能设置为1.0'
      }
    }
    // 光流参数判断
    if (RifeScaleValue.value !== 1.0) {
      if (RifeModelValue.value !== 'v4_0' && RifeModelValue.value !== 'v4_2' && RifeModelValue.value !== 'v4_3'
        && RifeModelValue.value !== 'v4_4' && RifeModelValue.value !== 'v4_5' && RifeModelValue.value !== 'v4_6') {
        return '模型4.0, 4.2, 4.3, 4.4, 4.5,4.6以外的模型的光流参数只能设置为1'
      }
    }
  }
  return true
}
