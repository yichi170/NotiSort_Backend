package retrieve

import (
	"context"
	"log"
	"strings"

	firebase "firebase.google.com/go"
	"google.golang.org/api/iterator"
	"google.golang.org/api/option"
)

func GetNoti() []map[string]string {

	opt := option.WithCredentialsFile("./retrieve/intnoti-cc829-firebase-adminsdk-4abey-00f37cb945.json")
	app, err := firebase.NewApp(context.Background(), nil, opt)
	if err != nil {
		log.Fatalln(err)
	}

	ctx := context.Background()

	client, err := app.Firestore(ctx)
	if err != nil {
		log.Fatalln(err)
	}

	iter := client.Collection("notifications").Documents(ctx)

	mapslice := make([]map[string]string, 0)

	for {
		doc, err := iter.Next()
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Fatalf("Failed to iterate: %v", err)
		}
		perposition := "\t\t\t\t\t\t\t\t"
		content := strings.Split(doc.Data()["content"].(string), perposition)
		for _, c := range content {
			notimap := map[string]string{}
			notimap["appName"] = doc.Data()["appName"].(string)
			notimap["title"] = doc.Data()["title"].(string)
			notimap["content"] = c
			mapslice = append(mapslice, notimap)
		}

	}

	defer client.Close()
	return mapslice
}
