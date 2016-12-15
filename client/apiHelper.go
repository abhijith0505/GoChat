package main

import (
"fmt"
"bytes"
"net/http"
"./variables"
)

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
        //panic(err)  
    }
    buf := new(bytes.Buffer)
    buf.ReadFrom(resp.Body)
    response := buf.String()

    //fmt.Println(response)
    defer resp.Body.Close()
    userPresent = response

    return userPresent
}



func main() {
    var username,password string
    fmt.Println("Enter your username:")
    fmt.Scanf("%s", &username)
    
    fmt.Println("Enter your password:")
    fmt.Scanf("%s", &password)   

    checkUser(username)
}
