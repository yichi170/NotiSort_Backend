package main

import (
	"firestore-test/retrieve"
	"fmt"
)

func main() {

	fmt.Println("main")
	notislice := retrieve.GetNoti()
	for _, noti := range notislice {
		fmt.Println(noti)
	}
}
