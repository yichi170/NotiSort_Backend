package main

import (
	"fmt"
	"flag"
	"context"
	"log"
	"google.golang.org/api/iterator"
	"cloud.google.com/go/firestore"

	"google.golang.org/api/option"
	firebase "firebase.google.com/go"
)

func createClient(ctx context.Context) *firestore.Client {
	projectID := "intnoti-cc829"

	flag.StringVar(&projectID, "project", projectID, "intnoti project ID.")
	flag.Parse()

	client, err := firestore.NewClient(ctx, projectID)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}

	return client
}

func main() {

	opt := option.WithCredentialsFile("./intnoti-cc829-firebase-adminsdk-4abey-00f37cb945.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		log.Fatalln(err)
	}

	ctx := context.Background()
	
	// client := createClient(ctx)
	
	client, err := app.Firestore(ctx)
	if err != nil {
		log.Fatalln(err)
	}

	iter := client.Collection("notifications").Documents(ctx)
	for {
		doc, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatalf("Failed to iterate: %v", err)
		}
		fmt.Println(doc.Data())
	}

	defer client.Close()
}