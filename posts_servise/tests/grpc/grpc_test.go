package tests

import (
	"context"
	"log"
	"testing"

	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/handlers"
	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/repository"

	"github.com/stretchr/testify/assert"

	pb "github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/pkg"

	"github.com/testcontainers/testcontainers-go"
	"github.com/testcontainers/testcontainers-go/modules/mongodb"
)


func TestGrpcCreateGet(t* testing.T) {
	ctx := context.Background()

	mongoDB, err := mongodb.RunContainer(ctx, testcontainers.WithImage("mongo"))

	if err != nil {
		log.Fatal(err)
	}

	defer func() {
		err := mongoDB.Terminate(ctx) 
		if err != nil {
			log.Fatal(err)
		}
	}()

	db_link, err := mongoDB.ConnectionString(ctx)

	if err != nil {
		log.Fatal(err)
	}


	repo := repository.NewPostsRepository(db_link)

	hand := handlers.NewServer(repo)

	create_body := &pb.CreateRequest{
		UserId: 1,
		Title: "test",
		Body: "test",
	}

	response, err := hand.CreatePost(context.Background(), create_body)

	assert.Equal(t, err, nil)

	get_body := &pb.GetById{
		Id: response.Id,
		UserId: 0,
	}

	post, err := hand.GetByIdPost(context.Background(), get_body)

	assert.Equal(t, err, nil)
	assert.Equal(t, post.Body, "test")
}
