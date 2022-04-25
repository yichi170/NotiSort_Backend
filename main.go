package main

import (
	"encoding/json"
	"firestore-test/retrieve"
	"fmt"

	"github.com/gin-gonic/gin"
)

func main() {

	fmt.Println("main")
	notislice := retrieve.GetNoti()
	for _, noti := range notislice {
		fmt.Println(noti)
	}

	router := gin.Default()
	// router.GET("/test", test)
	output, _ := json.Marshal(notislice)

	router.GET("/test", func(c *gin.Context) {

		// fmt.Println(string(output))

		c.Data(200, "application/json", output)
	})

	router.Run(":8000")
}
