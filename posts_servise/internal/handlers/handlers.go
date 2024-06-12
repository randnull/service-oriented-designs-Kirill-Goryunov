package handlers

import (
	"context"
	"sort"
	"time"

	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/modals"
	pb "github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/pkg"
	"google.golang.org/protobuf/types/known/timestamppb"
)

//go:generate mockgen -source=handlers.go -destination=mock/handlers.go

type RepositoryInterface interface {
	Create(post modals.PostData) (string, error)
	Delete(id string, user_id int) error
	GetById(id string, user_id int) (*modals.PostDataWithId, error)
	Update(id string, user_id int, new_title string, new_body string) error
	GetAll(user_id int) ([]modals.PostDataWithId, error)
}


type Server struct {
	repo   RepositoryInterface
	pb.UnimplementedPostsServiceServer
}


func NewServer(repo RepositoryInterface) *Server {
	return &Server{
		repo: repo,
	}
}

func min(a int, b int) int {
	if a > b {
		return a
	}
	return b
}


func (s *Server) CreatePost(ctx context.Context, in *pb.CreateRequest) (*pb.CreateResponse, error) {
	post_data := modals.PostData{
		UserId: int(in.UserId),
		Body: in.Body,
		Title: in.Title,
		CreatedAt: time.Now(),
	}
	
	id, _ := s.repo.Create(post_data)
	
	return &pb.CreateResponse{Id: id}, nil
}


func (s *Server) DeletePost(ctx context.Context, in *pb.DeleteRequest) (*pb.Response, error) {
	_ = s.repo.Delete(in.Id, int(in.UserId))	
	
	return &pb.Response{Status: 0}, nil
}


func (s *Server) GetByIdPost(ctx context.Context, in *pb.GetById) (*pb.Post, error) {
	post, err := s.repo.GetById(in.Id, int(in.UserId))

	status := 0

	if err != nil {
		status = 1
		postAnswer := &pb.Post {
			Id:			"",
			UserId: 	0,
			Title:  	"",
			Body: 		"",
			CreatedAt: 	timestamppb.New(time.Now()),
			Status:		int64(status),
		}
		return postAnswer, nil
	} 

	postAnswer := &pb.Post {
		Id:			post.ObjectID.Hex(),
		UserId: 	int64(post.UserId),
		Title:  	post.Title,
		Body: 		post.Body,
		CreatedAt: 	timestamppb.New(post.CreatedAt),
		Status:		int64(status),
	}

	return postAnswer, nil
}


func (s *Server) UpdatePost(ctx context.Context, in *pb.UpdateRequest) (*pb.Response, error) {
	err := s.repo.Update(in.Id, int(in.UserId), in.Title, in.Body)

	if err != nil {
		return &pb.Response{Status: 1}, nil
	}

	return &pb.Response{Status: 0}, nil
}


func (s *Server) GetAllPost(ctx context.Context, in *pb.GetAllRequest) (*pb.GetAllResponse, error) {
	posts, err := s.repo.GetAll(int(in.UserId))

	var postsformatted []*pb.Post

	if err != nil {
		return &pb.GetAllResponse{Posts: postsformatted}, nil
	}

	sort.Slice(posts, func(i, j int) bool {
		return posts[i].CreatedAt.Before(posts[j].CreatedAt)
	})

	start := int((in.PageNumber - 1) * in.PageSize)
	end := min((start + int(in.PageSize)), len(posts))

	if len(posts) < start {
		return &pb.GetAllResponse{Posts: postsformatted}, nil
	}

	posts = posts[start:end]

	for i:=0;i<len(posts);i++ {
		status := 0
		formatpost := &pb.Post {
			Id:			posts[i].ObjectID.Hex(),
			UserId: 	int64(posts[i].UserId),
			Title:  	posts[i].Title,
			Body: 		posts[i].Body,
			CreatedAt: 	timestamppb.New(posts[i].CreatedAt),
			Status:		int64(status),
		}
		postsformatted = append(postsformatted, formatpost)
	}

	return &pb.GetAllResponse{Posts: postsformatted}, nil
}
