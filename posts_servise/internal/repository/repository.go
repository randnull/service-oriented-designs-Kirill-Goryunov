package repository

import (
	"context"
	"log"

	"github.com/randnull/service-oriented-designs-Kirill-Goryunov/posts_servise/modals"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)


type PostsRepository struct {
	dbCollection *mongo.Collection
}


func NewPostsRepository(URI string) *PostsRepository {
	client, err := mongo.NewClient(options.Client().ApplyURI(URI))

	if err != nil {
		log.Fatal(err)
	}

	err = client.Connect(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}

	mongoDb := client.Database("posts")
	collectionTrip := mongoDb.Collection("post")

	log.Println("Database is ready!")

	return &PostsRepository{
		dbCollection: collectionTrip,
	}
}


func (storage *PostsRepository) Create(post modals.PostData) (string, error) {
	result, err := storage.dbCollection.InsertOne(context.TODO(), post)
	if err != nil {
		return "", err
	}

	resp_id, _ := result.InsertedID.(primitive.ObjectID)

	resp_id_str := resp_id.Hex()
	
	return resp_id_str, nil
}


func (storage *PostsRepository) Delete(id string, user_id int) error {
	objectID, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return err
    }

	filter := bson.M{"_id": objectID, "userid": user_id}

	_, err = storage.dbCollection.DeleteOne(context.TODO(), filter)
    if err != nil {
        return err
    }

	return nil
}


func (storage *PostsRepository) GetById(id string, user_id int) (*modals.PostDataWithId, error) {
	objectID, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return nil, err
    }

	filter := bson.M{"_id": objectID} // "userid": user_id

	var post modals.PostDataWithId

    err = storage.dbCollection.FindOne(context.TODO(), filter).Decode(&post)
    if err != nil {
        return nil, err
    }

    return &post, nil
}


func (storage *PostsRepository) Update(id string, user_id int, new_title string, new_body string) error {
	objectID, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return err
    }

	filter := bson.M{"_id": objectID, "userid": user_id}
	update := bson.M{"$set": bson.M{"title": new_title, "body": new_body}}
	_, err = storage.dbCollection.UpdateOne(context.TODO(), filter, update)

	if err != nil {
        return err
    }

	return nil
}


func (storage *PostsRepository) GetAll(user_id int) ([]modals.PostDataWithId, error) {
	cur, err := storage.dbCollection.Find(context.TODO(), bson.M{"userid": user_id})

	if err != nil {
		return nil, err
	}

	var posts []modals.PostDataWithId

	for cur.Next(context.TODO()) {
		var post modals.PostDataWithId
		err := cur.Decode(&post)
		if err != nil {
			return nil, err
		}
		posts = append(posts, post)
	}

	return posts, nil
}
