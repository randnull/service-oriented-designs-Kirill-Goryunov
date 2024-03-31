package main

import (
	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal"
)


func main() {
	a := posts_app.NewApp()
	a.Run()
}
