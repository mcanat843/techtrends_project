package main
import(
	"fmt"
	"net/http"
)
func helloWorld(w http.ResponseWriter, r *http.Request)  {
	fmt.Fprintf(w,"Hello World")
	
}

func main()  {
	http.HandleFunc("/", helloWorld)
	http.ListenAndServe(":7111", nil)
	
}

// #35d78936-69fe-4405-b32d-f6fc6598e022