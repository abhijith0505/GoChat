package main

import (
"fmt"
"log"
"os"
"gopkg.in/mgo.v2"
"gopkg.in/mgo.v2/bson"
)

var MONGODB_URL string = "mongodb://localhost:27017/goChat"

type Profile struct {
    Name string
    UserName string
}

func addSelf() {
    session, err := mgo.Dial(MONGODB_URL)
    if err != nil {
        panic(err)
    }
    defer session.Close()
    session.SetMode(mgo.Monotonic, true)

    var name,username string
    fmt.Println("Enter your name:")
    fmt.Scanf("%s", &name)
    fmt.Println("Enter your username:")
    fmt.Scanf("%s", &username)

    c := session.DB("goChat").C("profile")

    index := mgo.Index{
        Key: []string{"username"},
        Unique: true,
    }

    err = c.EnsureIndex(index)
    if err != nil {
        panic(err)
    }
    err = c.Insert(&Profile{name, username})
    if err != nil {
        log.Fatal(err)
    }

    result := Profile{}
    err = c.Find(bson.M{"username": username}).One(&result)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Name: ", result.Name, "        UserName: ", result.UserName)
}


func main() {
   

    if _, err := os.Stat("oneTimerFlag"); os.IsNotExist(err) {
        addSelf()
        f, err := os.Create("oneTimerFlag")
        if err != nil {
            log.Fatal(err)
        }

        defer f.Close()
    }else{
        fmt.Println("You are logged in as")
    }

    
}
