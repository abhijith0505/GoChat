package main

import (
"fmt"
"log"
"syscall"
"os"
"bytes"
"net/http"
"os/signal"
"gopkg.in/mgo.v2"
"gopkg.in/mgo.v2/bson"
"./variables"
)
var name,username,password,password2 string


type Profile struct {
    Name string
    UserName string
    LoggedIn bool
}

func loginLogout(logged bool) {
    session, err := mgo.Dial(variables.MONGODB_URL)
    if err != nil {
        panic(err)
    }
    defer session.Close()
    session.SetMode(mgo.Monotonic, true)
    c := session.DB("goChat").C("profile")
    
    result := Profile{}
    err = c.Find(bson.M{"username": username}).One(&result)

    result.LoggedIn = logged
    
    colQuerier := bson.M{"username": username}
    change := bson.M{"$set": bson.M{"loggedin": result.LoggedIn}}
    err = c.Update(colQuerier, change)
    if err != nil {
        panic(err)
    }
    if(logged==true){
        fmt.Println("\nLogged In\n")
    }else{
        fmt.Println("\nLogged Out\n")
    }
}

func checkUser(username string) bool{
    var userPresent bool
        
    url := variables.AWSEndPoint + "/checkUser"

    var jsonprep string = "{\"username\":\"" + username + "\"}"
    var jsonStr = []byte(jsonprep)
    
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonStr))
    req.Header.Set("Content-Type", "application/json")

    client := http.Client{}
    resp, err := client.Do(req)

    if err != nil {
        panic(err)  
    }
    fmt.Println(resp)
    /*if(resp==false){
        userPresent=false
    }else{
        userPresent=true
    }*/
    //defer resp.Body.Close()

    return userPresent
}

func signIn() {
    fmt.Println("----------Sign In-----------")

    fmt.Println("Enter your username:")
    fmt.Scanf("%s", &username)
    var userPresent bool
    //userPresent = checkUser(username)
    userPresent=false
    if(userPresent==true){
        fmt.Println("Enter your password:")
        fmt.Scanf("%s", &password)
        loginLogout(true)
    }else{
        addSelf()
    }
}

func addSelf() {
    session, err := mgo.Dial(variables.MONGODB_URL)
    if err != nil {
        panic(err)
    }
    defer session.Close()
    session.SetMode(mgo.Monotonic, true)

    fmt.Println("----------Sign Up-----------")

   
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
    
    url := variables.AWSEndPoint + "/registerUser"

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
    
    err = c.Insert(&Profile{name, username, true})
    if err != nil {
        log.Fatal(err)
    }

    result := Profile{}
    err = c.Find(bson.M{"username": username}).One(&result)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println("Name: ", result.Name, "        UserName: ", result.UserName, "     loggedIn: ",result.LoggedIn)
}

func main() {
    fmt.Println("###################################################### GOChatCLI ###################################################### ")

    signIn()
    
    c := make(chan os.Signal, 2)
    signal.Notify(c, os.Interrupt, syscall.SIGTERM)
    go func() {
        <-c
        loginLogout(false)
        os.Exit(1)
    }()
}
