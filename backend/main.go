package main

import (
	"encoding/json"
	"firestore-test/retrieve"
	"fmt"

	"github.com/gin-gonic/gin"
)

func main() {

	router := gin.Default()

	notislice := retrieve.GetNoti()
	for _, noti := range notislice {
		fmt.Println(noti)
	}

	output, _ := json.Marshal(notislice)

	router.GET("/test", func(c *gin.Context) {
		c.Data(200, "application/json", output)
	})

	router.Run(":8000")
}
