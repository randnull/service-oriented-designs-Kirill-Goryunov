package modals

import (
	"time"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type PostData struct {
	UserId 		int
	Body    	string
	Title   	string
	CreatedAt 	time.Time
}

type PostDataWithId struct {
	ObjectID 	primitive.ObjectID `bson:"_id"`
	UserId 		int
	Body    	string
	Title   	string
	CreatedAt 	time.Time
}


type UpdatePost struct {
	UserId 		int
	Body    	string
	Title   	string
}
