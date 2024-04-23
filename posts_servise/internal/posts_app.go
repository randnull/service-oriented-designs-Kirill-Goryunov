package posts_app

import (
	"log"
	"net"
	"os"
	"fmt"
	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/repository"
	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/handlers"
	pb "github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/pkg"
	"google.golang.org/grpc"
)


type App struct {
	server *handlers.Server
}


func NewApp() *App {
	database_host := os.Getenv("HOST_DATABASE")
	database_port := os.Getenv("PORT_DATABASE")

	db_link := fmt.Sprintf("mongodb://%s:%s", database_host, database_port)

	repo := repository.NewPostsRepository(db_link)
	server := handlers.NewServer(repo)

	apl := &App{
		server: server,
	}
	return apl
}


func (a* App) Run() {
	port := os.Getenv("PORT_SERVISE")

	serv_link := fmt.Sprintf(":%s", port)

	lis, err := net.Listen("tcp", serv_link)

	if err != nil {
		log.Fatal("server failed")
	}

	s := grpc.NewServer()

	pb.RegisterPostsServiceServer(s, a.server)

	log.Printf("server listening : %s", port)

	if err := s.Serve(lis); err != nil {
		log.Fatal("server failed")
	}
}
