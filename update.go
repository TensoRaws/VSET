package main

import (
	"bytes"
	"fmt"
	"github.com/gen2brain/go-unarr"
	"github.com/tidwall/gjson"
	"io"
	"net/http"
	"os"
	"path"
)

var GithubrpHost = "https://git.114514.lol/"           // 反代GitHub域名
var GithubAPIrpHost = "https://api-github.114514.lol/" // 反代GitHub API
// rp -- reverse proxy

func getCurrentVersion() []string {
	repositoryVset := "v1.0."
	repositoryVsVsmlrt := "v1.0"
	repositoryVsPytorch := "v1.0.0"
	return []string{repositoryVset, repositoryVsVsmlrt, repositoryVsPytorch}
}

func getLastestVersion() []string {
	getVersion := func(url string) string {
		res, err := http.Get(url)
		if err != nil {
			return "-114514"
		}
		defer res.Body.Close()
		buffer := bytes.NewBuffer(make([]byte, 4096))
		_, err = io.Copy(buffer, res.Body)
		if err != nil {
			return "-114514"
		}
		return gjson.Get(buffer.String(), "tag_name").String()
	}
	// https://api.github.com/repos/Tohrusky/VSET/releases/latest
	repository1 := GithubAPIrpHost + "repos/Tohrusky/VSET/releases/latest"
	repository2 := GithubAPIrpHost + "repos/Tohrusky/vs_vsmlrt/releases/latest"
	repository3 := GithubAPIrpHost + "repos/Tohrusky/vs_pytorch/releases/latest"
	return []string{getVersion(repository1), getVersion(repository2), getVersion(repository3)}
}

func getDownloadLink(version []string) []string {
	repositoryVset := GithubrpHost + "Tohrusky/VSET/releases/download/" + version[0] + "/VSET.zip"
	// https://github.com/Tohrusky/VSET/releases/download/v1.0.0/VSET.zip
	repositoryVsVsmlrt := GithubrpHost + "Tohrusky/vs_vsmlrt/releases/download/" + version[1] + "/vs_vsmlrt.7z"
	// https://github.com/Tohrusky/vs_vsmlrt/releases/download/v1.0.0/vs_vsmlrt.7z
	repositoryVsPytorch := GithubrpHost + "Tohrusky/vs_pytorch/releases/download/" + version[2] + "/vs_pytorch.7z"
	// https://github.com/Tohrusky/vs_pytorch/releases/download/v1.0.0/vs_pytorch.7z
	return []string{repositoryVset, repositoryVsVsmlrt, repositoryVsPytorch}
}

// MyDownloader 下载器结构体，实现io.Reader接口
type MyDownloader struct {
	io.Reader
	TotalSize   int64
	CurrentSize int64
}

// 实现Read方法
func (d *MyDownloader) Read(p []byte) (n int, err error) {
	n, err = d.Reader.Read(p)
	d.CurrentSize += int64(n)
	fmt.Printf("\r正在下载，下载进度：%.2f%%", float64(d.CurrentSize*10000/d.TotalSize)/100)
	if d.CurrentSize == d.TotalSize {
		fmt.Printf("\r下载完成，下载进度：%.2f%%", float64(d.CurrentSize*10000/d.TotalSize)/100)
	}
	return
}

func downloadFile(url string, p string) {
	deleteDLfile := func() {
		if err := os.RemoveAll(path.Join(p, "tempdl")); err != nil {
			fmt.Println("删除下载文件失败")
		}
	}
	file, err := os.OpenFile(path.Join(p, "tempdl"), os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("创建下载文件失败")
		panic(err)
	}
	defer file.Close()
	resp, err := http.Get(url)
	if err != nil {
		fmt.Println("    ||    下载文件失败，请检查网络是否稳定，建议开启tun/tap模式")
		deleteDLfile()
		panic(err)
	}
	defer resp.Body.Close()

	myDownloader := &MyDownloader{
		Reader:    resp.Body,
		TotalSize: resp.ContentLength,
	}
	if _, err := io.Copy(file, myDownloader); err != nil {
		fmt.Println("    ||    下载文件失败，请检查网络是否稳定，建议开启tun/tap模式")
		deleteDLfile()
		panic(err)
	}
}

func main() {
	MyDirPath, _ := os.Getwd()
	CurrentVersion := getCurrentVersion()
	LastestVersion := getLastestVersion()
	DownloadLink := getDownloadLink(LastestVersion)

	pgName := [][]string{{"VSET主程序", "VSET.zip"}, {"vs_vsmlrt环境包", "vs_vsmlrt.7z"}, {"vs_pytorch环境包", "vs_pytorch.7z"}}
	cnt := 0
	for i := 0; i < 3; i++ {
		if LastestVersion[i] != CurrentVersion[i] {
			cnt++

			fmt.Println(pgName[i][0] + " 当前版本" + CurrentVersion[i] + "，" +
				"有新版本" + LastestVersion[i] + "，按回车键开始下载")
			_, scanln := fmt.Scanln()
			if scanln != nil {
				return
			}

			downloadFile(DownloadLink[i], MyDirPath)

			_ = os.Rename(path.Join(MyDirPath, "tempdl"), path.Join(MyDirPath, pgName[i][1]))
			DownloadFile, err := unarr.NewArchive(path.Join(MyDirPath, pgName[i][1]))
			if err != nil {
				panic(err)
			}
			_, err = DownloadFile.Extract(MyDirPath)
			if err != nil {
				panic(err)
			}

			DownloadFile.Close()

			fmt.Println("    ||    解压完成，要删除下载的压缩包吗？（y/n）")
			var scan string
			_, scanln = fmt.Scanln(&scan)
			if scanln != nil {
				return
			}
			if scan == "y" {
				err = os.RemoveAll(path.Join(MyDirPath, pgName[i][1]))
				if err != nil {
					panic(err)
				}
			}
		}
	}
	if cnt == 0 {
		fmt.Println("Ciallo~~恭喜你呀，当前已是最新版本")
	}
}
