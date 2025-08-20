import vapoursynth as vs
core = vs.core
res = core.lsmas.LWLibavSource(r"D:/code/压缩包/output.mp4")
from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend
import vsmlrt
res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)
res = core.std.Crop(clip=res,left=0, right=0, top=0, bottom=0)
res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)
res=core.fmtc.bitdepth(res, bits=32)
device_sr=Backend.ORT_CUDA()
device_sr.device_id=0
device_sr.fp16=True
device_sr.num_streams=1
res = RealESRGAN(res, scale=2,tiles=1,model=5010, backend=device_sr)
res = core.resize.Bicubic(clip=res, matrix_s="709", format=vs.YUV420P16)
res = core.std.Crop(clip=res,left=0, right=0, top=0, bottom=0)
res.set_output()
