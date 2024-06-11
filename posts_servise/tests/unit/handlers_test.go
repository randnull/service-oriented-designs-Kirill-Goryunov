package unit

import (
	"context"
	"testing"

	"errors"

	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"

	pb "github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/pkg"

	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/handlers"
	mock "github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/internal/handlers/mock"
)

func TestCreate(t *testing.T) {
	ctrl := gomock.NewController(t)

	repoMock := mock.NewMockRepositoryInterface(ctrl)

	hand := handlers.NewServer(repoMock)

	repoMock.EXPECT().Create(gomock.Any()).Return("1", nil).Times(1)

	req := &pb.CreateRequest{
		UserId: 5,
		Body:   "body",
		Title:  "title",
	}

	resp, err := hand.CreatePost(context.Background(), req)

	assert.Equal(t, err, nil)
	assert.Equal(t, resp.Id, "1")
}


func TestGetById(t *testing.T) {
	ctrl := gomock.NewController(t)

	repoMock := mock.NewMockRepositoryInterface(ctrl)

	hand := handlers.NewServer(repoMock)

	repoMock.EXPECT().GetById("0", 1).Return(nil, errors.New("some error")).Times(1)

	req := &pb.GetById{
		Id: "0",
		UserId: 1,
	}

	post, err := hand.GetByIdPost(context.Background(), req)

	assert.Equal(t, post.Id, "")
	assert.Equal(t, post.Title, "")
	assert.Equal(t, err, nil)
}
