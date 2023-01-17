package main

import (
	"bytes"
	"fmt"
	"github.com/tidwall/gjson"
	"io"
	"net/http"
	"os"
)

var GithubrpHost = "https://git.114514.lol/"           // 反代GitHub域名
var GithubAPIrpHost = "https://api-github.114514.lol/" // 反代GitHub API
// rp -- reverse proxy

func getCurrentVersion() []string {
	repositoryVset := "v1.0.0"
	repositoryVsVsmlrt := "v1.0.0"
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

func downloadFile(url string, path string) (len int, err error) {
	out, err := os.OpenFile("path/download", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	defer out.Close()
	resp, err := http.Get(url)
	defer resp.Body.Close()
	n, err := io.Copy(out, resp.Body)
	return int(n), err
}

func main() {
	//str, _ := os.Getwd()
	fmt.Println(getLastestVersion())
}
