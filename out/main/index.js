"use strict";
const electron$1 = require("electron");
const path$1 = require("path");
const utils = require("@electron-toolkit/utils");
const child_process = require("child_process");
const util = require("util");
const si = require("systeminformation");
const icon = path$1.join(__dirname, "../../resources/icon.png");
const electron = require("electron");
const appPath$1 = electron.app.getAppPath();
const fs$1 = require("fs");
const exec = util.promisify(child_process.exec);
function generate_cmd(config_json, vipipePath, vpyPath, ffmpegPath, video) {
  let cmd = '"' + vipipePath + '" "-c" "y4m" "' + vpyPath + '" "-" | "' + ffmpegPath + '" "-hide_banner" "-y" "-i" "pipe:" "-i" "' + video + '" "-map" "0:v:0" "-map" "1:a" "-c:v" "' + config_json.encoderValue + '" ';
  if (config_json.encoderValue == "libx265") {
    cmd += '"-pix_fmt" "yuv420p10le" "-profile:v" "main10" "-vtag" "hvc1" ';
  }
  if (config_json.encoderValue == "libx264") {
    cmd += '"-pix_fmt" "yuv420p" "-profile:v" "main" ';
  }
  if (config_json.encoderValue == "libaom-av1") {
    cmd += '"-pix_fmt" "yuv420p10le" ';
  }
  if (config_json.encoderValue == "h264_nvenc") {
    cmd += '"-pix_fmt" "yuv420p" ';
  }
  if (config_json.encoderValue == "hevc_nvenc") {
    cmd += '"-pix_fmt" "p010le" "-profile:v" "main10" "-vtag" "hvc1" ';
  }
  if (config_json.encoderValue == "av1_nvenc") {
    cmd += '"-pix_fmt" "p010le" ';
  }
  cmd += '-preset "' + config_json.qualityValue + '" ';
  if (config_json.isUseCrf == true) {
    cmd += '"-crf" "' + config_json.crfValue + '" ';
  } else {
    cmd += '"-b:v" "' + config_json.bitValue + 'M" ';
  }
  if (config_json.isSaveAudio == true) {
    cmd += '"-c:a" "copy" ';
  } else {
    cmd += '"-c:a" "' + config_json.AudioContainer.toLowerCase() + '" ';
  }
  cmd += '"' + config_json.outputfolder + "/" + path$1.parse(path$1.basename(video)).name + "_enhance." + config_json.videoContainer.toLowerCase() + '"';
  return cmd;
}
function generate_vpy(config_json, videoName) {
  let vpyContent = "";
  vpyContent += "import vapoursynth as vs\n";
  vpyContent += "core = vs.core\n";
  vpyContent += 'res = core.lsmas.LWLibavSource(r"' + videoName + '")\n';
  if (config_json.UseResize_BeforeEnhance == true) {
    vpyContent += "res = core.resize.Bicubic(clip=res,width=" + config_json.ResizeWidth_BeforeEnhance + ",height=" + config_json.ResizeHeight_BeforeEnhance + ",format=vs.YUV420P16)\n";
  } else {
    vpyContent += "res = core.resize.Bicubic(clip=res,format=vs.YUV420P16)\n";
  }
  vpyContent += "res = core.std.Crop(clip=res,left=" + config_json.ReduceLeft_BeforeEnhance + ", right=" + config_json.ReduceRight_BeforeEnhance + ", top=" + config_json.ReduceOn_BeforeEnhance + ", bottom=" + config_json.ReduceDown_BeforeEnhance + ")\n";
  if (config_json.useSR == true) {
    vpyContent += 'res = core.resize.Bicubic(clip=res,range=1,matrix_in_s="709",format=vs.RGB48)\n';
    vpyContent += "res=core.fmtc.bitdepth(res, bits=32)\n";
    vpyContent += "from vsmlrt import CUGAN,RealESRGAN,Waifu2x,RIFE,Backend\n";
    if (config_json.RealcuganInferenceValue == "Cuda") {
      vpyContent += "device_sr=Backend.ORT_CUDA()\n";
    }
    if (config_json.RealcuganInferenceValue == "TensorRt") {
      vpyContent += "device_sr=Backend.TRT()\n";
    }
    if (config_json.RealcuganInferenceValue == "NCNN") {
      vpyContent += "device_sr=Backend.NCNN_VK()\n";
    }
    if (config_json.RealcuganInferenceValue == "OV") {
      vpyContent += "device_sr=Backend.OV_GPU()\n";
    }
    vpyContent += "device_sr.device_id=0\n";
    vpyContent += "device_sr.fp16=True\n";
    if (config_json.SRMethodValue == "Real_cugan") {
      const model_switch = {
        "pro-conservative-up2x": [0, 2, 2],
        "pro-conservative-up3x": [0, 3, 2],
        "pro-denoise3x-up2x": [3, 2, 2],
        "pro-denoise3x-up3x": [3, 3, 2],
        "pro-no-denoise3x-up2x": [-1, 2, 2],
        "pro-no-denoise3x-up3x": [-1, 3, 2],
        "up2x-latest-conservative": [0, 2, 1],
        "up2x-latest-denoise1x": [1, 2, 1],
        "up2x-latest-denoise2x": [2, 2, 1],
        "up2x-latest-denoise3x": [3, 2, 1],
        "up2x-latest-no-denoise": [-1, 2, 1],
        "up3x-latest-conservative": [0, 3, 1],
        "up3x-latest-denoise3x": [3, 3, 1],
        "up3x-latest-no-denoise": [-1, 3, 1],
        "up4x-latest-conservative": [0, 4, 1],
        "up4x-latest-denoise3x": [3, 4, 1],
        "up4x-latest-no-denoise": [-1, 4, 1]
      };
      const [noise, scale, version] = model_switch[config_json.RealcuganModelValue] || [0, 2, 2];
      vpyContent += `res = CUGAN(res, noise=${noise}, scale=${scale}, tiles=${config_json.RealcuganTileValue}, version=${version}, alpha=${config_json.RealcuganAlphaValue}, backend=device_sr)
`;
    }
    if (config_json.SRMethodValue == "Real_esrgan") {
      const model_switch = {
        "animevideov3": 0,
        "animevideo-xsx2": 1,
        "animevideo-xsx4": 2,
        "animejanaiV2L1": 5005,
        "animejanaiV2L2": 5006,
        "animejanaiV2L3": 5007,
        "animejanaiV3_HD_L1": 5008,
        "animejanaiV3_HD_L2": 5009,
        "animejanaiV3_HD_L3": 5010
      };
      const model = model_switch[config_json.RealesrganModelValue] || 0;
      vpyContent += "res = RealESRGAN(res, scale=" + config_json.RealesrganScaleValue + ",tiles=" + config_json.RealesrganTileValue + ",model=" + model + ", backend=device_sr)\n";
    }
  }
  if (config_json.UseResize_AfterEnhance == true) {
    vpyContent += "res = core.resize.Bicubic(clip=res,width=" + config_json.ResizeWidth_AfterEnhance + ",height=" + config_json.ResizeHeight_AfterEnhance + ',matrix_s="709", format=vs.YUV420P16)\n';
  } else {
    vpyContent += 'res = core.resize.Bicubic(clip=res, matrix_s="709", format=vs.YUV420P16)\n';
  }
  vpyContent += "res = core.std.Crop(clip=res,left=" + config_json.ReduceLeft_AfterEnhance + ", right=" + config_json.ReduceRight_AfterEnhance + ", top=" + config_json.ReduceOn_AfterEnhance + ", bottom=" + config_json.ReduceDown_AfterEnhance + ")\n";
  vpyContent += "res.set_output()\n";
  return vpyContent;
}
async function RunCommand(event, config_json) {
  const videos = config_json.fileList;
  const vipipePath = path$1.join(appPath$1, "package", "VSPipe.exe");
  const ffmpegPath = path$1.join(appPath$1, "package", "ffmpeg.exe");
  const ffprobePath = path$1.join(appPath$1, "package", "ffprobe.exe");
  for (const video of videos) {
    try {
      const baseName = path$1.basename(video, path$1.extname(video));
      const vpyPath = path$1.join(appPath$1, "vpyFiles", `${baseName}.vpy`);
      const ffprobeCommand = `"${ffprobePath}" -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate,nb_frames -of json "${video}"`;
      const { stdout: probeOut } = await exec(ffprobeCommand);
      const metadata = JSON.parse(probeOut);
      const videoStream = metadata.streams?.[0];
      if (videoStream) {
        const frameCount = videoStream.nb_frames || "未知";
        const frameRate = videoStream.avg_frame_rate || "未知";
        const resolution = `${videoStream.width}x${videoStream.height}`;
        event.sender.send("ffmpeg-output", `正在处理输入视频 ${video} 的信息:
`);
        event.sender.send("ffmpeg-output", `帧数(输入): ${frameCount}
`);
        event.sender.send("ffmpeg-output", `帧率(输入): ${frameRate}
`);
        event.sender.send("ffmpeg-output", `分辨率(输入): ${resolution}
`);
      }
      const vpyFile = generate_vpy(config_json, video);
      fs$1.writeFileSync(vpyPath, vpyFile);
      const vspipeInfoCommand = `"${vipipePath}" --info "${vpyPath}"`;
      const { stdout: vspipeOut } = await exec(vspipeInfoCommand);
      const info = {
        width: vspipeOut.match(/Width:\s*(\d+)/)?.[1] || "未知",
        height: vspipeOut.match(/Height:\s*(\d+)/)?.[1] || "未知",
        frames: vspipeOut.match(/Frames:\s*(\d+)/)?.[1] || "0",
        fps: vspipeOut.match(/FPS:\s*([\d\/]+)\s*\(([\d.]+) fps\)/)?.[2] || "0"
      };
      event.sender.send("ffmpeg-output", `以下是视频的输出信息:
`);
      event.sender.send("ffmpeg-output", `Width: ${info.width}
`);
      event.sender.send("ffmpeg-output", `Height: ${info.height}
`);
      event.sender.send("ffmpeg-output", `Frames: ${info.frames}
`);
      event.sender.send("ffmpeg-output", `FPS: ${info.fps}
`);
      const cmd = generate_cmd(config_json, vipipePath, vpyPath, ffmpegPath, video);
      event.sender.send("ffmpeg-output", `Executing command: ${cmd}
`);
      await new Promise((resolve, reject) => {
        const renderProcess = child_process.spawn(cmd, { shell: true });
        renderProcess.stdout.on("data", (data) => {
          event.sender.send("ffmpeg-output", data.toString());
        });
        renderProcess.stderr.on("data", (data) => {
          const str = data.toString();
          const regex = /frame=\s*(-?\d+)\s+fps=\s*([\d.]+).+time=\s*(-?[\d:.]+)\s+bitrate=\s*(-?[\w/.-]+)/;
          const match = str.match(regex);
          if (match) {
            const [_, frame, fps, time, bitrate] = match;
            const totalFrames = parseInt(info.frames || "0", 10);
            const renderedFrames = parseInt(frame, 10);
            const currentFps = parseFloat(fps);
            const remainingFrames = totalFrames - renderedFrames;
            const estSeconds = remainingFrames / (currentFps || 1);
            const hours = Math.floor(estSeconds / 3600);
            const minutes = Math.floor(estSeconds % 3600 / 60);
            const seconds = Math.floor(estSeconds % 60);
            event.sender.send(
              "ffmpeg-output",
              `已渲染/总帧数: ${frame} / ${totalFrames} 速度(FPS): ${fps} 预计剩余时间：${hours}h ${minutes}min ${seconds}s 已渲染的时间长度: ${time} 比特率: ${bitrate}
`
            );
          } else {
            event.sender.send("ffmpeg-output", str);
          }
        });
        renderProcess.on("close", () => {
          event.sender.send("ffmpeg-output", "finish\n");
          resolve();
        });
        renderProcess.on("error", (err) => {
          reject(err);
        });
      });
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error);
      event.sender.send("ffmpeg-output", `处理视频 ${video} 时出错: ${errMsg}
`);
    }
  }
  event.sender.send("ffmpeg-finish");
}
const selectDirectory = async () => {
  const res = await electron$1.dialog.showOpenDialog({
    title: "选择文件夹",
    properties: ["openDirectory", "createDirectory"]
  });
  return res.canceled === false ? res.filePaths[0].replace(/\\/g, "/") : "";
};
async function getGpuInfo() {
  const deviceList = [];
  const gpus = await si.graphics();
  for (const i in gpus.controllers) {
    deviceList.push(gpus.controllers[i].model);
  }
  return deviceList;
}
async function getCpuInfo() {
  const cpu = await si.cpu();
  return cpu.brand;
}
const ipc = (_win) => {
  electron$1.ipcMain.handle("selectDirectory", async () => {
    return selectDirectory();
  });
  electron$1.ipcMain.handle("getGpuInfo", async () => {
    return getGpuInfo();
  });
  electron$1.ipcMain.handle("getCpuInfo", async () => {
    return getCpuInfo();
  });
};
const appPath = electron$1.app.getAppPath();
const path = require("path");
const fs = require("fs");
function createWindow() {
  const mainWindow = new electron$1.BrowserWindow({
    width: 900,
    height: 670,
    minWidth: 900,
    minHeight: 670,
    show: false,
    autoHideMenuBar: true,
    ...process.platform === "linux" ? { icon } : {},
    webPreferences: {
      preload: path$1.join(__dirname, "../preload/index.js"),
      sandbox: false
    }
  });
  mainWindow.on("ready-to-show", () => {
    mainWindow.show();
  });
  mainWindow.webContents.setWindowOpenHandler((details) => {
    electron$1.shell.openExternal(details.url);
    return { action: "deny" };
  });
  if (utils.is.dev && process.env["ELECTRON_RENDERER_URL"]) {
    mainWindow.loadURL(process.env["ELECTRON_RENDERER_URL"]);
  } else {
    mainWindow.loadFile(path$1.join(__dirname, "../renderer/index.html"));
  }
  return mainWindow;
}
electron$1.app.whenReady().then(() => {
  utils.electronApp.setAppUserModelId("com.electron");
  electron$1.app.on("browser-window-created", (_, window) => {
    utils.optimizer.watchWindowShortcuts(window);
  });
  electron$1.ipcMain.on("execute-command", RunCommand);
  electron$1.ipcMain.on("generate-json", (_, data) => {
    const filePath = path.join(appPath, "json", "setting.json");
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  });
  electron$1.ipcMain.on("open-folder-dialog", (event) => {
    electron$1.dialog.showOpenDialog({
      properties: ["openDirectory"]
    }).then((result) => {
      if (!result.canceled) {
        event.sender.send("selected-folder", result.filePaths[0]);
      }
    }).catch((err) => {
      console.error("Error opening folder dialog:", err);
    });
  });
  electron$1.ipcMain.on("ping", () => console.log("pong"));
  electron$1.ipcMain.on("upload-file", (_, filePath) => {
    console.log("File path:", filePath);
  });
  createWindow();
  ipc();
  electron$1.app.on("activate", function() {
    if (electron$1.BrowserWindow.getAllWindows().length === 0) {
      createWindow();
      ipc();
    }
  });
});
electron$1.app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    electron$1.app.quit();
  }
});
