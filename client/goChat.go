package main

import (
"fmt"
"log"
"os"
"bytes"
"net/http"
"gopkg.in/mgo.v2"
"gopkg.in/mgo.v2/bson"
"./variables"
)

type Profile struct {
    Name string
    UserName string
}

func addSelf() {
    session, err := mgo.Dial(variables.MONGODB_URL)
    if err != nil {
        panic(err)
    }
    defer session.Close()
    session.SetMode(mgo.Monotonic, true)

    fmt.Println("----------Sign Up-----------")

    var name,username,password,password2 string
    fmt.Println("Enter your name:")
    fmt.Scanf("%s", &name)
    fmt.Println("Enter your username:")
    fmt.Scanf("%s", &username)
    GOTO_passwordMatch:
    fmt.Println("Enter your password:")
    fmt.Scanf("%s", &password)
    fmt.Println("Enter your password again:")
    fmt.Scanf("%s", &password2)

    if password == password2{
        fmt.Println("Passwords match!")
    }else{
        fmt.Println("Passwords do not match!")
        goto GOTO_passwordMatch
    }
    url := variables.AWSEndPoint + "/register"

    var jsonprep string = "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}"
    var jsonStr = []byte(jsonprep)
    
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
    req.Header.Set("Content-Type", "application/json")

    client := http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        fmt.Println("Error creating!")
        panic(err)
    }else{
        fmt.Println("Created!")
    }
    defer resp.Body.Close()

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
   
    fmt.Println("###################################################### GOChatCLI ###################################################### ")

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
