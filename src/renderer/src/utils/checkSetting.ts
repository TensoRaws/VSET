import useOutputconfigStore from '@renderer/store/OutputStore'
import useVfisettingconfigStore from '@renderer/store/VfiSettingsStore'
import { storeToRefs } from 'pinia'

export function CheckSetting(): boolean {
  const VfiSettingStore = useVfisettingconfigStore()
  const OutputConfigStore = useOutputconfigStore()

  const {
    useVfi,
    RifeModelValue,
    RifeScaleValue,
    RifeEnsembleValue,
  } = storeToRefs(VfiSettingStore)
  const {
    outputfolder,
  } = storeToRefs(OutputConfigStore)

  if (!outputfolder.value) {
    return false// 终止后续执行
  }

  if (useVfi.value === true) {
    // ensemble参数判断
    if (RifeEnsembleValue.value === true) {
      if (RifeModelValue.value === 'v4_21' || RifeModelValue.value === 'v4_22' || RifeModelValue.value === 'v4_22_lite' || RifeModelValue.value === 'v4_23'
        || RifeModelValue.value === 'v4_25' || RifeModelValue.value === 'v4_25_lite' || RifeModelValue.value === 'v4_25_heavy' || RifeModelValue.value === 'v4_26'
        || RifeModelValue.value === 'v4_26_heavy') {
        return false// 终止后续执行
      }
      if (RifeScaleValue.value !== 1.0) {
        return false// 终止后续执行
      }
    }
    // 光流参数判断
    if (RifeScaleValue.value !== 1) {
      if (RifeModelValue.value !== 'v4_0' && RifeModelValue.value !== 'v4_2' && RifeModelValue.value !== 'v4_3'
        && RifeModelValue.value !== 'v4_4' && RifeModelValue.value !== 'v4_5' && RifeModelValue.value !== 'v4_6') {
        return false// 终止后续执行}
      }
    }
  }
  return true
}
