package main

import (
	"io"
	"net/http"
	"os"
)

func get_repository_url() []string {
	repository_1 := "https://github.com/Tohrusky/VSET/releases/download/v1.0.0/VSET.zip"
	repository_2 := ""
	repository_3 := ""
	var res = []string{repository_1, repository_2, repository_3}
	return res
}

func downLoadFile(url string, path string) (len int, err error) {
	//err write /dev/null: bad file descriptor#
	out, err := os.OpenFile("path/out.zip", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	defer out.Close()
	resp, err := http.Get(url)
	defer resp.Body.Close()
	n, err := io.Copy(out, resp.Body)
	return int(n), err
}

func main() {
	str, _ := os.Getwd()
	file, err := downLoadFile("https://github.com/Tohrusky/VSET/releases/download/v1.0.0/VSET.zip", str)
	if err != nil {
		return
	}
	print(file)
}
